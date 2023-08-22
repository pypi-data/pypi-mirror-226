import os

import click

_INTERNAL_FOLDER_NAME = ".flockfysh"


def _find_flockfysh_workspace() -> str or None:
    prev_path = None
    cur_path = os.getcwd()
    while True:
        if cur_path == prev_path:
            cur_path = None
            break
        else:
            if os.path.isdir(os.path.join(cur_path, ".flockfysh")):
                break
            prev_path = cur_path
        cur_path = os.path.realpath(os.path.join(cur_path, ".."))
    return cur_path


_global_workspace_dir = _find_flockfysh_workspace()


def flockfysh_path(directory):
    global _global_workspace_dir
    return os.path.join(_global_workspace_dir, _INTERNAL_FOLDER_NAME, directory)


def _check_flockfysh_dir(func):
    def decorated(*args, **kwargs):
        if _global_workspace_dir is not None and os.path.exists(
                os.path.join(_global_workspace_dir, _INTERNAL_FOLDER_NAME)):
            return func(*args, **kwargs)
        else:
            raise FileNotFoundError("Flockfysh directory not found.")

    return decorated


def init_project():
    if _global_workspace_dir is not None:
        if click.confirm(
                f"Are you sure to create a new project? You might want to use another folder instead. {_global_workspace_dir}"):
            os.makedirs(_INTERNAL_FOLDER_NAME, exist_ok=True)
    os.makedirs(_INTERNAL_FOLDER_NAME, exist_ok=True)
    os.makedirs(os.path.join(_INTERNAL_FOLDER_NAME, "assets"), exist_ok=True)
    os.makedirs(os.path.join(_INTERNAL_FOLDER_NAME, "streams"), exist_ok=True)
