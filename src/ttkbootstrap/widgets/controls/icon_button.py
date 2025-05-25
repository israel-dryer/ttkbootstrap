from tkinter import Misc
from tkinter.ttk import Button as ttkButton

from ttkbootstrap.style.styled_widget import StyledWidget
from ttkbootstrap.widgets.mixins import IconMixin
from ttkbootstrap.ttk_types import (
    StyleColor,
    ButtonStyleVariant as Variant,
    ButtonOptions as BtnOpts,
)

try:
    from typing import Unpack
except ImportError:
    from typing_extensions import Unpack


class IconButton(IconMixin, StyledWidget, ttkButton):
    def __init__(
        self,
        master: Misc = None,
        icon: str = None,
        size: int = 24,
        color: StyleColor = "default",
        variant: Variant = "default",
        **kwargs: Unpack[BtnOpts],
    ):
        self._icon_name = icon
        self._icon_size = size
        self._color = color
        self._variant = variant

        # Inject icon and compound into kwargs before init
        self.init_icon_support(kwargs, default_compound="image")

        super().__init__(master, **kwargs)

        self.bind_icon_hover_events()
        self.bind_theme_change_event()
        self._init_style("icon.button", color=color, variant=variant, **kwargs)

