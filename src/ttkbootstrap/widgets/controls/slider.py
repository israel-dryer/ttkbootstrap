from tkinter import Misc
from tkinter.ttk import Scale as ttkScale

from ..mixins import BackgroundInheritMixin
from ...ttk_types import StyleColor
from ...style.styled_widget import StyledWidget

try:
    from typing import Literal, Unpack
except ImportError:
    from typing_extensions import Unpack


class Slider(BackgroundInheritMixin, StyledWidget, ttkScale):

    def __init__(
        self,
        master: Misc = None,
        color: StyleColor = "default",
        orient: Literal['horizontal', 'vertical'] = "horizontal",
        **kwargs
    ):
        self._color = color
        self._variant = "default"
        self._orient = orient
        self._extras = {"orient": orient}
        super().__init__(master, **kwargs, orient=orient)
        self._init_style('slider', color=color, variant=self._variant, extras=self._extras, **kwargs)
