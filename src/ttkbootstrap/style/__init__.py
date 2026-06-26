"""ttkbootstrap style engine package.

Public import path `ttkbootstrap.style` (unchanged from the pre-2.0 single
module). The implementation is split across submodules (`theme`, `builders_tk`,
`builders_ttk`, `engine`, `bootstyle`); those submodule paths are
implementation detail and carry no back-compat guarantee. Import the names below
from `ttkbootstrap.style` (or, preferably, from `ttkbootstrap`).
"""
from ttkbootstrap.style.theme import Colors, ThemeDefinition
from ttkbootstrap.style.builders_tk import StyleBuilderTK
from ttkbootstrap.style.builders_ttk import StyleBuilderTTK
from ttkbootstrap.style.engine import Style
from ttkbootstrap.style.bootstyle import (
    Keywords,
    Bootstyle,
    BootMixin,
    AutoStyleMixin,
    bootify,
    apply_bootstyle,
    enable_global_api,
)

__all__ = [
    "Colors",
    "ThemeDefinition",
    "StyleBuilderTK",
    "StyleBuilderTTK",
    "Style",
    "Keywords",
    "Bootstyle",
    "BootMixin",
    "AutoStyleMixin",
    "bootify",
    "apply_bootstyle",
    "enable_global_api",
]
