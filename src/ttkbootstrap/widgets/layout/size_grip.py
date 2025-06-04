from tkinter import Misc
from tkinter.ttk import Sizegrip as ttkSizegrip

from ..mixins import BackgroundMixin, BaseMixin, StyleMixin
from ...ttk_types import StyleColor as Color
from ...utils import keys_to_lower


class SizeGrip(
    StyleMixin,
    BaseMixin,
    BackgroundMixin
):

    def __init__(
        self,
        master: Misc | None = None,
        color: Color = "default",
        **kwargs,
    ):
        self._kwargs = dict(kwargs)
        self._master = master
        self._color = color
        self._variant = "default"
        self._extras = {}
        self._widget: "ttkSizegrip"
        self._render_widget()

    def _render_widget(self):
        """Create and initialize the internal ttk widget."""
        self._widget: "ttkSizegrip" = ttkSizegrip(self._master, **keys_to_lower(self._kwargs))

        self._initialize_style(
            'sizegrip',
            color=self._color,
            variant=self._variant,
            extras=self._extras,
            **self._kwargs
        )
