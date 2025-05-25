from tkinter import Misc
from tkinter.ttk import Scrollbar as ttkScrollbar

from ...style.styled_widget import StyledWidget
from ...ttk_types import StyleColor, ScrollbarOptions

try:
    from typing import Unpack, Literal
except ImportError:
    from typing_extensions import Unpack, Literal


class Scrollbar(StyledWidget, ttkScrollbar):

    def __init__(
        self,
        master: Misc | None = None,
        color: StyleColor = "default",
        variant: Literal['default', 'round'] = 'default',
        orient: Literal["vertical", "horizontal"] = "vertical",
        **kwargs: Unpack[ScrollbarOptions],
    ):
        self._color = color
        self._variant = variant
        self._orient = orient

        super().__init__(master, orient=orient, **kwargs)

        self._init_style(
            "scrollbar",
            color=self._color,
            variant=self._variant,
            orient=self._orient,
            **kwargs
        )
