from tkinter import Misc
from tkinter.ttk import Frame as ttkFrame

from ttkbootstrap.ttk_types import (
    StyleColor as Color
)
from ttkbootstrap.style.styled_widget import StyledWidget

try:
    from typing import Literal, Unpack
except ImportError:
    from typing_extensions import Unpack


class Frame(StyledWidget, ttkFrame):

    def __init__(
            self,
            master: Misc = None,
            color: Color = "default",
            variant: Literal['default', 'round'] = "default",
            **kwargs,
    ):
        self._color = color
        self._variant = variant
        super().__init__(master, **kwargs)
        self._init_style('frame', color=color, variant=self._variant, **kwargs)
