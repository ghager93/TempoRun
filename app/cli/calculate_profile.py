from typing import Optional

import typer
import rich
from rich.prompt import Prompt, Confirm

from sqlmodel import select

from app import db
from app.cli import list
from app.models import Profile


app = typer.Typer()

@app.callback(invoke_without_command=True)
def calculate_stride(height: Optional[float] = typer.Option(None, prompt="What is your height? (metres)"), kph: Optional[float] = typer.Option(None, prompt="What speed do you want to run at? (kph)")):
    stride = _height2stride(height)
    mps = _kph2mps(kph)
    ideal_tempo = _ideal_tempo(stride, mps)

    rich.print(f"Your stride is approximately {stride} metres.")
    rich.print(f"The ideal music tempo for you to run to at {kph} kph is {ideal_tempo} bpm.")
    
    do_save_to_profile = Confirm.ask("Would you like to save this information to a profile?", default=False)

    if do_save_to_profile:
        session = db.get_session()

        curr_profile_names = [profile.name for profile in session.exec(select(Profile))]

        while True:
            profile_name = Prompt.ask("Name for profile")
            if profile_name == "":
                rich.print("Profile name cannot be blank.")
            elif profile_name in curr_profile_names:
                rich.print("Profile name already exists, please choose another.")
            else:
                break

        profile = Profile(
            name=profile_name,
            stride=stride,
            mps=mps,
            ideal_bpm=ideal_tempo
        )

        session.add(profile)
        session.commit()

    rich.print("Here are some tracks you could run to:")
    list.list(tempo=ideal_tempo)



def _height2stride(height: float) -> float:
    return 0.414 * height


def _kph2mps(kph: float) -> float:
    return round(kph*1000/3600, 2)


def _ideal_tempo(stride: float, mps: float) -> int:
    return int(mps/stride * 60)