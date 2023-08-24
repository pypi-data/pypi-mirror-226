"""aiobafi6 discovery.

Provides functionality to discover BAF i6 API services.
"""
from __future__ import annotations

import asyncio
import inspect
import logging
from dataclasses import dataclass
from typing import Callable, Dict, Optional, Sequence, Set, Tuple

from zeroconf import ServiceStateChange, Zeroconf
from zeroconf.asyncio import AsyncServiceBrowser, AsyncServiceInfo

from .const import MIN_API_VERSION

__all__ = ("PORT", "ZEROCONF_SERVICE_TYPE", "Service", "ServiceBrowser")

_LOGGER = logging.getLogger(__name__)

"""Default service API port number. Only use to manually create a `Service` object."""
PORT = 31415

"""Zeroconf service type for BAF API DNS service discovery."""
ZEROCONF_SERVICE_TYPE = "_api._tcp.local."


@dataclass
class Service:
    """Represents a BAF i6 API service.

    A service is uniquely identified by a device UUID and provides a device name, model
    name, and API endpoints (address:port).

    A Device object can be created using a Service object.
    """

    ip_addresses: Tuple[str]
    port: int
    uuid: Optional[str] = None
    service_name: Optional[str] = None
    device_name: Optional[str] = None
    model: Optional[str] = None
    api_version: Optional[str] = None

    def __init__(
        self,
        ip_addresses: Sequence[str],
        port: int,
        uuid: Optional[str] = None,
        service_name: Optional[str] = None,
        device_name: Optional[str] = None,
        model: Optional[str] = None,
        api_version: Optional[str] = None,
    ):
        self.ip_addresses = tuple(ip for ip in ip_addresses)
        self.port = port
        self.uuid = uuid
        self.service_name = service_name
        self.device_name = device_name
        self.model = model
        self.api_version = api_version


class ServiceBrowser:
    """Discovers BAF i6 API services.

    This class manages a `AsyncServiceBrowser` bound to a provided `Zeroconf` object
    to discover BAF i6 API services. The browser will call `callback` with a tuple of
    `Service` objects whenever the browser detects a change in service availability.
    """

    def __init__(self, zconf: Zeroconf, callback: Callable):
        self._callback = callback

        # Map device UUID to Service object. When a device is renamed, the service
        # record with the old name won't be removed until a TTL expires, so the
        # service/device name is not a good key.
        self._service_map: Dict[str, Service] = {}

        # Set of outstanding tasks spawned from the service browser.
        self._tasks: Set[asyncio.Task] = set()

        self._asb = AsyncServiceBrowser(
            zconf, ["_api._tcp.local."], handlers=[self._on_state_change]
        )

    def _dispatch_callback(self) -> None:
        services = tuple(s for s in self._service_map.values())
        if inspect.iscoroutinefunction(self._callback):
            task = asyncio.create_task(self._callback(services))
            self._tasks.add(task)
            task.add_done_callback(self._tasks.remove)
        else:
            self._callback(services)

    async def _async_resolve_service(
        self, zeroconf: Zeroconf, service_type: str, service_name: str
    ) -> None:
        info = AsyncServiceInfo(service_type, service_name)
        if not await info.async_request(zeroconf, 3000):
            _LOGGER.info("Failed to resolve service %s.", service_name)
            return
        if info.properties is None:
            _LOGGER.info("Service %s has no properties.", service_name)
            return
        if len(info.addresses) == 0:
            _LOGGER.info("Service %s has no addresses.", service_name)
            return
        if info.port is None:
            _LOGGER.info("Service %s has no port.", service_name)
            return
        try:
            api_version = info.properties[b"api version"].decode("utf-8")
            api_version_int = int(api_version)
            model = info.properties[b"model"].decode("utf-8")
            uuid = info.properties[b"uuid"].decode("utf-8")
            device_name = info.properties[b"name"].decode("utf-8")
        except (ValueError, KeyError) as err:
            _LOGGER.info(
                "Failed to parse service properties for %s: %s\n%s",
                service_name,
                err,
                info.properties,
            )
            return
        if api_version_int < MIN_API_VERSION:
            _LOGGER.info(
                "Ignoring service %s because api_version is < %d: %s",
                service_name,
                MIN_API_VERSION,
                api_version,
            )
            return
        _LOGGER.info(
            "Resolved service %s: device_name=`%s`, model=`%s`, uuid=%s, "
            " api_version=%s, ip_addresses=%s, port=%s",
            service_name,
            device_name,
            model,
            uuid,
            api_version,
            info.parsed_scoped_addresses(),
            info.port,
        )
        service = Service(
            info.parsed_scoped_addresses(),
            info.port,
            uuid,
            service_name,
            device_name,
            model,
            api_version,
        )
        self._service_map[uuid] = service
        self._dispatch_callback()

    def _on_state_change(
        self,
        zeroconf: Zeroconf,
        service_type: str,
        name: str,
        state_change: ServiceStateChange,
    ) -> None:
        _LOGGER.info("Service %s state changed: %s", name, state_change)
        if state_change == ServiceStateChange.Removed:
            for k in tuple(self._service_map.keys()):
                if self._service_map[k].service_name == name:
                    del self._service_map[k]
            self._dispatch_callback()
        else:
            task = asyncio.create_task(
                self._async_resolve_service(zeroconf, service_type, name)
            )
            self._tasks.add(task)
            task.add_done_callback(self._tasks.remove)
