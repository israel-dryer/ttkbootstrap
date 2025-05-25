from tkinter import Misc
from tkinter.ttk import Checkbutton as ttkCheckbutton

from ttkbootstrap.ttk_types import (
    StyleColor as Color, CheckbuttonOptions as CbOpts
)
from ttkbootstrap.style.styled_widget import StyledWidget

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


class Switch(StyledWidget, ttkCheckbutton):

    def __init__(
            self,
            master: Misc = None,
            color: Color = "primary",
            **kwargs: Unpack[CbOpts],
    ):
        self._color = color
        self._variant = "default"
        super().__init__(master, **kwargs)
        self._init_style('switch', color=color, variant=self._variant, **kwargs)
