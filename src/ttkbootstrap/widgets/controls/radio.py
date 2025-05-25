from tkinter import Misc
from tkinter.ttk import Radiobutton as ttkRadiobutton

from ...ttk_types import StyleColor
from ...style.styled_widget import StyledWidget

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


class Radiobutton(StyledWidget, ttkRadiobutton):

    def __init__(
        self,
        master: Misc = None,
        color: StyleColor = "primary",
        **kwargs
    ):
        self._color = color
        self._variant = "default"
        super().__init__(master, **kwargs)
        self._init_style('radiobutton', color=color, variant=self._variant, **kwargs)
