from tkinter import Misc, StringVar
from tkinter.ttk import Radiobutton as ttkRadioButton
from typing import Any, Callable, Optional, Union

from ttkbootstrap.ttk_types import StyleColor
from ttkbootstrap.utils import keys_to_lower
from ttkbootstrap.widgets.mixins import (
    BackgroundMixin,
    BaseMixin,
    EnabledMixIn, StyleMixin, TextVariableMixin, VariableMixin, WidthMixin,
)


class RadioButton(
    StyleMixin,
    BaseMixin,
    TextVariableMixin,
    VariableMixin,
    EnabledMixIn,
    WidthMixin,
    BackgroundMixin
):
    def __init__(
        self,
        master: Optional[Misc] = None,
        text: Optional[str] = None,
        value: Optional[Union[str, int]] = None,
        selected: bool = False,
        group: Optional[str] = None,
        color: StyleColor = "default",
        on_change: Optional[Callable[[int], Any]] = None,
        **kwargs
    ):
        kw = dict(kwargs)
        self._master = master
        self._group = group
        self._color = color
        self._on_change = on_change
        self._kwargs = kw
        self._extras = {}
        self._value = value
        self._inherit_background = kw.pop('inherit_background', False)
        self._text_variable = StringVar(master, text)
        self._variable = StringVar(master, value if selected else None, group)
        self._widget: Misc
        self._render_widget()

    def _render_widget(self):
        """Create and initialize the internal ttk.Radiobutton widget."""
        self._widget = ttkRadioButton(
            self._master,
            value=self._value,
            textvariable=self._text_variable,
            variable=self._variable,
            **keys_to_lower(self._kwargs)
        )

        self._initialize_style(
            'radiobutton',
            color=self._color,
            extras=self._extras,
            **self._kwargs
        )

        if self._on_change:
            func = self._on_change
            self.on_change = func
