from tkinter import Misc
from tkinter.ttk import Label as ttkLabel

from ..mixins import BackgroundInheritMixin
from ...ttk_types import StyleColor
from ...style.styled_widget import StyledWidget

try:
    from typing import Literal, Unpack
except ImportError:
    from typing_extensions import Unpack


class Badge(BackgroundInheritMixin, StyledWidget, ttkLabel):
    def __init__(
        self,
        master: Misc = None,
        color: StyleColor = "default",
        variant: Literal['default', 'pill', 'circle'] = "default",
        **kwargs,
    ):
        self._color = color
        self._variant = variant
        self._extras = {}

        super().__init__(master, **kwargs)
        self._init_style("badge", color=color, variant=variant, extras=self._extras, **kwargs)
