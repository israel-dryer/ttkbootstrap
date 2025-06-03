from tkinter import IntVar, Misc, PhotoImage, StringVar
from tkinter.ttk import Checkbutton as ttkCheckButton
from typing import Any, Callable, Literal, Optional, Tuple, Union

from ttkbootstrap.ttk_types import StyleColor
from ttkbootstrap.utils import keys_to_lower
from ttkbootstrap.widgets.mixins import (
    BackgroundMixin, BaseMixin, EnabledMixIn, IconMixin,
    ImageMixin, OnChangeMixin, OnOffValueMixin, PaddingMixin,
    StyleMixin, TextVariableMixin, VariableMixin, WidthMixin,
)


class CheckButtonToggle(
    StyleMixin,
    BaseMixin,
    TextVariableMixin,
    VariableMixin,
    OnChangeMixin,
    EnabledMixIn,
    WidthMixin,
    ImageMixin,
    PaddingMixin,
    OnOffValueMixin,
    IconMixin,
    BackgroundMixin
):
    """
    A themed toggle-style checkbutton widget
    """

    def __init__(
        self,
        master: Optional[Misc] = None,
        text: Optional[str] = None,
        value: Optional[Literal[-1, 0, 1]] = -1,
        color: StyleColor = "primary",
        icon: Optional[Union[str, Tuple[str, int]]] = None,
        variant: Literal['default', 'outline'] = "default",
        on_change: Optional[Callable[[int], Any]] = None,
        **kwargs
    ):
        self._master = master
        self._icon = icon
        self._color = color
        self._on_change = on_change
        self._kwargs = dict(kwargs)
        self._extras = {}
        self._image: Optional[PhotoImage] = None
        self._variant = variant + ".tool"
        self._inherit_background = self._kwargs.pop('inherit_background', False)
        self._text_variable = StringVar(master, text)
        self._variable = IntVar(master, value)
        self._widget: Misc
        self._render_widget()

    def _render_widget(self):
        """Create and initialize the internal checkbutton widget"""
        self._widget: "ttkCheckButton" = ttkCheckButton(
            self._master,
            textvariable=self._text_variable,
            variable=self._variable,
            **keys_to_lower(self._kwargs)
        )
        self._bind_icon_events()
        self._prepare_icon_kwargs(default_compound="left")
        self._initialize_style(
            'checkbutton',
            color=self._color,
            extras=self._extras,
            variant=self._variant,
            **self._kwargs
        )
        if self._on_change:
            self.on_change = self._on_change
