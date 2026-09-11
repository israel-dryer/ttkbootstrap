"""Pyinstaller hook to include static assets"""

import os


def get_hook_dirs() -> list[str]:
    """Returns the absolute path of this directory to PyInstaller."""
    return [os.path.dirname(__file__)]
