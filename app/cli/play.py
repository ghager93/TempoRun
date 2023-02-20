import os
import random
import time
import subprocess
from typing import Optional
from datetime import datetime

import typer
import vlc
import pydub

from pydub import playback
from sqlmodel import select

from app import db
from app import utils
from app.conf import config, ROOT_DIR
from app.models import AudioPID


app = typer.Typer()


@app.callback(invoke_without_command=True)
def play(
    file: Optional[str] = typer.Argument(None),
    fileno: Optional[bool] = typer.Option(False),
    metronome: bool = typer.Option(False),
    detached: bool = typer.Option(False),
    duration: int = typer.Option(3),
    offset: int = typer.Option(0),
) -> None:
    print(locals().items())
    if not file:
        filename = _get_random_audio_file()
    elif fileno:
        filename = _get_audio_file_by_fileno(file)
    else:
        filename = _get_audio_file_by_name(file)

    if detached:
        _detached_mode(filename, duration, offset)
    else:
        _play_file_pydub(filename, duration, offset)

    _clear_audiopid(os.getpid())


def _detached_mode(filename: str, duration: int = 3, offset: int = 0) -> None:
    cmd = [
        "nohup",
        "python",
        "entrypoint.py",
        "play",
        f"--duration={duration}",
        f"--offset={offset}",
        filename,
    ]
    process = subprocess.Popen(cmd)
    _save_audiopid_to_database(filename, process.pid)
    

def _save_audiopid_to_database(filename: str, pid: str) -> None:
    timestamp = datetime.now()
    audiopid = AudioPID(
        name=filename,
        process_id=pid,
        created_at=timestamp,
        updated_at=timestamp
    )

    session = next(db.get_session())
    session.add(audiopid)
    session.commit()


def _clear_audiopid(pid: str) -> None:
    session = next(db.get_session())
    results = session.exec(select(AudioPID).where(AudioPID.process_id == pid))
    audiopid = results.first()

    if audiopid:
        session.delete(audiopid)
        session.commit()


def _play_file_vlc(filename: str, duration: int = 3, offset: int = 0) -> None:
    player = vlc.MediaPlayer(
        utils.abs_path(os.path.join(config.get("audio_dir"), filename))
    )
    player.play()
    player.audio_set_mute(True)
    time.sleep(0.1)
    if player.get_length() < offset * 1000:
        raise Exception(
            f"Offset longer than file length. Please choose smaller offset."
        )
    player.audio_set_mute(False)
    player.set_time(offset * 1000)
    time.sleep(duration)


def _play_file_pydub(filename: str, duration: int = 3, offset: int = 0) -> None:
    song = pydub.AudioSegment.from_file(
        utils.abs_path(os.path.join(config.get("audio_dir"), filename))
    )

    playback.play(song)


def _get_random_audio_file() -> str:
    return random.choice(utils.list_audio())


def _get_audio_file_by_fileno(fileno: str) -> str:
    try:
        return utils.list_audio()[int(fileno)]
    except ValueError:
        raise Exception(
            f"Argument must be integer if '--fileno' option is set.  Argument received: {fileno}."
        )
    except IndexError:
        raise Exception(
            f"No file {fileno}. Please choose number between 0 and {len(utils.list_audio)}."
        )


def _get_audio_file_by_name(filename: str) -> str:
    if filename in utils.list_audio():
        return filename
    else:
        raise Exception(f"No file named {filename}.")
