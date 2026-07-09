"""ttkbootstrap style engine package.

Public import path `ttkbootstrap.style` (unchanged from the pre-2.0 single
module). The implementation is split across submodules (`theme`, `builders_tk`,
`builders_ttk`, `engine`, `bootstyle`); those submodule paths are
implementation detail and carry no back-compat guarantee. Import the names below
from `ttkbootstrap.style` (or, preferably, from `ttkbootstrap`).
"""
from ttkbootstrap.style.theme import Colors, RampColor, Theme, ThemeDefinition
from ttkbootstrap.style.builders_tk import StyleBuilderTK
from ttkbootstrap.style.builders_ttk import StyleBuilderTTK
from ttkbootstrap.style.engine import Style
from ttkbootstrap.style.bootstyle import (
    Keywords,
    Bootstyle,
    FluentGeometryMixin,
    BootMixin,
    AutoStyleMixin,
    bootify,
    apply_bootstyle,
    enable_global_api,
)
from ttkbootstrap.style.assets import Assets
from ttkbootstrap.style.layout import (
    El,
    layout,
    register_style,
    image_element,
    statespec,
    state_map,
    StyleName,
)
from ttkbootstrap.style.icons import Icon, apply_icon, icon_element, IconRenderer
from ttkbootstrap.style._compat import (
    set_bootstyle_strict,
    is_bootstyle_strict,
)

__all__ = [
    "Colors",
    "RampColor",
    "Theme",
    "ThemeDefinition",
    "StyleBuilderTK",
    "StyleBuilderTTK",
    "Style",
    "Keywords",
    "Bootstyle",
    "FluentGeometryMixin",
    "BootMixin",
    "AutoStyleMixin",
    "bootify",
    "apply_bootstyle",
    "enable_global_api",
    # Style-construction toolkit (Workstream I)
    "Assets",
    "El",
    "layout",
    "register_style",
    "image_element",
    "statespec",
    "state_map",
    "StyleName",
    # Icon-rendered assets (Workstream I, Tier 1.5)
    "Icon",
    "apply_icon",
    "icon_element",
    "IconRenderer",
    # bootstyle grammar strictness (Workstream D)
    "set_bootstyle_strict",
    "is_bootstyle_strict",
]
