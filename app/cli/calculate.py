import os
import glob

from datetime import datetime
from typing import Optional

import typer
import pydub

from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn
from sqlmodel import select

from app import db
from app import utils
from app.detection import detection
from app.models import AudioFile
from app.conf import config
from app.exceptions import ArgumentException


app = typer.Typer()

@app.callback(invoke_without_command=True)
def calculate(path: Optional[str] = typer.Argument(None), simple: bool = typer.Option(False)):
    session = db.get_session()

    timestamp = datetime.now()

    if path:
        path = os.path.join(config.get("audio_dir"), path)
        if os.path.isfile(path):
            audio_filenames = [path]
        elif os.path.isdir(path):
            audio_filenames = utils.get_relative_audio_paths(path)
        else:
            raise ArgumentException(f"Invalid filepath: {path}")
    else:
        audio_filenames = utils.get_relative_audio_paths(config.get("audio_dir"))

    curr_audiofiles = session.exec(select(AudioFile))
    curr_audiofiles_dict = {a.name: a for a in curr_audiofiles}

    for filename in audio_filenames:
        if simple:
            bpm = None
        else:
            audio_segment = pydub.AudioSegment.from_file(
                utils.abs_path(os.path.join(config.get("audio_dir"), filename))
            )

            progress = Progress(
                SpinnerColumn(),
                TextColumn("{task.description}"),
                "Elapsed: ",
                TimeElapsedColumn()
            )
            with progress:
                progress.add_task(description=f"Calculating bpm for {filename}... ")
                bpm = round(detection.get_global_tempo(audio_segment))

        if filename in curr_audiofiles_dict:
            audio_file = curr_audiofiles_dict[filename]
            audio_file.updated_at = timestamp
            if not simple:
                audio_file.bpm = bpm
        else:
            audio_file = AudioFile(
                name=filename,
                bpm=bpm,
                created_at=timestamp,
                updated_at=timestamp
            )
            session.add(audio_file)

    session.commit()
