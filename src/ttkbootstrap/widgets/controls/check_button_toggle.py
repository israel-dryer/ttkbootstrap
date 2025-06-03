from tkinter import IntVar, Misc, PhotoImage, StringVar
from tkinter.ttk import Checkbutton as ttkCheckButton
from typing import Callable, Literal, Optional, Tuple, TypedDict, Union, Unpack

from ttkbootstrap.ttk_types import StyleColor
from ttkbootstrap.utils import keys_to_lower
from ttkbootstrap.widgets.mixins import (
    BackgroundMixin, BaseMixin, EnabledMixIn, IconMixin,
    ImageMixin, OnChangeMixin, OnOffValueMixin, PaddingMixin,
    StyleMixin, TextVariableMixin, VariableMixin, WidthMixin,
)


class CheckButtonToggleOptions(TypedDict, total=False):
    """Typed dictionary for supported ttk checkbutton options."""
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

    Args:
        master (Optional[Misc]): Parent container.
        text (Optional[str]): Label to display beside the toggle.
        value (Literal[-1, 0, 1]): Initial toggle state.
        color (StyleColor): Bootstrap-like color token (e.g., "primary", "info").
        icon (Optional[Union[str, Tuple[str, int]]]): Name or (name, size) of the icon.
        variant (Literal["default", "outline"]): Style variant for toggle appearance.
        on_change (Optional[Callable]): Function to call when value changes.
        **kwargs (CheckButtonToggleOptions): Additional ttk-compatible options.
    """

    def __init__(
        self,
        master: Optional[Misc] = None,
        text: Optional[str] = None,
        value: Optional[Literal[-1, 0, 1]] = -1,
        color: StyleColor = "primary",
        icon: Optional[Union[str, Tuple[str, int]]] = None,
        variant: Literal['default', 'outline'] = "default",
        on_change: Optional[Callable] = None,
        **kwargs: Unpack[CheckButtonToggleOptions]
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
        """Create and initialize the internal checkbutton widget."""
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
            func = self._on_change
            self._on_change = lambda x, y, z: func(self.value)
            self.variable.trace_add('write', self._on_change)

    def invoke(self):
        """
        Programmatically trigger the checkbutton's click action.
        Returns:
            Any: The return value of the associated command function, if any.
        """
        return self.widget.invoke()
