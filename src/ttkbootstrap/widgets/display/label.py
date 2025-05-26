from tkinter import Misc
from tkinter.ttk import Label as ttkLabel

from ..mixins import IconMixin
from ...style.styled_widget import StyledWidget
from ...ttk_types import StyleColor

try:
    from typing import Literal, Unpack
except ImportError:
    from typing_extensions import Unpack


class Label(IconMixin, StyledWidget, ttkLabel):
    def __init__(
        self,
        master: Misc = None,
        text: str = "",
        icon: str = None,
        size: int = 24,
        color: StyleColor = "default",
        variant: Literal['default', 'inverse'] = "default",
        **kwargs,
    ):
        self._icon_name = icon
        self._icon_size = size
        self._color = color
        self._variant = variant

        # Inject icon and compound into kwargs before init
        kwargs['text'] = text
        self._inject_icon_support(kwargs, default_compound="image")
        super().__init__(master, **kwargs)
        self._bind_icon_events()
        self._init_style("label", color=color, variant=variant, **kwargs)
