from tkinter import Misc
from tkinter.ttk import Scrollbar as ttkScrollbar
from typing import Any, Callable, Literal, Optional, Tuple

from ..mixins import BaseMixin, OrientMixin, StyleMixin
from ...ttk_types import StyleColor
from ...utils import keys_to_lower


class Scrollbar(
    StyleMixin,
    BaseMixin,
    OrientMixin,
):

    def __init__(
        self,
        master: Misc | None = None,
        color: StyleColor = "default",
        variant: Literal['default', 'square'] = 'default',
        orient: Literal["vertical", "horizontal"] = "vertical",
        on_scroll: Optional[Callable[[str, float], Any]] = None,
        **kwargs,
    ):
        self._kwargs = dict(kwargs)
        self._master = master
        self._color = color
        self._variant = variant
        self._orient = orient
        self._extras = {"orient": orient}
        self._on_scroll = on_scroll
        self._widget: "ttkScrollbar"
        self._render_widget()

    def _render_widget(self):
        """Create and initialize the internal ttk widget."""
        self._widget: "ttkScrollbar" = ttkScrollbar(
            self._master, command=self._on_scroll, **keys_to_lower(self._kwargs))

        self._initialize_style(
            'scrollbar',
            color=self._color,
            variant=self._variant,
            extras=self._extras,
            **self._kwargs
        )

    @property
    def on_scroll(self):
        return self._on_scroll

    @on_scroll.setter
    def on_scroll(self, value: Callable[[str, int], Any]):
        self._on_scroll = value
        self.widget.configure(command=self._on_scroll)

    def get(self) -> Tuple[float, float]:
        """Returns the scrollbar settings whose elements are the arguments to the most recent set command"""
        return self.widget.get()

    def set(self, first: float, last: float):
        """
        Specifies the visible range to be displayed. `first` and `last` are real fractions between 0 and 1;
        normally invoked by the widget's `scroll_x` or `scroll_y` method
        """
        self.widget.set(first, last)
