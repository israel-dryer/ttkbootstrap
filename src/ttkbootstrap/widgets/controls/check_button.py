from tkinter import IntVar, Misc, StringVar
from tkinter.ttk import Checkbutton as ttkCheckButton
from typing import Callable, Literal, Optional, Tuple, Union

from ttkbootstrap.ttk_types import StyleColor
from ttkbootstrap.utils import keys_to_lower
from ttkbootstrap.widgets.mixins import (
    AnchorMixin, BackgroundMixin, BaseMixin, StyleMixin,
    EnabledMixIn, OnChangeMixin, OnOffValueMixin, PaddingMixin,
    TextVariableMixin, VariableMixin, WidthMixin
)


class CheckButton(
    StyleMixin,
    BaseMixin,
    AnchorMixin,
    VariableMixin,
    TextVariableMixin,
    EnabledMixIn,
    OnChangeMixin,
    WidthMixin,
    PaddingMixin,
    OnOffValueMixin,
    BackgroundMixin
):
    def __init__(
        self,
        master: Optional[Misc] = None,
        text: Optional[str] = None,
        value: Optional[Literal[-1, 0, 1]] = -1,
        icon: Optional[Union[str, Tuple[str, int]]] = None,
        color: StyleColor = "default",
        on_change: Optional[Callable] = None,
        **kwargs
    ):
        kw = dict(kwargs)
        self._master = master
        self._icon = icon
        self._color = color
        self._on_change = on_change
        self._kwargs = kw
        self._extras = {}
        self._inherit_background = kw.pop('inherit_background', False)
        self._text_variable = StringVar(master, text)
        self._variable = IntVar(master, value)
        self._widget: Misc
        self._render_widget()

    def _render_widget(self):
        """Create and initialize the internal checkbutton widget"""
        self._widget = ttkCheckButton(
            self._master,
            textvariable=self._text_variable,
            variable=self._variable,
            **keys_to_lower(self._kwargs)
        )
        self._initialize_style(
            'checkbutton',
            color=self._color,
            extras=self._extras,
            **self._kwargs
        )
        if self._on_change:
            self.on_change = self._on_change
