import os
import random
import time
import subprocess
from typing import Optional
from datetime import datetime
from tempfile import NamedTemporaryFile

import typer
import pydub


from app import utils
from app.conf import config
from app.exceptions import ArgumentException


app = typer.Typer()


@app.callback(invoke_without_command=True)
def play_process(
    file: Optional[str] = typer.Argument(None),
    metronome: bool = typer.Option(False),
    duration: int = typer.Option(3),
    offset: int = typer.Option(0),
) -> None:
    audio = pydub.AudioSegment.from_file(
        utils.abs_path(os.path.join(config.get("audio_dir"), file))
    )
    if offset > len(audio):
        raise ArgumentException(f"Offset longer than file length. Please choose smaller offset. File length: {len(audio)} milliseconds.")
    segment_end = min((offset + duration)*1000, len(audio)-1)

    play(audio[offset*1000:segment_end])

    time.sleep(60)


def play(seg):
    PLAYER = "ffplay"
    with NamedTemporaryFile("w+b", suffix=".wav") as f:
        name = f.name
        seg.export(f.name, "wav")
        process = subprocess.Popen([PLAYER, "-nodisp", "-autoexit", "-hide_banner", f.name])
        time.sleep(0.1)
    return process