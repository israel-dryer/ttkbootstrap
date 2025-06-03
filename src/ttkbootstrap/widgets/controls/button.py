from tkinter import Misc, PhotoImage, StringVar
from tkinter.ttk import Button as ttkButton
from typing import Callable, Literal, Optional, Tuple, Union

from ttkbootstrap.ttk_types import StyleColor
from ttkbootstrap.utils import keys_to_lower
from ttkbootstrap.widgets.mixins import (
    AnchorMixin, BackgroundMixin, BaseMixin, IconMixin,
    StyleMixin, DefaultMixin, EnabledMixIn, ImageMixin,
    OnClickMixin, PaddingMixin, TextVariableMixin, WidthMixin
)


class Button(
    StyleMixin,
    BaseMixin,
    AnchorMixin,
    TextVariableMixin,
    ImageMixin,
    OnClickMixin,
    PaddingMixin,
    WidthMixin,
    EnabledMixIn,
    DefaultMixin,
    IconMixin,
    BackgroundMixin,
):
    """
    A styled button widget that supports icon rendering, style variants, and command bindings.

    Args:
        master (Optional[Misc]): Parent widget.
        text (Optional[str]): Initial text value of the button.
        icon (Optional[Union[str, Tuple[str, int]]]): Icon name or (name, size) tuple.
        color (StyleColor): Named style color for the button theme.
        variant (str): Named style variant (e.g. 'outline', 'primary').
        on_click (Optional[Callable]): Function to call when the button is clicked.
        **kwargs: Additional options passed to ttk.Button.
    """

    def __init__(
        self,
        master: Optional[Misc] = None,
        text: Optional[str] = None,
        icon: Optional[Union[str, Tuple[str, int]]] = None,
        color: StyleColor = "default",
        variant: Literal['default', 'outline', 'text'] = "default",
        on_click: Optional[Callable] = None,
        **kwargs
    ):
        kw = dict(kwargs)
        self._master = master
        self._icon = icon
        self._color = color
        self._variant = variant
        self._on_click = on_click
        self._kwargs = kw
        self._extras = {}
        self._text = text
        self._image: Optional[PhotoImage] = None
        self._inherit_background = kw.pop('inherit_background', False)
        self._variable = StringVar(master, text)
        self._widget: Misc
        self._render_widget()

    def _render_widget(self):
        """Create and initialize the internal ttk.Button widget."""
        self._widget: "ttkButton" = ttkButton(
            self._master,
            command=self._on_click,
            textvariable=self._variable,
            **keys_to_lower(self._kwargs)
        )
        self._bind_icon_events()
        self._prepare_icon_kwargs(default_compound="left")
        self._initialize_style(
            'button',
            color=self._color,
            variant=self._variant,
            extras=self._extras,
            **self._kwargs
        )

    def invoke(self):
        """
        Programmatically trigger the button's click action.

        Returns:
            Any: The return value of the associated command function, if any.
        """
        return self.widget.invoke()
