from tkinter import Misc, StringVar
from tkinter.ttk import Radiobutton as ttkRadioButton
from typing import Callable, Literal, Optional, Tuple, Union

from ttkbootstrap.ttk_types import StyleColor
from ttkbootstrap.utils import keys_to_lower
from ttkbootstrap.widgets.mixins import (
    BackgroundMixin, BaseMixin, EnabledMixIn, IconMixin,
    ImageMixin, OnChangeMixin, PaddingMixin, StyleMixin,
    TextVariableMixin, VariableMixin, WidthMixin,
)


class RadioButtonToggle(
    StyleMixin,
    BaseMixin,
    TextVariableMixin,
    VariableMixin,
    OnChangeMixin,
    EnabledMixIn,
    WidthMixin,
    ImageMixin,
    PaddingMixin,
    IconMixin,
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
        icon: Optional[Union[str, Tuple[str, int]]] = None,
        variant: Literal['default', 'outline'] = "default",
        on_change: Optional[Callable] = None,
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
        self._icon = icon
        self._text = text
        self._variant = variant + ".tool"
        self._inherit_background = kw.pop('inherit_background', False)
        self._text_variable = StringVar(master, text)
        self._variable = StringVar(master, value if selected else None, group)
        self._widget: "ttkRadioButton"
        self._render_widget()

    def _render_widget(self):
        """Create and initialize the internal RadioButton widget."""
        self._widget: "ttkRadioButton" = ttkRadioButton(
            self._master,
            value=self._value,
            textvariable=self._text_variable,
            variable=self._variable,
            **keys_to_lower(self._kwargs)
        )
        self._bind_icon_events()
        self._prepare_icon_kwargs(default_compound="left")
        self._initialize_style(
            'radiobutton',
            color=self._color,
            extras=self._extras,
            **self._kwargs
        )

        if self._on_change:
            self.on_change = self._on_change
