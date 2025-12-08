"""Shim for backward compatibility during v2 refactor.

Primary implementation now lives in `ttkbootstrap.core.appconfig`. This file
remains to keep imports working while the project migrates to the new layout.
"""
from ttkbootstrap.core.appconfig import *  # noqa: F401,F403
