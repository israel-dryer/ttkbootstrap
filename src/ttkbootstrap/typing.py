from typing import Literal, TypedDict, Callable
from tkinter import Variable

from PIL.ImageTk import PhotoImage

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack

StyleColor = Literal['primary', 'secondary', 'success', 'info', 'warning', 'danger', 'light', 'dark']
ButtonStyleVariant = Literal['default', 'outline', 'link']


class ButtonOptions(TypedDict, total=False):
    text: str
    textvariable: str | Variable
    underline: int
    image: str | PhotoImage
    compound: Literal["top", "bottom", "left", "right", "center", "none"]
    state: Literal["normal", "active", "disabled"]
    takefocus: bool
    command: Callable[[], None]
    style: str
    width: int
    cursor: str
    padding: int | str | tuple
    anchor: Literal["n", "ne", "e", "se", "s", "sw", "w", "nw", "center"]
