# pylint: disable=protected-access, missing-class-docstring, missing-function-docstring, invalid-name, line-too-long

"""Tests for wireutils."""

from . import wireutils


def test_add_emulation_prevention():
    got = wireutils.add_emulation_prevention(b"\xc0")
    assert got == b"\xdb\xdc"
    got = wireutils.add_emulation_prevention(b"\xdb")
    assert got == b"\xdb\xdd"
    got = wireutils.add_emulation_prevention(
        b'\x12+")\x12\r\n\x0bLiving Room\x12\x04\x18\xc0\xbe\x01\x12\x03\xb0\x08\x00\x12\x03\xb8\x08\x00\x12\x03\xc0\x08\x01\x12\x03\xb0\t\x00'
    )
    assert (
        got
        == b'\x12+")\x12\r\n\x0bLiving Room\x12\x04\x18\xdb\xdc\xbe\x01\x12\x03\xb0\x08\x00\x12\x03\xb8\x08\x00\x12\x03\xdb\xdc\x08\x01\x12\x03\xb0\t\x00'
    )


def test_remove_emulation_prevention():
    got = wireutils.remove_emulation_prevention(b"\xdb\xdc")
    assert got == b"\xc0"
    got = wireutils.remove_emulation_prevention(b"\xdb\xdd")
    assert got == b"\xdb"
    got = wireutils.remove_emulation_prevention(
        b'\x12+")\x12\r\n\x0bLiving Room\x12\x04\x18\xdb\xdc\xbe\x01\x12\x03\xb0\x08\x00\x12\x03\xb8\x08\x00\x12\x03\xdb\xdc\x08\x01\x12\x03\xb0\t\x00'
    )
    assert (
        got
        == b'\x12+")\x12\r\n\x0bLiving Room\x12\x04\x18\xc0\xbe\x01\x12\x03\xb0\x08\x00\x12\x03\xb8\x08\x00\x12\x03\xc0\x08\x01\x12\x03\xb0\t\x00'
    )
