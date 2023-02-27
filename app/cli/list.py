import os
import enum
import math

from typing import Optional, List

import typer

from sqlmodel import select
from rich.console import Console
from rich.table import Table

from app import db
from app.conf import config
from app.exceptions import ArgumentException
from app.models import AudioFile


app = typer.Typer()


class OrderBy(str, enum.Enum):
    name = "name"
    duration = "duration"
    tempo = "tempo"


@app.callback(invoke_without_command=True)
def list_cli(
    tempo: Optional[int] = typer.Option(None),
    threshold: Optional[int] = typer.Option(5),
    min_tempo: Optional[int] = typer.Option(None),
    max_tempo: Optional[int] = typer.Option(None),
    order_by: OrderBy = typer.Option(OrderBy.name, case_sensitive=False),
    order_ascending: Optional[bool] = typer.Option(True),
    fold: Optional[bool] = typer.Option(True)
):
    list(
        tempo,
        threshold,
        min_tempo,
        max_tempo,
        order_by,
        order_ascending,
        fold
    )


def list(
    tempo: Optional[int] = None,
    threshold: Optional[int] = 5,
    min_tempo: Optional[int] = None,
    max_tempo: Optional[int] = None,
    order_by: OrderBy = OrderBy.name,
    order_ascending: bool = True,
    fold: bool = True
) -> None:
    if tempo and (min_tempo or max_tempo):
        raise ArgumentException("Either set tempo or min and/or max, not both.")
    
    if not (tempo or (min_tempo or max_tempo)):
        audiofiles = _get_all()
    elif fold:
        audiofiles = list(filter(lambda x: _can_fold_into(x.bpm, min_tempo, max_tempo), _get_all()))
    else:    
        if tempo:
            min_tempo = tempo-threshold
            max_tempo = tempo+threshold

        audiofiles = _get_range(min_tempo, max_tempo)

    table = Table(title="Audio Tracks")
    table.add_column("Title")
    table.add_column("Tempo")
    for audiofile in audiofiles:
        table.add_row(audiofile.name, str(audiofile.bpm))

    console = Console()
    console.print(table)


def _get_range(min_tempo: int, max_tempo: int) -> List[AudioFile]:
    session = db.get_session()

    if min_tempo is None:
        statement = select(AudioFile).where(AudioFile.bpm <= max_tempo)
    elif max_tempo is None:
        statement = select(AudioFile).where(AudioFile.bpm >= min_tempo)
    else:
        statement = select(AudioFile).where(AudioFile.bpm >= min_tempo).where(AudioFile.bpm <= max_tempo)

    return session.exec(statement)


def _get_all() -> List[AudioFile]:
    session = db.get_session()

    return session.exec(select(AudioFile))


def _can_fold_into(tempo: int, min_tempo: int, max_tempo: int) -> bool:
    return math.ceil(math.log2(min_tempo) - math.log2(tempo)) <= max_tempo

