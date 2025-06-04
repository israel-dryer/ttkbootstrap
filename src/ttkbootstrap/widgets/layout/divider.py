from tkinter import Misc
from tkinter.ttk import Separator as ttkSeparator
from typing import Literal

from ..mixins import BackgroundMixin, BaseMixin, OrientMixin, StyleMixin
from ...ttk_types import StyleColor
from ...utils import keys_to_lower


class Divider(
    StyleMixin,
    BaseMixin,
    OrientMixin,
    BackgroundMixin,
):

    def __init__(
        self,
        master: Misc = None,
        color: StyleColor = "default",
        variant: Literal['default', 'dashed'] = "default",
        orient: Literal['horizontal', 'vertical'] = "horizontal",
        **kwargs,
    ):
        kw = dict(kwargs)
        self._master = master
        self._kwargs = kw
        self._color = color
        self._variant = variant
        self._orient = orient
        self._extras = {"orient": orient}
        self._inherit_background = kw.pop('inherit_background', False)
        self._widget: "ttkSeparator"
        self._render_widget()

    def _render_widget(self):
        """Create and initialize the internal ttk widget."""
        self._widget: "ttkSeparator" = ttkSeparator(self._master, **keys_to_lower(self._kwargs))

        self._initialize_style(
            'divider',
            color=self._color,
            variant=self._variant,
            extras=self._extras,
            **self._kwargs
        )
