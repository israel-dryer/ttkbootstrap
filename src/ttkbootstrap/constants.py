"""Constants and type aliases for ttkbootstrap.

This module defines constants and type aliases used throughout ttkbootstrap,
including tkinter/ttk configuration values and ttkbootstrap-specific enums.

The module provides:
    - Type aliases using Literal for better type checking
    - Standard tkinter constants (anchor, fill, relief, etc.)
    - TTkbootstrap-specific constants (bootstyle colors and types)
    - Final-typed constants for IDE autocomplete

All constants are exported in __all__ for easy wildcard import:
    ```python
    from ttkbootstrap.constants import *
    ```

Type Aliases:
    Anchor: Widget anchor positions (n, s, e, w, nw, ne, sw, se, center)
    Fill: Fill modes for pack geometry manager (none, x, y, both)
    Side: Widget placement side (left, top, right, bottom)
    Relief: Border relief style (raised, sunken, flat, ridge, groove, solid)
    Orient: Widget orientation (horizontal, vertical)
    State: Widget state (normal, disabled, active, hidden, readonly)
    BootColor: Bootstyle color names (primary, secondary, success, etc.)
    BootType: Bootstyle type modifiers (outline, link, toggle, etc.)

Example:
    ```python
    import ttkbootstrap as ttk
    from ttkbootstrap.constants import *

    root = ttk.Window()

    # Use constants for cleaner code
    btn = ttk.Button(root, text="OK", bootstyle=SUCCESS)
    btn.pack(side=LEFT, fill=X, padx=10)

    root.mainloop()
    ```
"""
from __future__ import annotations

from typing import Final, Literal

# ---------------------------
# Type aliases (Literal unions)
# ---------------------------

Anchor = Literal["nw", "n", "ne", "w", "center", "e", "sw", "s", "se"]

# Tk uses the same value set for -fill and many APIs call this "sticky"
Sticky = Literal["none", "x", "y", "both"]
Fill = Sticky

Side = Literal["left", "top", "right", "bottom"]

Relief = Literal["raised", "sunken", "flat", "ridge", "groove", "solid"]

Orient = Literal["horizontal", "vertical"]

Tabs = Literal["numeric"]

Wrap = Literal["char", "word"]

Align = Literal["baseline"]

TkBoolean = Literal[0, 1, True, False]

BorderMode = Literal["inside", "outside"]

State = Literal["normal", "disabled", "active", "hidden", "readonly"]

MenuItemType = Literal["cascade", "checkbutton", "command", "radiobutton", "separator"]

SelectMode = Literal["single", "browse", "multiple", "extended"]

ActiveStyle = Literal["none", "dotbox", "underline"]

PieStyle = Literal["pieslice", "chord", "arc"]

LineCap = Literal["butt", "projecting", "round"]

LineJoin = Literal["bevel", "miter", "round"]

IndexPos = Literal["first", "last"]

ViewArg = Literal["moveto", "scroll", "units", "pages"]

TtkTheme = Literal["clam", "alt", "default"]

MeterMode = Literal["full", "semi"]

ProgressMode = Literal["determinate", "indeterminate"]

BootColor = Literal["primary", "secondary", "success", "danger", "warning", "info", "light", "dark"]

BootType = Literal["outline", "link", "toggle", "inverse", "striped", "toolbutton", "square"]

TreeviewDisplay = Literal["tree", "headings", "tree headings"]

# ---------------------------
# Booleans (legacy Tk style)
# ---------------------------
NO = FALSE = OFF = 0  # type: Final[TkBoolean]
YES = TRUE = ON = 1  # type: Final[TkBoolean]

# ---------------------------
# -anchor / -sticky
# ---------------------------
N: Final[Anchor] = "n"
S: Final[Anchor] = "s"
W: Final[Anchor] = "w"
E: Final[Anchor] = "e"
NW: Final[Anchor] = "nw"
SW: Final[Anchor] = "sw"
NE: Final[Anchor] = "ne"
SE: Final[Anchor] = "se"
NS: Final[Anchor] = "ns"
EW: Final[Anchor] = "ew"
NSEW: Final[Anchor] = "nsew"
CENTER: Final[Anchor] = "center"

