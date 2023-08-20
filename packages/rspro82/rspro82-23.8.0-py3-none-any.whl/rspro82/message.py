from collections.abc import Sequence
from decimal import Decimal
from typing import ClassVar, Final, Protocol
from typing_extensions import Self

import attr

# A message is composed of packets.
# Each packet has a payload representing a command.


class Command(Protocol):
    """A Command represents an abstract instruction to the radio."""

    @property
    def magic(self) -> bytes:
        ...

    @property
    def parameter(self) -> bytes:
        ...

    @property
    def data(self) -> bytes:
        ...


class Start(Command):
    magic: Final[bytes] = b"\x01"
    parameter: Final[bytes] = b"\x00"
    data: Final[bytes] = b"\x00"


class End(Command):
    magic: Final[bytes] = b"\x02"
    parameter: Final[bytes] = b"\x00"
    data: Final[bytes] = b"\x00"


@attr.frozen
class ProgramChannel(Command):
    channel: int
    frequency: Decimal
    delay: bool
    lockout: bool
    priority: bool

    magic: ClassVar[bytes] = b"\x10"
    parameter: ClassVar[bytes] = b"\x00"

    @property
    def data(self) -> bytes:
        frequency_str = str(self.frequency.quantize(Decimal("1.0000")))
        parts = [
            *(b"C", bytes(str(self.channel), "ascii"), b"^"),
            *(b"F", bytes(frequency_str, "ascii"), b"^"),
            *(b"D", b"S" if self.delay else b"R", b"^"),
            *(b"L", b"S" if self.lockout else b"R", b"^"),
            *(b"P", b"S" if self.priority else b"R", b"^"),
        ]
        return b"".join(parts)


@attr.frozen
class Packet:
    """A packet represents a serialized Command."""

    header: ClassVar[bytes] = b"\x81"
    payload: bytes

    @property
    def length(self) -> int:
        return len(self.payload) + 1

    @property
    def checksum(self) -> bytes:
        checksum = (~((self.length + sum(self.payload)) % 256) + 1) % 256
        result = checksum.to_bytes(1, "big")
        return result

    @classmethod
    def from_command(cls, command: Command) -> Self:
        payload = b"".join([command.magic, command.parameter, command.data])
        return cls(
            payload=payload,
        )

    def as_bytes(self) -> bytes:
        return b"".join([self.header, self.length.to_bytes(1, "big"), self.payload, self.checksum])


@attr.frozen
class Message:
    """A Message represents a complete series of commands,
    expressed as packets, to send to the radio."""

    commands: tuple[Command, ...]
    packets: tuple[Packet, ...]

    @property
    def data(self) -> list[bytes]:
        return [packet.as_bytes() for packet in self.packets]

    @classmethod
    def from_commands(cls, commands: Sequence[Command]) -> Self:
        packets = [Packet.from_command(command) for command in [Start(), *commands, End()]]
        return cls(
            commands=tuple(commands),
            packets=tuple(packets),
        )
