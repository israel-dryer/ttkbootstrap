from tkinter import Misc
from tkinter.ttk import Button as ttkButton
from ..mixins import IconMixin
from ...ttk_types import StyleColor
from ...style.styled_widget import StyledWidget

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


class Button(IconMixin, StyledWidget, ttkButton):
    def __init__(
        self,
        master: Misc = None,
        icon: str = None,
        size: int = 24,
        color: StyleColor = "default",
        variant: str = "default",
        **kwargs,
    ):
        self._icon_name = icon
        self._icon_size = size
        self._color = color
        self._variant = variant

        self._inject_icon_support(kwargs, default_compound="left")
        super().__init__(master, **kwargs)
        self._bind_icon_events()
        self._init_style("button", color=color, variant=variant, **kwargs)