# ---------------------------
# -fill
# ---------------------------
NONE: Final[Fill] = "none"
X: Final[Fill] = "x"
Y: Final[Fill] = "y"
BOTH: Final[Fill] = "both"

# ---------------------------
# -side
# ---------------------------
LEFT: Final[Side] = "left"
TOP: Final[Side] = "top"
RIGHT: Final[Side] = "right"
BOTTOM: Final[Side] = "bottom"

# ---------------------------
# -relief
# ---------------------------
RAISED: Final[Relief] = "raised"
SUNKEN: Final[Relief] = "sunken"
FLAT: Final[Relief] = "flat"
RIDGE: Final[Relief] = "ridge"
GROOVE: Final[Relief] = "groove"
SOLID: Final[Relief] = "solid"

# ---------------------------
# -orient
# ---------------------------
HORIZONTAL: Final[Orient] = "horizontal"
VERTICAL: Final[Orient] = "vertical"

# ---------------------------
# -tabs
# ---------------------------
NUMERIC: Final[Tabs] = "numeric"

# ---------------------------
# -wrap
# ---------------------------
CHAR: Final[Wrap] = "char"
WORD: Final[Wrap] = "word"

# ---------------------------
# -align
# ---------------------------
BASELINE: Final[Align] = "baseline"

# ---------------------------
# -bordermode
# ---------------------------
INSIDE: Final[BorderMode] = "inside"
OUTSIDE: Final[BorderMode] = "outside"

# ---------------------------
# Special tags / marks / positions
# ---------------------------
SEL: Final[str] = "sel"
SEL_FIRST: Final[str] = "sel.first"
SEL_LAST: Final[str] = "sel.last"
END: Final[str] = "end"
INSERT: Final[str] = "insert"
CURRENT: Final[str] = "current"
ANCHOR: Final[str] = "anchor"
ALL: Final[str] = "all"  # e.g., Canvas.delete(ALL)

# ---------------------------
# States
# ---------------------------
NORMAL: Final[State] = "normal"
DISABLED: Final[State] = "disabled"
ACTIVE: Final[State] = "active"
HIDDEN: Final[State] = "hidden"  # Canvas state
READONLY: Final[State] = "readonly"  # ttk state

# ---------------------------
# Menu item types
# ---------------------------
CASCADE: Final[MenuItemType] = "cascade"
CHECKBUTTON: Final[MenuItemType] = "checkbutton"
COMMAND: Final[MenuItemType] = "command"
RADIOBUTTON: Final[MenuItemType] = "radiobutton"
SEPARATOR: Final[MenuItemType] = "separator"

# ---------------------------
# Listbox modes / styles
# ---------------------------
SINGLE: Final[SelectMode] = "single"
BROWSE: Final[SelectMode] = "browse"
MULTIPLE: Final[SelectMode] = "multiple"
EXTENDED: Final[SelectMode] = "extended"

DOTBOX: Final[ActiveStyle] = "dotbox"
UNDERLINE: Final[ActiveStyle] = "underline"
# (NONE from Fill is also a valid ActiveStyle value)

# ---------------------------
# Canvas styles
# ---------------------------
PIESLICE: Final[PieStyle] = "pieslice"
CHORD: Final[PieStyle] = "chord"
ARC: Final[PieStyle] = "arc"

FIRST: Final[IndexPos] = "first"
LAST: Final[IndexPos] = "last"

BUTT: Final[LineCap] = "butt"
PROJECTING: Final[LineCap] = "projecting"
ROUND: Final[LineCap] = "round"

BEVEL: Final[LineJoin] = "bevel"
MITER: Final[LineJoin] = "miter"
# ROUND already defined above for LineCap; same literal is valid for LineJoin too

# ---------------------------
# xview / yview args
# ---------------------------
MOVETO: Final[ViewArg] = "moveto"
SCROLL: Final[ViewArg] = "scroll"
UNITS: Final[ViewArg] = "units"
PAGES: Final[ViewArg] = "pages"

