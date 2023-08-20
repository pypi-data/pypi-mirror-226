from decimal import Decimal

import rspro82.message as message


def test_start():
    command = message.Start()
    packet = message.Packet.from_command(command)
    assert packet.as_bytes() == bytes([0x81, 0x04, 0x01, 0x00, 0x00, 0xFB])


def test_channel_checksum():
    # https://forums.radioreference.com/threads/pro-82-20-315-comp-programing.150862/page-3
    command = message.ProgramChannel(
        channel=25,
        frequency=Decimal("155.025"),
        delay=True,
        lockout=False,
        priority=False,
    )
    packet = message.Packet.from_command(command)
    assert packet.checksum == b"\xa9"
