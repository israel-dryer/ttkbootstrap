from tkinter import Misc
from tkinter.ttk import Entry as ttkEntry

from ttkbootstrap.ttk_types import (
    StyleColor,
)
from ttkbootstrap.style.styled_widget import StyledWidget

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


class TextBox(StyledWidget, ttkEntry):

    def __init__(
            self,
            master: Misc = None,
            color: StyleColor = "default",
            **kwargs
    ):
        self._color = color
        self._variant = "default"

        # set a default font if not provided
        if 'font' not in kwargs:
            kwargs['font'] = '-size 12'

        super().__init__(master, **kwargs)
        self._init_style('input', color=color, variant=self._variant, **kwargs)
