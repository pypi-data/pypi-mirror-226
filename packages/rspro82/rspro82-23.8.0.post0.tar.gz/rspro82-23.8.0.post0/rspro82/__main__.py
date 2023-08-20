import time
from pathlib import Path

import serial
import typer

from rspro82.message import Message
from rspro82.channels import commands_from_csv


def main(port: Path, spreadsheet: Path):
    commands = commands_from_csv(spreadsheet)
    data = Message.from_commands(commands).data
    ser = serial.Serial(str(port), 4800, 8, "N", 2)

    for packet in data:
        ser.write(packet)
        time.sleep(0.2)

    ser.close()


def entrypoint():
    typer.run(main)


if __name__ == "__main__":
    entrypoint()
