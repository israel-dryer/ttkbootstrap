from tkinter import Misc
from tkinter.ttk import Checkbutton as ttkCheckbutton

from ttkbootstrap.ttk_types import (
    StyleColor as Color
)
from ttkbootstrap.style.styled_widget import StyledWidget
from ttkbootstrap.widgets.mixins import IconMixin

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


class CheckbuttonToggle(IconMixin, StyledWidget, ttkCheckbutton):

    def __init__(
            self,
            master: Misc = None,
            icon: str = None,
            size: int = 24,
            color: Color = "primary",
            **kwargs,
    ):
        self._color = color
        self._variant = "default"  # Checkbutton does not support style variants
        self._icon_name = icon
        self._icon_size = size

        self.init_icon_support(kwargs, default_compound="left")

        super().__init__(master, **kwargs)

        self.bind_icon_hover_events()
        self.bind_theme_change_event()
        self._init_style('checkbutton.toggle', color=color, variant=self._variant, **kwargs)
