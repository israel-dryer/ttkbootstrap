from typing import Literal, TypedDict, Callable, Union
from tkinter import StringVar, IntVar, BooleanVar, DoubleVar, Variable as TkVariable

from PIL.ImageTk import PhotoImage

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack

Variable = Union[StringVar, IntVar, BooleanVar, DoubleVar, TkVariable]
StyleColor = Literal['primary', 'secondary', 'success', 'info', 'warning', 'danger', 'light', 'dark', 'default']
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
    textvariable: str | Variable
    underline: int
    image: str
    compound: Literal["top", "bottom", "left", "right", "center", "none"]
    state: Literal["normal", "active", "disabled"]
    takefocus: bool | str
    variable: str | Variable
    onvalue: str | int
    offvalue: str | int
    command: Callable[[], None]
    style: str
    width: int
    cursor: str
    padding: int | str | tuple
    anchor: Literal["n", "ne", "e", "se", "s", "sw", "w", "nw", "center"]


class ComboboxOptions(TypedDict, total=False):
    textvariable: str | Variable
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


class EntryOptions(TypedDict, total=False):
    textvariable: str | Variable
    show: str
    validate: Literal["none", "focus", "focusin", "focusout", "key", "all"]
    validatecommand: Callable[..., bool]
    invalidcommand: Callable[[], None]
    state: Literal["normal", "readonly", "disabled"]
    exportselection: bool
    font: str
    justify: Literal["left", "center", "right"]
    takefocus: bool | str
    width: int
    style: str
    cursor: str


class FrameOptions(TypedDict, total=False):
    borderwidth: int
    relief: str  # Could refine with Literal["flat", "groove", "raised", "ridge", "solid", "sunken"]
    padding: int | tuple[int, ...] | str
    width: int
    height: int
    style: str
    takefocus: bool | str
    cursor: str


class LabelOptions(TypedDict, total=False):
    text: str
    textvariable: str | Variable
    image: str
    compound: Literal["top", "bottom", "left", "right", "center", "none"]
    anchor: Literal["n", "ne", "e", "se", "s", "sw", "w", "nw", "center"]
    justify: Literal["left", "center", "right"]
    padding: int | tuple[int, ...] | str
    font: str
    width: int
    style: str
    cursor: str
    takefocus: bool | str
    underline: int


class LabelFrameOptions(TypedDict, total=False):
    text: str
    labelanchor: Literal["n", "ne", "e", "se", "s", "sw", "w", "nw", "center"]
    underline: int
    padding: int | str | tuple[int, ...]
    borderwidth: int
    relief: Literal["flat", "raised", "sunken", "ridge", "solid", "groove"]
    width: int
    height: int
    style: str
    takefocus: bool | str
    cursor: str


class NotebookOptions(TypedDict, total=False):
    height: int
    width: int
    padding: int | str | tuple[int, ...]
    style: str
    takefocus: bool | str
    cursor: str


class PanedWindowOptions(TypedDict, total=False):
    orient: Literal["horizontal", "vertical"]
    style: str
    takefocus: bool | str
    cursor: str
    width: int
    height: int


class ProgressbarOptions(TypedDict, total=False):
    orient: Literal["horizontal", "vertical"]
    length: int
    mode: Literal["determinate", "indeterminate"]
    maximum: float
    value: float
    variable: str | Variable
    style: str
    takefocus: bool | str
    cursor: str


class RadiobuttonOptions(TypedDict, total=False):
    text: str
    textvariable: str | Variable
    value: str | int
    variable: str | Variable
    command: Callable[[], None]
    image: str
    compound: Literal["top", "bottom", "left", "right", "center", "none"]
    state: Literal["normal", "active", "disabled"]
    underline: int
    takefocus: bool | str
    width: int
    cursor: str
    style: str
    padding: int | str | tuple


class ScaleOptions(TypedDict, total=False):
    from_: float
    to: float
    orient: Literal["horizontal", "vertical"]
    variable: str | Variable
    value: float
    command: Callable[[str], None]
    length: int
    resolution: float
    state: Literal["normal", "disabled"]
    style: str
    takefocus: bool | str
    cursor: str
