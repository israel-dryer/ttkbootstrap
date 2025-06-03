from tkinter import IntVar, Misc, StringVar
from tkinter.ttk import Checkbutton as ttkCheckButton
from typing import Callable, Literal, Optional, Tuple, TypedDict, Union, Unpack

from ttkbootstrap.ttk_types import StyleColor
from ttkbootstrap.utils import keys_to_lower
from ttkbootstrap.widgets.mixins import (
    BackgroundMixin, BaseMixin, StyleMixin,
    EnabledMixIn, OnChangeMixin, OnOffValueMixin, PaddingMixin,
    TextVariableMixin, VariableMixin, WidthMixin
)


class CheckButtonOptions(TypedDict, total=False):
    """Typed dictionary of supported options for the `CheckButton` widget."""
    compound: Literal['text', 'image', 'center', 'top', 'bottom', 'left', 'right', 'none']
    cursor: str
    take_focus: bool
    width: int
    padding: Union[int, Tuple[int, int], Tuple[int, int, int, int]]
    style: str
    state: Literal['normal', 'disabled']
    underline: int
    off_value: int
    on_value: int
    variable: IntVar
    inherit_background: bool


class CheckButton(
    StyleMixin,
    BaseMixin,
    VariableMixin,
    TextVariableMixin,
    EnabledMixIn,
    OnChangeMixin,
    WidthMixin,
    PaddingMixin,
    OnOffValueMixin,
    BackgroundMixin
):
    """
    A styled `Checkbutton` widget with theme-aware styling, value binding,
    icon support, and event callbacks.

    Attributes:
        widget (ttk.Checkbutton): The internal checkbutton widget.
        text_variable (StringVar): The text variable for the label.
        variable (IntVar): The value variable for the checkbutton.
    """

    def __init__(
        self,
        master: Optional[Misc] = None,
        text: Optional[str] = None,
        value: Optional[Literal[-1, 0, 1]] = -1,
        icon: Optional[Union[str, Tuple[str, int]]] = None,
        color: StyleColor = "default",
        on_change: Optional[Callable] = None,
        **kwargs: Unpack[CheckButtonOptions]
    ):
        """
        Initialize the CheckButton.

        Args:
            master (Optional[Misc]): Parent widget.
            text (Optional[str]): Text displayed next to the checkbutton.
            value (Literal[-1, 0, 1]): Initial value (-1: indeterminate, 0: off, 1: on).
            icon (Optional[str|Tuple]): The name or tuple (name, size) of the icon.
            color (StyleColor): Theme color used to style the widget.
            on_change (Optional[Callable]): Callback when value changes.
            **kwargs (CheckButtonOptions): Additional ttk options.
        """
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
        """Create and initialize the internal `ttk.Checkbutton`."""
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
            func = self._on_change
            self._on_change = lambda x, y, z: func(self.value)
            self.variable.trace_add('write', self._on_change)
