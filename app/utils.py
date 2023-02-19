import os

from app.conf import config, ROOT_DIR


def list_audio() -> list[str]:
    return os.listdir(abs_path(config.get("audio_dir")))


def abs_path(relative_path: str) -> str:
    return os.path.join(ROOT_DIR, relative_path)