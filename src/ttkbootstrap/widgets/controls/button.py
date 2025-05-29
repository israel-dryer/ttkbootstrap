from tkinter import Misc, PhotoImage, StringVar
from tkinter.ttk import Button as ttkButton
from typing import Callable, Literal, Optional, Tuple, TypedDict, Union, Unpack

from ttkbootstrap.ttk_types import StyleColor
from ttkbootstrap.utils import keys_to_lower
from ttkbootstrap.widgets.mixins import (
    BackgroundMixin,
    BaseMixin,
    IconMixin,
    StyleMixin,
)


class ButtonOptions(TypedDict, total=False):
    """Typed dictionary for supported ttk Button options."""
    compound: Literal['text', 'image', 'center', 'top', 'bottom', 'left', 'right', 'none']
    cursor: str
    default: Literal['normal', 'active', 'disabled']
    image: PhotoImage
    take_focus: bool
    width: int
    inherit_background: bool


class Button(StyleMixin, BaseMixin, IconMixin, BackgroundMixin):
    """
    A styled button widget that supports icon rendering, style variants, and command bindings.

    Args:
        master (Optional[Misc]): Parent widget.
        text (Optional[str]): Initial text value of the button.
        icon (Optional[Union[str, Tuple[str, int]]]): Icon name or (name, size) tuple.
        color (StyleColor): Named style color for the button theme.
        variant (str): Named style variant (e.g. 'outline', 'primary').
        on_click (Optional[Callable]): Function to call when the button is clicked.
        **kwargs (Unpack[ButtonOptions]): Additional options passed to ttk.Button.

    Example:
        ```python
        Button(root, text="Submit", color="primary", on_click=submit_form)
        ```
    """

    def __init__(
            self,
            master: Optional[Misc] = None,
            text: Optional[str] = None,
            icon: Optional[Union[str, Tuple[str, int]]] = None,
            color: StyleColor = "default",
            variant="default",
            on_click: Optional[Callable] = None,
            **kwargs: Unpack[ButtonOptions]
    ):
        kw = dict(kwargs)
        self._master = master
        self._icon = icon
        self._color = color
        self._variant = variant
        self._on_click = on_click
        self._kwargs = kw
        self._extras = {}
        self._image: Optional[PhotoImage] = None
        self._inherit_background = kw.pop('inherit_background', False)
        self._variable = StringVar(master, text)
        self._widget: Misc
        self._render_widget()

    def _render_widget(self):
        """Create and initialize the internal ttk.Button widget."""
        self._inject_icon_support(default_compound="left")
        self._widget = ttkButton(
            self._master,
            command=self._on_click,
            textvariable=self._variable,
            **keys_to_lower(self._kwargs)
        )
        self._bind_icon_events()

        self._initialize_style(
            'button',
            color=self._color,
            variant=self._variant,
            extras=self._extras,
            **self._kwargs
        )

    @property
    def widget(self) -> Misc:
        """Return the internal ttk.Button widget."""
        return self._widget

    @property
    def variable(self) -> StringVar:
        """Return the StringVar linked to the button text."""
        return self._variable

    @property
    def text(self) -> str:
        """Get or set the button label text."""
        return self.variable.get()

    @text.setter
    def text(self, value: str):
        self.variable.set(value)

    @property
    def enabled(self) -> bool:
        """Return True if the button is enabled; otherwise False."""
        return self.widget.cget('state') != 'disabled'

    @enabled.setter
    def enabled(self, value: bool):
        self.widget.configure(state='normal' if value else 'disabled')

    @property
    def on_click(self) -> Optional[Callable]:
        """Get or set the command function triggered on button click."""
        return self._on_click

    @on_click.setter
    def on_click(self, value: Callable):
        self._on_click = value
        self.widget.configure(command=value)

    @property
    def cursor(self) -> str:
        """Get or set the mouse cursor when hovering over the button."""
        return self.widget.cget('cursor')

    @cursor.setter
    def cursor(self, value: str):
        self.widget.configure(cursor=value)

    @property
    def image(self) -> Optional[PhotoImage]:
        """Return the associated image if set via icon mixin."""
        return self._image

    @property
    def width(self) -> int:
        """Get or set the width of the button in text units."""
        return self.widget.cget('width')

    @width.setter
    def width(self, value: int):
        self.widget.configure(width=value)

    @property
    def take_focus(self) -> bool:
        """Get or set whether the button can take focus via keyboard navigation."""
        return self.widget.cget('takefocus')

    @take_focus.setter
    def take_focus(self, value: bool):
        self.widget.configure(takefocus=value)

    @property
    def default(self) -> bool:
        """Return True if the button is set as the default button."""
        return self.widget.cget('default') in ('normal', 'active')

    @default.setter
    def default(self, is_default: bool, is_active_default: bool = False):
        """
        Set the default state of the button.

        Args:
            is_default (bool): Whether to mark the button as default.
            is_active_default (bool): Whether it should be the active default.
        """
        if is_active_default:
            self.widget.configure(default='active')
        elif is_default:
            self.widget.configure(default='normal')
        else:
            self.widget.configure(default='disabled')

    def invoke(self):
        """
        Programmatically trigger the button's click action.

        Returns:
            Any: The return value of the associated command function, if any.
        """
        return self.widget.invoke()
