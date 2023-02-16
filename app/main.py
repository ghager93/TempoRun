import os

import typer

from app.conf import config, ROOT_DIR
from app.cli import list, calculate
from app.models import SQLModel


app = typer.Typer()
app.add_typer(list.app, name="list")
app.add_typer(calculate.app, name="calculate")

@app.command()
def hello(name: str):
    print(f"Hello {name}")


@app.command()
def listaudio():
    print(os.listdir(os.path.join(ROOT_DIR, config.get("audio_dir"))))

if __name__ == "__main__":
    app()