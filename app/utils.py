import os
import glob

from app.conf import config, ROOT_DIR


def list_audio() -> list[str]:
    return os.listdir(abs_path(config.get("audio_dir")))


def list_audio_recursive(root_dir: str = None) -> list[str]:
    valid_formats = {".mp3", ".mp4", ".m4a", ".flac", ".aac", ".wav", ".wma"}

    if not root_dir:
        root_dir = config.get("audio_dir")

    all_files = glob.glob(os.path.join(root_dir, "**/*"), recursive=True)
    return list(filter(lambda file: os.path.splitext(file)[1] in valid_formats, all_files))


def get_relative_audio_paths(root_dir: str = None) -> list[str]:
    paths = list_audio_recursive(root_dir)
    return [strip_audio_dir_from_path(path) for path in paths]


def strip_audio_dir_from_path(path: str) -> str:
    return _strip_root_dir_from_path(path, config.get("audio_dir"))


def _strip_root_dir_from_path(path: str, root_dir: str) -> str:
    if path.startswith(root_dir):
        path = path[len(root_dir):]
    if path.startswith("/"):
        path = path[1:]
    return path


def abs_path(relative_path: str) -> str:
    return os.path.join(ROOT_DIR, relative_path)