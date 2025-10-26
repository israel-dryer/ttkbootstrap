"""Deprecated module path shim for `ttkbootstrap.toast`.

This module is deprecated. Use `ttkbootstrap.widgets` instead.
"""
import warnings

warnings.warn(
    "ttkbootstrap.toast is deprecated; import from ttkbootstrap.widgets",
    DeprecationWarning,
    stacklevel=2,
)

from .widgets.toast import *  # re-export

