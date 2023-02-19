import os
import random
import time

import typer
import vlc

from app import utils
from app.conf import config, ROOT_DIR


app = typer.Typer()


@app.command()
def play():
    songs = utils.list_audio()
    song = random.choice(songs)
    player = vlc.MediaPlayer(utils.abs_path(os.path.join(config.get('audio_dir'), song)))
    player.play()

    time.sleep(10)

