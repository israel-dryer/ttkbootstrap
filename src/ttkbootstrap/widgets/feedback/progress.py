from tkinter import DoubleVar, Misc
from tkinter.ttk import Progressbar as ttkProgressbar
from typing import Literal

from ..mixins import (
    BaseMixin, EnabledMixIn, LengthMixin, OrientMixin,
    StyleMixin, VariableMixin
)
from ...ttk_types import StyleColor
from ...utils import keys_to_lower


class Progress(
    BaseMixin,
    StyleMixin,
    LengthMixin,
    OrientMixin,
    VariableMixin,
    EnabledMixIn
):

    def __init__(
        self,
        master: Misc = None,
        color: StyleColor = "default",
        orient: Literal['horizontal', 'vertical'] = "horizontal",
        variant: Literal['default', 'striped'] = "default",
        value: float = 0,
        **kwargs
    ):
        self._kwargs = dict(kwargs)
        self._master = master
        self._color = color
        self._variant = variant
        self._orient = orient
        self._extras = {"orient": orient}
        self._widget: "ttkProgressbar"
        self._variable = DoubleVar(master, value)
        self._render_widget()

    def _render_widget(self):
        """Create and initialize the internal ttk.Button widget."""
        self._widget: "ttkProgressbar" = ttkProgressbar(
            self._master,
            variable=self._variable,
            **keys_to_lower(self._kwargs)
        )
        self._initialize_style(
            'progress',
            color=self._color,
            variant=self._variant,
            extras=self._extras,
            **self._kwargs
        )

    @property
    def mode(self):
        """One of determinate or indeterminate."""
        return self.widget.cget('mode')

    @mode.setter
    def mode(self, value: Literal['determinate', 'indeterminate']):
        self.widget.configure(mode=value)

    @property
    def maximum(self):
        """A floating point number specifying the maximum; default = 100"""
        return self.widget.cget('maximum')

    @maximum.setter
    def maximum(self, value: float):
        self.widget.configure(maximum=value)

    def start(self, interval: float = 50):
        """Begin autoincrement mode: schedules a recurring timer event that calls step every interval milliseconds.
        If omitted, interval defaults to 50 milliseconds (20 steps/second)."""
        self.widget.start(interval)

    def stop(self):
        """Stop autoincrement mode: cancels any recurring timer event initiated by `start()`."""
        self.widget.stop()

    def step(self, amount: float = 1.0):
        """Increments the `value` by amount. `amount` defaults to 1.0 if omitted."""
        self.widget.step(amount)
