"""Deprecated module path shim for `ttkbootstrap.tableview`.

This module is deprecated. Use `ttkbootstrap.widgets.tableview` instead.
"""
import warnings

warnings.warn(
    "ttkbootstrap.tableview is deprecated; import from ttkbootstrap.widgets.tableview",
    DeprecationWarning,
    stacklevel=2,
)

from .widgets.tableview import *  # re-export