# ---------------------------
# Themes / ttk themes
# ---------------------------
DEFAULT: Final[str] = "default"
DEFAULT_THEME: Final[str] = "litera"

TTK_CLAM: Final[TtkTheme] = "clam"
TTK_ALT: Final[TtkTheme] = "alt"
TTK_DEFAULT: Final[TtkTheme] = "default"

# ---------------------------
# Meter / progressbar
# ---------------------------
FULL: Final[MeterMode] = "full"
SEMI: Final[MeterMode] = "semi"
DETERMINATE: Final[ProgressMode] = "determinate"
INDETERMINATE: Final[ProgressMode] = "indeterminate"

# ---------------------------
# Bootstyle colors / types
# ---------------------------
PRIMARY: Final[BootColor] = "primary"
SECONDARY: Final[BootColor] = "secondary"
SUCCESS: Final[BootColor] = "success"
DANGER: Final[BootColor] = "danger"
WARNING: Final[BootColor] = "warning"
INFO: Final[BootColor] = "info"
LIGHT: Final[BootColor] = "light"
DARK: Final[BootColor] = "dark"

OUTLINE: Final[BootType] = "outline"
LINK: Final[BootType] = "link"
TOGGLE: Final[BootType] = "toggle"
INVERSE: Final[BootType] = "inverse"
STRIPED: Final[BootType] = "striped"
TOOLBUTTON: Final[BootType] = "toolbutton"
SQUARE: Final[BootType] = "square"

# ---------------------------
# Treeview
# ---------------------------
TREE: Final[TreeviewDisplay] = "tree"
HEADINGS: Final[TreeviewDisplay] = "headings"
TREEHEADINGS: Final[TreeviewDisplay] = "tree headings"

# ---------------------------
# Public exports
# ---------------------------
__all__ = [
    # literals (type aliases)
    "Anchor", "Sticky", "Fill", "Side", "Relief", "Orient", "Tabs", "Wrap",
    "Align", "BorderMode", "State", "MenuItemType", "SelectMode", "ActiveStyle",
    "PieStyle", "LineCap", "LineJoin", "IndexPos", "ViewArg", "TtkTheme",
    "MeterMode", "ProgressMode", "BootColor", "BootType", "TreeviewDisplay",
    # constants
    "NO", "FALSE", "OFF", "YES", "TRUE", "ON",
    "N", "S", "W", "E", "NW", "SW", "NE", "SE", "NS", "EW", "NSEW", "CENTER",
    "NONE", "X", "Y", "BOTH",
    "LEFT", "TOP", "RIGHT", "BOTTOM",
    "RAISED", "SUNKEN", "FLAT", "RIDGE", "GROOVE", "SOLID",
    "HORIZONTAL", "VERTICAL",
    "NUMERIC",
    "CHAR", "WORD",
    "BASELINE",
    "INSIDE", "OUTSIDE",
    "SEL", "SEL_FIRST", "SEL_LAST", "END", "INSERT", "CURRENT", "ANCHOR", "ALL",
    "NORMAL", "DISABLED", "ACTIVE", "HIDDEN", "READONLY",
    "CASCADE", "CHECKBUTTON", "COMMAND", "RADIOBUTTON", "SEPARATOR",
    "SINGLE", "BROWSE", "MULTIPLE", "EXTENDED",
    "DOTBOX", "UNDERLINE",
    "PIESLICE", "CHORD", "ARC", "FIRST", "LAST",
    "BUTT", "PROJECTING", "ROUND", "BEVEL", "MITER",
    "MOVETO", "SCROLL", "UNITS", "PAGES",
    "DEFAULT", "DEFAULT_THEME", "TTK_CLAM", "TTK_ALT", "TTK_DEFAULT",
    "FULL", "SEMI", "DETERMINATE", "INDETERMINATE",
    "PRIMARY", "SECONDARY", "SUCCESS", "DANGER", "WARNING", "INFO", "LIGHT", "DARK",
    "OUTLINE", "LINK", "TOGGLE", "INVERSE", "STRIPED", "TOOLBUTTON", "SQUARE",
    "TREE", "HEADINGS", "TREEHEADINGS",
]
