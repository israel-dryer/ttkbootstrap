"""Constants and type aliases for ttkbootstrap.

Re-exports the standard tkinter/ttk configuration values (anchors, fills,
reliefs, orientations, states) and defines the ttkbootstrap bootstyle
vocabulary: the `BootColor`/`BootType`/`BootBase` `Literal` aliases and the
color/keyword constants. All names are exported via `__all__` for
`from ttkbootstrap.constants import *`.
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

BootColor = Literal["primary", "secondary", "success", "danger", "warning", "info", "light", "dark", "neutral"]

# The bootstyle type modifiers (variant slot). NOTE for 2.0 (Workstream D): this
# is the reconciled set -- `round` is included (it is buildable; its historical
# omission was a bug), and `toggle`/`toolbutton` are *removed* because they are
# base-types (widget families), not modifiers. Those two moved to `BootBase`.
BootType = Literal["outline", "link", "ghost", "inverse", "round", "square", "striped", "thin"]

# Base-types a user may name explicitly in a bootstyle string. Most base-types
# are inferred from the widget's class and never typed; these two "chameleon"
# families are the exception (e.g. a Checkbutton rendered as a switch/toolbutton).
BootBase = Literal["toggle", "toolbutton"]

TreeviewDisplay = Literal["tree", "headings", "tree headings"]

# ---------------------------------------------------------------------------
# Bootstyle vocabulary -- the single runtime source of truth for the grammar.
# The bootstyle resolver (style/bootstyle.py) tokenizes against these tuples;
# it no longer keeps a second copy. The `Literal` aliases above must match the
# public tuples member-for-member (enforced by tests/test_bootstyle_grammar.py,
# since a static `Literal[*tuple]` is not visible to type checkers).
# ---------------------------------------------------------------------------
BOOTSTYLE_COLORS: Final = (
    "primary", "secondary", "success", "info", "warning", "danger",
    "light", "dark", "neutral",
)
# Families for which `neutral` (the derived, no-accent color) produces a real
# style. Unlike the accent colors, `neutral` is not valid everywhere -- it is a
# render policy (surface fill + derived border + normal text), meaningful only
# where accent-vs-neutral is a genuine choice. The reference generator advertises
# `neutral-<family>` only for these (see tools/generate_bootstyle_reference.py).
NEUTRAL_FAMILIES: Final = ("button", "menubutton", "toolbutton")
# Public, documented type modifiers -- matches BootType.
BOOTSTYLE_MODIFIERS: Final = (
    "outline", "link", "ghost", "inverse", "round", "square", "striped", "thin",
)
# Internal-only composite modifiers used by Meter/DateEntry/Tableview/Scrolled to
# build their sub-styles. Valid grammar tokens, but undocumented and not in any
# public Literal -- end users never type these. `card`/`highlight` are the bordered
# and focus-accent frame variants ScrolledText uses to own its border.
BOOTSTYLE_INTERNAL_MODIFIERS: Final = (
    "meter", "metersubtxt", "table", "card", "highlight",
)
# User-nameable base-types -- matches BootBase.
BOOTSTYLE_BASES: Final = ("toggle", "toolbutton")
# Every base-type/family the resolver recognizes, whether inferred from the
# widget class or named explicitly in the string.
BOOTSTYLE_FAMILIES: Final = (
    "button", "checkbutton", "radiobutton", "toggle", "toolbutton",
    "combobox", "entry", "spinbox", "scale", "progressbar", "floodgauge",
    "scrollbar", "separator", "sizegrip", "label", "labelframe", "frame",
    "notebook", "panedwindow", "treeview", "menubutton", "calendar",
    "optionmenu", "menu", "text", "canvas", "tk", "toplevel", "listbox",
)
BOOTSTYLE_ORIENTS: Final = ("horizontal", "vertical")

# Named neutral surfaces a widget can be placed on (2.0 surface-color). The
# *surface* is the background a widget renders against; the style engine resolves
# it to a concrete color (style/builders_ttk.py `resolve_surface`). `background`
# is the application default -- the only surface that produces no style-name
# segment; `card` is a mode-aware raised panel. Accent colors (BOOTSTYLE_COLORS)
# are ALSO valid surfaces (resolved separately), so a ghost/outline/link control
# can blend into an accent container. A non-default surface prefixes the style
# name with an `@<surface>.` segment. Raw-hex surfaces are deferred.
DEFAULT_SURFACE: Final = "background"
BOOTSTYLE_SURFACES: Final = ("background", "card")

# ---------------------------------------------------------------------------
# Canonical bootstyle strings (generated). The closed set of bootstyle values
# that resolve to a real ttk style, derived from the vocabulary above x the
# builder registry by tools/generate_bootstyle_reference.py. Regenerate after
# any vocabulary/builder change (a test enforces it). `bootstyle` accepts
# `BootStyle | str`; the Literal is an editor-autocomplete aid, the runtime
# validator is the real gate.
# ---------------------------------------------------------------------------
BootStyle = Literal[
    'danger',
    'danger-ghost',
    'danger-inverse',
    'danger-link',
    'danger-outline',
    'danger-outline-toolbutton',
    'danger-round',
    'danger-round-toggle',
    'danger-square-toggle',
    'danger-striped',
    'danger-thin',
    'danger-toggle',
    'danger-toolbutton',
    'dark',
    'dark-ghost',
    'dark-inverse',
    'dark-link',
    'dark-outline',
    'dark-outline-toolbutton',
    'dark-round',
    'dark-round-toggle',
    'dark-square-toggle',
    'dark-striped',
    'dark-thin',
    'dark-toggle',
    'dark-toolbutton',
    'ghost',
    'info',
    'info-ghost',
    'info-inverse',
    'info-link',
    'info-outline',
    'info-outline-toolbutton',
    'info-round',
    'info-round-toggle',
    'info-square-toggle',
    'info-striped',
    'info-thin',
    'info-toggle',
    'info-toolbutton',
    'inverse',
    'light',
    'light-ghost',
    'light-inverse',
    'light-link',
    'light-outline',
    'light-outline-toolbutton',
    'light-round',
    'light-round-toggle',
    'light-square-toggle',
    'light-striped',
    'light-thin',
    'light-toggle',
    'light-toolbutton',
    'link',
    'neutral',
    'neutral-ghost',
    'neutral-link',
    'neutral-outline',
    'neutral-outline-toolbutton',
    'neutral-toolbutton',
    'outline',
    'outline-toolbutton',
    'primary',
    'primary-ghost',
    'primary-inverse',
    'primary-link',
    'primary-outline',
    'primary-outline-toolbutton',
    'primary-round',
    'primary-round-toggle',
    'primary-square-toggle',
    'primary-striped',
    'primary-thin',
    'primary-toggle',
    'primary-toolbutton',
    'round',
    'round-toggle',
    'secondary',
    'secondary-ghost',
    'secondary-inverse',
    'secondary-link',
    'secondary-outline',
    'secondary-outline-toolbutton',
    'secondary-round',
    'secondary-round-toggle',
    'secondary-square-toggle',
    'secondary-striped',
    'secondary-thin',
    'secondary-toggle',
    'secondary-toolbutton',
    'square-toggle',
    'striped',
    'success',
    'success-ghost',
    'success-inverse',
    'success-link',
    'success-outline',
    'success-outline-toolbutton',
    'success-round',
    'success-round-toggle',
    'success-square-toggle',
    'success-striped',
    'success-thin',
    'success-toggle',
    'success-toolbutton',
    'thin',
    'toggle',
    'toolbutton',
    'warning',
    'warning-ghost',
    'warning-inverse',
    'warning-link',
    'warning-outline',
    'warning-outline-toolbutton',
    'warning-round',
    'warning-round-toggle',
    'warning-square-toggle',
    'warning-striped',
    'warning-thin',
    'warning-toggle',
    'warning-toolbutton',
]

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
DEFAULT_THEME: Final[str] = "bootstrap-light"

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
NEUTRAL: Final[BootColor] = "neutral"

OUTLINE: Final[BootType] = "outline"
LINK: Final[BootType] = "link"
GHOST: Final[BootType] = "ghost"
INVERSE: Final[BootType] = "inverse"
STRIPED: Final[BootType] = "striped"
THIN: Final[BootType] = "thin"
SQUARE: Final[BootType] = "square"
# ROUND ("round") is a valid BootType too, but the constant is already defined
# above for LineCap/LineJoin with the same value -- reuse it; do not redefine.
# Base-types (families), not modifiers -- see BootBase.
TOGGLE: Final[BootBase] = "toggle"
TOOLBUTTON: Final[BootBase] = "toolbutton"

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
    "MeterMode", "ProgressMode", "BootColor", "BootType", "BootBase", "BootStyle",
    "TreeviewDisplay",
    # bootstyle vocabulary (single source of truth)
    "BOOTSTYLE_COLORS", "BOOTSTYLE_MODIFIERS", "BOOTSTYLE_INTERNAL_MODIFIERS",
    "BOOTSTYLE_BASES", "BOOTSTYLE_FAMILIES", "BOOTSTYLE_ORIENTS", "NEUTRAL_FAMILIES",
    "BOOTSTYLE_SURFACES", "DEFAULT_SURFACE",
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
    "NEUTRAL",
    "OUTLINE", "LINK", "GHOST", "TOGGLE", "INVERSE", "STRIPED", "THIN", "TOOLBUTTON", "SQUARE",
    "TREE", "HEADINGS", "TREEHEADINGS",
]
