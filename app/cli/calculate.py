import os
from datetime import datetime

import typer

from app import db
from app.models import AudioFile
from app.conf import config, ROOT_DIR


app = typer.Typer()

@app.callback(invoke_without_command=True)
def calculate():
    session = db.get_session()

    timestamp = datetime.now()
    audio_filenames = os.listdir(os.path.join(ROOT_DIR, config.get("audio_dir")))

    for filename in audio_filenames:
        audio_file = AudioFile(
            name=filename,
            created_at=timestamp,
            updated_at=timestamp
        )
        session.add(audio_file)

    session.commit()