import os

import typer

from app.conf import config, ROOT_DIR


app = typer.Typer()


@app.callback(invoke_without_command=True)
def list():
    print(os.listdir(os.path.join(ROOT_DIR, config.get("audio_dir"))))
