from tkinter.ttk import Frame as ttkFrame
from tkinter import Misc

from ..mixins import BackgroundMixin, BaseMixin, HeightMixin, PaddingMixin, StyleMixin, WidthMixin
from ...ttk_types import StyleColor
from ...utils import keys_to_lower

try:
    from typing import Literal, Optional, Tuple, TypedDict, Union, Unpack
except ImportError:
    from typing_extensions import Unpack


class Frame(StyleMixin, BaseMixin, BackgroundMixin, PaddingMixin, WidthMixin, HeightMixin):

    def __init__(
        self,
        master: Misc = None,
        color: StyleColor = "default",
        variant: Literal['default', 'round'] = "default",
        **kwargs,
    ):
        kw = dict(kwargs)
        self._color = color
        self._variant = variant
        self._extras = {}
        self._master = master
        self._color = color
        self._variant = variant
        self._kwargs = kw
        self._extras = {}
        self._inherit_background = kw.pop('inherit_background', False)
        self._widget: "ttkFrame"
        self._render_widget()

    def _render_widget(self):
        """Create and initialize the internal ttk widget."""
        self._widget: "ttkFrame" = ttkFrame(self._master, **keys_to_lower(self._kwargs))

        self._initialize_style(
            'frame',
            color=self._color,
            variant=self._variant,
            extras=self._extras,
            **self._kwargs
        )
