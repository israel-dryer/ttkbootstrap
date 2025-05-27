from tkinter import Misc
from tkinter.ttk import Frame as ttkFrame

from ...ttk_types import StyleColor
from ...style.styled_widget import StyledWidget

try:
    from typing import Literal, Unpack
except ImportError:
    from typing_extensions import Unpack


class Frame(StyledWidget, ttkFrame):

    def __init__(
        self,
        master: Misc = None,
        color: StyleColor = "default",
        variant: Literal['default', 'round'] = "default",
        transparency=False,
        **kwargs,
    ):
        self._color = color
        self._variant = variant
        self._transparency = transparency
        self._extras = {"transparency": self._transparency}
        super().__init__(master, **kwargs)
        self._init_style('frame', color=color, variant=self._variant, extras=self._extras, **kwargs)
