import os
from datetime import datetime

import typer
import pydub

from app import db
from app import utils
from app.models import AudioFile
from app.conf import config


app = typer.Typer()

@app.callback(invoke_without_command=True)
def calculate(simple: bool = typer.Option(False)):
    session = db.get_session()

    timestamp = datetime.now()
    audio_filenames = os.listdir(config.get("audio_dir"))

    for filename in audio_filenames:
        if not simple:
            audio = pydub.AudioSegment.from_file(
                utils.abs_path(os.path.join(config.get("audio_dir"), filename))
            )
        audio_file = AudioFile(
            name=filename,
            created_at=timestamp,
            updated_at=timestamp
        )
        session.add(audio_file)

    session.commit()