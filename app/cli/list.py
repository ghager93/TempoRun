import os

import typer

from app.conf import config, ROOT_DIR


app = typer.Typer()


@app.command()
def list_audio():
    print(os.listdir(os.path.join(ROOT_DIR, config.get("audio_dir"))))
