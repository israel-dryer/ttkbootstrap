from tkinter import Misc
from tkinter.ttk import Progressbar as ttkProgressbar

from ...ttk_types import StyleColor
from ...style.styled_widget import StyledWidget

try:
    from typing import Literal, Unpack
except ImportError:
    from typing_extensions import Unpack


class Progress(StyledWidget, ttkProgressbar):

    def __init__(
        self,
        master: Misc = None,
        color: StyleColor = "default",
        orient: Literal['horizontal', 'vertical'] = "horizontal",
        variant: Literal['default', 'striped'] = "default",
        **kwargs
    ):
        self._color = color
        self._variant = variant
        self._orient = orient
        super().__init__(master, **kwargs, orient=orient)
        self._init_style('progress', color=color, variant=self._variant, **kwargs, extras={"orient": orient})
