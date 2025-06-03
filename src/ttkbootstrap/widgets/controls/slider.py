from tkinter import DoubleVar, Misc
from tkinter.ttk import Scale as ttkScale
from typing import Callable, Literal, Optional

from ttkbootstrap.ttk_types import StyleColor
from ttkbootstrap.utils import keys_to_lower
from ttkbootstrap.widgets.mixins import (
    BackgroundMixin, BaseMixin, MinMaxMixin, OnChangeMixin,
    OrientMixin, StyleMixin, VariableMixin,
)


class Slider(
    StyleMixin,
    BaseMixin,
    VariableMixin,
    OrientMixin,
    OnChangeMixin,
    MinMaxMixin,
    BackgroundMixin
):

    def __init__(
        self,
        master: Optional[Misc] = None,
        value=0.0,
        min_value=0.0,
        max_value=100.0,
        precision=2,
        orient: Literal['horizontal', 'vertical'] = "horizontal",
        color: StyleColor = "default",
        on_change: Optional[Callable] = None,
        **kwargs
    ):
        kw = dict(kwargs)
        self._master = master
        self._color = color
        self._orient = orient
        self._on_change = on_change
        self._kwargs = kw
        self._extras = {"orient": orient}
        self._min_value = min_value
        self._max_value = max_value
        self._precision = precision
        self._inherit_background = kw.pop('inherit_background', False)
        self._variable = DoubleVar(master, value)
        self._widget: Misc
        self._prev_value = value
        self._render_widget()

    def _render_widget(self):
        """Create and initialize the internal ttk widget."""
        self._widget: ttkScale = ttkScale(
            self._master,
            from_=self._min_value,
            to=self._max_value,
            variable=self._variable,
            orient=self._orient,
            **keys_to_lower(self._kwargs)
        )

        self._initialize_style(
            'slider',
            color=self._color,
            extras=self._extras,
            **self._kwargs
        )

        if self._on_change:
            self.on_change = self._on_change
