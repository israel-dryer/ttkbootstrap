"""Deprecated module path shim for `ttkbootstrap.scrolled`.

This module is deprecated. Use `ttkbootstrap.widgets.scrolled` instead.
"""
import warnings

warnings.warn(
    "ttkbootstrap.scrolled is deprecated; import from ttkbootstrap.widgets.scrolled",
    DeprecationWarning,
    stacklevel=2,
)

from .widgets.scrolled import *  # re-export
