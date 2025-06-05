from tkinter import Misc
from tkinter.ttk import PanedWindow as ttkPanedWindow, Widget
from typing import Any, List, Literal

from ..mixins import BackgroundMixin, BaseMixin, HeightMixin, OrientMixin, StyleMixin, WidthMixin
from ...ttk_types import StyleColor
from ...utils import keys_to_lower


class PanedWindow(
    StyleMixin,
    BaseMixin,
    OrientMixin,
    BackgroundMixin,
    WidthMixin,
    HeightMixin
):

    def __init__(
        self,
        master: Misc = None,
        color: StyleColor = "default",
        orient: Literal['horizontal', 'vertical'] = "vertical",
        width: int = None,
        height: int = None,
        **kwargs,
    ):
        kw = dict(kwargs)
        kw['width'] = width
        kw['height'] = height
        kw['orient'] = orient
        self._kwargs = kw

        self._master = master
        self._color = color
        self._variant = "default"

        self._extras = {"orient": orient}
        self._inherit_background = kw.pop('inherit_background', False)
        self._widget: "ttkPanedWindow"
        self._render_widget()

    def _render_widget(self):
        """Create and initialize the internal ttk widget."""
        self._widget: "ttkPanedWindow" = ttkPanedWindow(self._master, **keys_to_lower(self._kwargs))

        self._initialize_style(
            'panedwindow',
            color=self._color,
            variant=self._variant,
            extras=self._extras,
            **self._kwargs
        )

    def add_pane(self, pane: Any, weight: int = None):
        """Adds a new pane to the window"""
        self._widget.add(pane, weight=weight)

    def remove_pane(self, pane: Any):
        """Removes the specified pane from the window"""
        self._widget.forget(pane)

    def insert_pane(self, position: Any, pane: Any, weight: int = None):
        """Inserts a pane at the specified position. `position` is either the string 'end', an integer index, or the managed subwindow."""
        self._widget.insert(position, pane, weight=weight)

    def update_pane(self, pane: Any, weight: int):
        """Update the specified pane"""
        self._widget.paneconfigure(pane, weight=weight)

    def query_pane(self, pane):
        """Query the specified pane settings"""

    def update_sash(self, index: int, position: int) -> int:
        """Update the specified sash at index; returns new sash position"""
        return self._widget.sashpos(index, position)

    def query_sash(self, index: int):
        """Query the sash settings at `index`"""
        return self._widget.sashpos(index)

    def panes(self) -> List[Any]:
        """Return a list of all panes managed by the window"""
        names = self._widget.panes()
        return [self._widget.nametowidget(name) for name in names]
