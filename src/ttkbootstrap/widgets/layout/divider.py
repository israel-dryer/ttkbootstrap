from tkinter import Misc
from tkinter.ttk import Separator as ttkSeparator

from ...ttk_types import StyleColor
from ...style.styled_widget import StyledWidget

try:
    from typing import Literal, Unpack
except ImportError:
    from typing_extensions import Unpack


class Divider(StyledWidget, ttkSeparator):

    def __init__(
        self,
        master: Misc = None,
        color: StyleColor = "default",
        variant: Literal['default', 'dashed'] = "default",
        orient: Literal['horizontal', 'vertical'] = "horizontal",
        **kwargs,
    ):
        self._color = color
        self._variant = variant
        super().__init__(master, **kwargs)
        self._init_style('separator', color=color, variant=self._variant, **kwargs, extras={"orient": orient})
