from tkinter.constants import (
    ACTIVE,
    ANCHOR,
    BOTTOM,
    CENTER,
    DISABLED,
    E,
    END,
    FIRST,
    HORIZONTAL,
    INSERT,
    LAST,
    LEFT,
    N,
    NE,
    NONE,
    NORMAL,
    NS,
    NSEW,
    NW,
    RIGHT,
    S,
    SE,
    SW,
    TOP,
    VERTICAL,
    W,
    X,
    Y,
)

DEFAULT = 'default'
DEFAULT_THEME = 'litera'
TTK_CLAM = 'clam'
TTK_ALT = 'alt'
TTK_DEFAULT = 'default'

# meter constants
FULL = 'full'
SEMI = 'semi'

# progressbar constant
DETERMINATE = 'determinate'
INDETERMINATE = 'indeterminate'

# bootstyle colors
PRIMARY = 'primary'
SECONDARY = 'secondary'
SUCCESS = 'success'
DANGER = 'danger'
WARNING = 'warning'
INFO = 'info'
LIGHT = 'light'
DARK = 'dark'

# bootstyle types
OUTLINE = 'outline'
LINK = 'link'
TOGGLE = 'toggle'
INVERSE = 'inverse'
STRIPED = 'striped'
TOOLBUTTON = 'toolbutton'
ROUND = 'round'
SQUARE = 'square'

# treeview constants
TREE = 'tree'
HEADINGS = 'headings'
TREEHEADINGS = 'tree headings'

# state constants
READONLY = 'readonly'

__all__ = [
    # tkinter.constants
    "ACTIVE", "ANCHOR", "BOTTOM", "CENTER", "DISABLED", "E", "END", "FIRST", "HORIZONTAL",
    "INSERT", "LAST", "LEFT", "N", "NE", "NONE", "NORMAL", "NS", "NSEW", "NW", "RIGHT",
    "S", "SE", "SW", "TOP", "VERTICAL", "W", "X", "Y",

    # themes
    "DEFAULT", "DEFAULT_THEME", "TTK_CLAM", "TTK_ALT", "TTK_DEFAULT",

    # meter
    "FULL", "SEMI",

    # progressbar
    "DETERMINATE", "INDETERMINATE",

    # bootstyle colors
    "PRIMARY", "SECONDARY", "SUCCESS", "DANGER", "WARNING", "INFO", "LIGHT", "DARK",

    # bootstyle types
    "OUTLINE", "LINK", "TOGGLE", "INVERSE", "STRIPED", "TOOLBUTTON", "ROUND", "SQUARE",

    # treeview
    "TREE", "HEADINGS", "TREEHEADINGS",

    # states
    "READONLY",
]
