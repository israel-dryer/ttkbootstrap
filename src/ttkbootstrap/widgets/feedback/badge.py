from tkinter import Misc, PhotoImage, StringVar
from tkinter.ttk import Label as ttkLabel

from ..mixins import (
    AnchorMixin, BackgroundMixin, BaseMixin, FontMixin,
    ImageMixin, JustifyMixin, PaddingMixin, StyleMixin,
    TextVariableMixin, WidthMixin, WrapLengthMixin
)
from ...ttk_types import StyleColor
from ...utils import keys_to_lower

try:
    from typing import Literal, Optional, Tuple, TypedDict, Union, Unpack
except ImportError:
    from typing_extensions import Unpack


class Badge(
    StyleMixin,
    BaseMixin,
    TextVariableMixin,
    AnchorMixin,
    FontMixin,
    ImageMixin,
    PaddingMixin,
    WidthMixin,
    BackgroundMixin,
    JustifyMixin,
    WrapLengthMixin
):

    def __init__(
        self,
        master: Optional[Misc] = None,
        text: Optional[str] = None,
        color: StyleColor = "default",
        variant: Literal["default", "circle", "pill"] = "default",
        **kwargs
    ):
        kw = dict(kwargs)
        self._master = master
        self._color = color
        self._variant = variant
        self._kwargs = kw
        self._extras = {}
        self._text = text
        self._image: Optional[PhotoImage] = None
        self._inherit_background = kw.pop('inherit_background', False)
        self._variable = StringVar(master, text)
        self._widget: Misc
        self._render_widget()

    def _render_widget(self):
        """Create and initialize the internal ttk widget."""
        self._widget: "ttkLabel" = ttkLabel(
            self._master,
            textvariable=self._variable,
            **keys_to_lower(self._kwargs)
        )

        self._initialize_style(
            'badge',
            color=self._color,
            variant=self._variant,
            extras=self._extras,
            **self._kwargs
        )
