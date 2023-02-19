import os
import random
import time
from typing import Optional

import typer
import vlc

from app import utils
from app.conf import config, ROOT_DIR


app = typer.Typer()


@app.callback(invoke_without_command=True)
def play(file: Optional[str] = typer.Argument(None), fileno: Optional[bool] = typer.Option(False), beat_track: bool = typer.Option(False), detached: bool = typer.Option(False), duration: int = typer.Option(3), offset: int = typer.Option(0)) -> None:
    print(locals().items())
    if not file:
        filename = _get_random_audio_file()
    elif fileno:
        filename = _get_audio_file_by_fileno(file)
    else:
        filename = _get_audio_file_by_name(file)

    _play_file(filename, duration, offset)


def _play_file(filename: str, duration: int = 3, offset: int = 0) -> None:
    player = vlc.MediaPlayer(utils.abs_path(os.path.join(config.get('audio_dir'), filename)))
    player.play()
    player.audio_set_mute(True)
    time.sleep(0.1)
    if player.get_length() < offset * 1000:
        raise Exception(f"Offset longer than file length. Please choose smaller offset.")
    player.audio_set_mute(False)
    player.set_time(offset * 1000)
    time.sleep(duration)


def _get_random_audio_file() -> str:
    return random.choice(utils.list_audio())


def _get_audio_file_by_fileno(fileno: str) -> str:
    try:
        return utils.list_audio()[int(fileno)]
    except ValueError:
        raise Exception(f"Argument must be integer if '--fileno' option is set.  Argument received: {fileno}.")
    except IndexError:
        raise Exception(f"No file {fileno}. Please choose number between 0 and {len(utils.list_audio)}.")


def _get_audio_file_by_name(filename: str) -> str:
    if filename in utils.list_audio():
        return filename
    else:
        raise Exception(f"No file named {filename}.")





