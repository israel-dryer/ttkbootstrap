from tkinter import Misc
from tkinter.ttk import Sizegrip as ttkSizegrip

from ...ttk_types import StyleColor as Color
from ...ttk_types import SizegripOptions as GripOpts
from ...style.styled_widget import StyledWidget

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


class Sizegrip(StyledWidget, ttkSizegrip):

    def __init__(
        self,
        master: Misc | None = None,
        color: Color = "default",
        **kwargs: Unpack[GripOpts],
    ):
        self._color = color
        self._variant = "default"
        super().__init__(master, **kwargs)
        self._init_style('sizegrip', color=color, variant="default")
