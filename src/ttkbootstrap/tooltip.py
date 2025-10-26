"""Deprecated module path shim for `ttkbootstrap.tooltip`.

This module is deprecated. Use `ttkbootstrap.widgets` instead.
"""
import warnings

warnings.warn(
    "ttkbootstrap.tooltip is deprecated; import from ttkbootstrap.widgets",
    DeprecationWarning,
    stacklevel=2,
)

from .widgets.tooltip import *  # re-export

