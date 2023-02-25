import os

import typer

from app.conf import config


app = typer.Typer()


@app.callback(invoke_without_command=True)
def list():
    print(os.listdir(config.get("audio_dir")))
