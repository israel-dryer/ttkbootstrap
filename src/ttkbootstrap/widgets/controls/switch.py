from tkinter import Misc
from tkinter.ttk import Checkbutton as ttkCheckbutton

from ...ttk_types import CheckbuttonOptions, StyleColor
from ...style.styled_widget import StyledWidget

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


class Switch(StyledWidget, ttkCheckbutton):

    def __init__(
        self,
        master: Misc = None,
        color: StyleColor = "primary",
        **kwargs: Unpack[CheckbuttonOptions],
    ):
        self._color = color
        self._variant = "default"
        super().__init__(master, **kwargs)
        self._init_style('switch', color=color, variant=self._variant, **kwargs)
