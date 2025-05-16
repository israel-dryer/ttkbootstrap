from typing import Literal, TypedDict, Callable
from tkinter import Variable

from PIL.ImageTk import PhotoImage

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack

StyleColor = Literal['primary', 'secondary', 'success', 'info', 'warning', 'danger', 'light', 'dark']
ButtonStyleVariant = Literal['default', 'outline', 'link']
SwitchVariant = Literal["round", "square"]
ToolbuttonVariant = Literal["default", "outline"]


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


class CheckbuttonOptions(TypedDict, total=False):
    text: str
    textvariable: str
    underline: int
    image: str
    compound: Literal["top", "bottom", "left", "right", "center", "none"]
    state: Literal["normal", "active", "disabled"]
    takefocus: bool | str
    variable: str  # Usually a tk.BooleanVar or tk.IntVar; str used for TypedDict compatibility
    onvalue: str | int
    offvalue: str | int
    command: Callable[[], None]
    style: str
    width: int
    cursor: str
    padding: int | str | tuple
    anchor: Literal["n", "ne", "e", "se", "s", "sw", "w", "nw", "center"]


class ComboboxOptions(TypedDict, total=False):
    textvariable: str
    values: list[str]
    state: Literal["normal", "readonly", "disabled"]
    postcommand: Callable[[], None]
    height: int
    justify: Literal["left", "center", "right"]
    exportselection: bool
    width: int
    style: str
    takefocus: bool | str
    cursor: str
