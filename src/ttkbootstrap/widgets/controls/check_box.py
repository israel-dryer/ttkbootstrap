from tkinter import Misc
from tkinter.ttk import Checkbutton as ttkCheckbutton

from ...ttk_types import StyleColor
from ...style.styled_widget import StyledWidget

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


class CheckBox(StyledWidget, ttkCheckbutton):

    def __init__(
        self,
        master: Misc = None,
        color: StyleColor = "primary",
        **kwargs,
    ):
        self._color = color
        self._variant = "default"  # Checkbutton does not support style variants
        super().__init__(master, **kwargs)
        self._init_style('checkbutton', color=color, variant=self._variant, **kwargs)
