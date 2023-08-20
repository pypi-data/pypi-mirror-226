from decimal import Decimal
from pathlib import Path

import pandas as pd

from rspro82.message import ProgramChannel


def commands_from_csv(path: Path) -> list[ProgramChannel]:
    df = pd.read_csv(
        path,
        usecols=["Channel", "Frequency", "Delay", "Lockout", "Priority"],
        dtype=dict(Channel=int, Frequency=str, Delay=bool, Lockout=bool, Priority=bool),
    )
    commands = []
    for _idx, row in df.iterrows():
        commands.append(
            ProgramChannel(
                channel=row.Channel,
                frequency=Decimal(row.Frequency),
                delay=row.Delay,
                lockout=row.Lockout,
                priority=row.Priority,
            )
        )
    return commands
