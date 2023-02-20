import os
import signal

import typer

from app.conf import config, ROOT_DIR
from app.cli import list, calculate, play


def handle_sigint_clear_audiopid() -> None:
    play._clear_audiopid(os.getpid())


signal.signal(signal.SIGTERM, handle_sigint_clear_audiopid)


app = typer.Typer()
app.add_typer(list.app, name="list")
app.add_typer(calculate.app, name="calculate")
app.add_typer(play.app, name="play")

@app.command()
def hello(name: str):
    print(f"Hello {name}")


@app.command()
def listaudio():
    print(os.listdir(os.path.join(ROOT_DIR, config.get("audio_dir"))))


if __name__ == "__main__":
    app()