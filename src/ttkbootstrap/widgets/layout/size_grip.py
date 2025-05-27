from tkinter import Misc
from tkinter.ttk import Sizegrip as ttkSizegrip

from ..mixins import BackgroundInheritMixin
from ...ttk_types import StyleColor as Color
from ...style.styled_widget import StyledWidget

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


class Sizegrip(BackgroundInheritMixin, StyledWidget, ttkSizegrip):

    def __init__(
        self,
        master: Misc | None = None,
        color: Color = "default",
        **kwargs,
    ):
        self._color = color
        self._variant = "default"
        self._extras = {}
        super().__init__(master, **kwargs)
        self._init_style('sizegrip', color=color, variant="default", extras=self._extras, **kwargs)
