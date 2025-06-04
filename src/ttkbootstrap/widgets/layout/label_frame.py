from tkinter import Misc
from tkinter.ttk import LabelFrame as ttkLabelFrame
from typing import Literal

from ..mixins import BackgroundMixin, BaseMixin, HeightMixin, PaddingMixin, StyleMixin, TextVariableMixin, WidthMixin
from ...ttk_types import StyleColor
from ...utils import keys_to_lower


# TODO can I use a fancy new label with icon to create a nice label?

class LabelFrame(
    StyleMixin,
    BaseMixin,
    PaddingMixin,
    HeightMixin,
    WidthMixin,
    BackgroundMixin,
):

    def __init__(
        self,
        master: Misc = None,
        text: str = None,
        color: StyleColor = "default",
        variant: Literal['default', 'dashed'] = "default",
        **kwargs,
    ):
        kw = dict(kwargs)
        self._master = master
        self._kwargs = kw
        self._text = text
        self._color = color
        self._variant = variant
        self._extras = {}
        self._inherit_background = kw.pop('inherit_background', False)
        self._widget: "ttkLabelFrame"
        self._render_widget()

    def _render_widget(self):
        """Create and initialize the internal ttk widget."""
        self._widget: "ttkLabelFrame" = ttkLabelFrame(self._master, text=self._text, **keys_to_lower(self._kwargs))

        self._initialize_style(
            'labelframe',
            color=self._color,
            variant=self._variant,
            extras=self._extras,
            **self._kwargs
        )

    @property
    def label_anchor(self):
        """Specifies where to place the label."""
        return self.widget.cget('labelanchor')

    @label_anchor.setter
    def label_anchor(self, value: str):
        self.widget.configure(labelanchor=value)

    @property
    def label_widget(self):
        """The widget to use for the label."""
        return self.widget.cget('labelwidget')

    @label_widget.setter
    def label_widget(self, value: Misc):
        self.widget.configure(labelwidget=value)
