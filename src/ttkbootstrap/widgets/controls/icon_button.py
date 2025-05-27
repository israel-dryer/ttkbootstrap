from tkinter import Misc
from tkinter.ttk import Button as ttkButton

from ...style.styled_widget import StyledWidget
from ..mixins import BackgroundInheritMixin, IconMixin
from ...ttk_types import StyleColor, ButtonStyleVariant

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


class IconButton(BackgroundInheritMixin, IconMixin, StyledWidget, ttkButton):
    def __init__(
        self,
        master: Misc = None,
        icon: str = None,
        size: int = 24,
        color: StyleColor = "default",
        variant: ButtonStyleVariant = "default",
        **kwargs,
    ):
        self._icon_name = icon
        self._icon_size = size
        self._color = color
        self._variant = variant
        self._extras = {}

        super().__init__(master, **kwargs)
        self._init_style("icon.button", color=color, variant=variant, extras=self._extras, **kwargs)
