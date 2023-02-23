import os
import random
import time
import subprocess
from typing import Optional
from datetime import datetime
from tempfile import NamedTemporaryFile

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
    process = subprocess.Popen(["nohup", "./entrypoint", "play-process", f"--duration={duration}", f"--offset={offset}", filename])

    # Need 2 seconds to allow for ffplay process to start. 
    time.sleep(5)
    child_processes = _get_child_processes(str(process.pid))
    print(child_processes)
    _save_audiopid_to_database(filename, process.pid, child_processes[0])
    

def _save_audiopid_to_database(filename: str, pid: str, ffplay_pid: str) -> None:
    timestamp = datetime.now()
    audiopid = AudioPID(
        name=filename,
        process_id=pid,
        ffplay_pid=ffplay_pid,
        created_at=timestamp,
        updated_at=timestamp
    )
    print(audiopid)
    print(audiopid.ffplay_pid)

    session = db.get_session()
    session.add(audiopid)
    session.commit()


def _clear_audiopid(pid: str) -> None:
    session = db.get_session()
    results = session.exec(select(AudioPID).where(AudioPID.process_id == pid))
    audiopid = results.first()

    if audiopid:
        session.delete(audiopid)
        session.commit()


def _play_file_pydub(filename: str, duration: int = 3, offset: int = 0) -> None:
    audio = pydub.AudioSegment.from_file(
        utils.abs_path(os.path.join(config.get("audio_dir"), filename))
    )
    
    if offset > len(audio):
        raise ArgumentException(f"Offset longer than file length. Please choose smaller offset. File length: {len(audio)} milliseconds.")
    segment_end = min((offset + duration)*1000, len(audio)-1)

    playback.play(audio[offset*1000:segment_end])


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


def _get_child_processes(pid: str) -> list[str]:
    result = subprocess.run(["pgrep", "-P", pid], capture_output=True)
    print(result.stdout.decode("utf-8").strip())
    return result.stdout.decode("utf-8").splitlines()