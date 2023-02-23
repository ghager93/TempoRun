import os
import random
import time
import subprocess
import signal
from typing import Optional
from datetime import datetime

import typer
import pydub

from pydub import playback
from sqlmodel import select

from app import db
from app import utils
from app.conf import config, ROOT_DIR
from app.models import AudioPID
from app.exceptions import ArgumentException


app = typer.Typer()


@app.callback(invoke_without_command=True)
def stop(    
    file: Optional[str] = typer.Argument(None),
    metronome: bool = typer.Option(False),
    all: bool = typer.Option(False)
) -> None:
    if all and file:
        raise ArgumentException("Cannot both include a filename and the --all flag.  Please choose either or neither.")

    session = db.get_session()

    if all:
        audiopids = session.exec(select(AudioPID)).all()
    elif file:
        audiopids = [session.exec(select(AudioPID).where(AudioPID.name == file)).first()]
    else:
        audiopids = [session.exec(select(AudioPID).order_by(AudioPID.updated_at)).first()]

    running_audiopids = list(filter(_is_audiopid_running, audiopids))
    print(audiopids, running_audiopids)
    if not metronome:
        _terminate_audiopids(running_audiopids)

    _delete_audiopids(session, audiopids)


def _is_audiopid_running(audiopid: AudioPID) -> bool:
    return _is_running(audiopid.ffplay_pid)


def _is_running(pid: str) -> bool:
    try:
        os.kill(int(pid), 0)
        return True
    except OSError:
        return False


def _terminate_audiopids(audiopids: list[AudioPID]) -> None:
    print("terminating", audiopids)
    [os.kill(int(ap.ffplay_pid), signal.SIGTERM) for ap in audiopids]


def _delete_audiopids(session, audiopids):
    [session.delete(ap) for ap in audiopids]
    session.commit()


    
    