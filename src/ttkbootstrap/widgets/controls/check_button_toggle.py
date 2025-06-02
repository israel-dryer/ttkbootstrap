from tkinter import IntVar, Misc, PhotoImage, StringVar
from tkinter.ttk import Checkbutton as ttkCheckButton
from typing import Any, Callable, Literal, Optional, Tuple, TypedDict, Union, Unpack

from ttkbootstrap.ttk_types import StyleColor
from ttkbootstrap.utils import keys_to_lower
from ttkbootstrap.widgets.mixins import (
    BackgroundMixin,
    BaseMixin,
    IconMixin,
    StyleMixin,
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


class CheckButtonToggle(StyleMixin, BaseMixin, IconMixin, BackgroundMixin):
    """
    A themed toggle-style checkbutton widget

    Args:
        master (Optional[Misc]): Parent container.
        text (Optional[str]): Label to display beside the toggle.
        value (Literal[-1, 0, 1]): Initial toggle state.
        color (StyleColor): Bootstrap-like color token (e.g., "primary", "info").
        icon (Optional[Union[str, Tuple[str, int]]]): Name or (name, size) of the icon.
        variant (Literal["default", "outline"]): Style variant for toggle appearance.
        on_click (Optional[Callable]): Function to call when clicked.
        on_value_changed (Optional[Callable]): Function to call when value changes.
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
        on_click: Optional[Callable] = None,
        on_value_changed: Optional[Callable] = None,
        **kwargs: Unpack[CheckButtonToggleOptions]
    ):
        self._master = master
        self._icon = icon
        self._color = color
        self._on_click = on_click
        self._on_value_changed = on_value_changed
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
            command=self._on_click,
            textvariable=self._text_variable,
            variable=self._variable,
            **keys_to_lower(self._kwargs)
        )
        self._bind_icon_events()
        self._prepare_icon_kwargs(default_compound="left")
        self._initialize_style(
            'button',
            color=self._color,
            extras=self._extras,
            variant=self._variant,
            **self._kwargs
        )
        if self._on_value_changed:
            func = self._on_value_changed
            self._on_value_changed = lambda x, y, z: func(self.value)
            self.variable.trace_add('write', self._on_value_changed)

    def invoke(self):
        """
        Programmatically trigger the checkbutton's click action.
        Returns:
            Any: The return value of the associated command function, if any.
        """
        return self.widget.invoke()

    @property
    def widget(self) -> "ttkCheckButton":
        """Return the internal checkbutton widget."""
        return self._widget

    @property
    def text_variable(self) -> StringVar:
        """Return the StringVar linked to the checkbutton label."""
        return self._text_variable

    @property
    def variable(self) -> IntVar:
        """Return the IntVar linked to the checkbutton value."""
        return self._variable

    @property
    def text(self) -> str:
        """Get or set the checkbutton's label text."""
        return self.text_variable.get()

    @text.setter
    def text(self, value: str):
        self.text_variable.set(value)

    @property
    def value(self) -> int:
        """Get or set the current checkbutton value."""
        return self._variable.get()

    @value.setter
    def value(self, value: Literal[-1, 0, 1]):
        self._variable.set(value)
        if value == -1:
            self.widget.state(['alternate'])

    @property
    def on_click(self) -> Optional[Callable]:
        """Get or set the function triggered when clicked."""
        return self._on_click

    @on_click.setter
    def on_click(self, value: Callable):
        self._on_click = value
        self.widget.configure(command=value)

    @property
    def on_value_changed(self) -> Optional[Callable]:
        """Get or set the function triggered when the checkbutton value changes."""
        return self._on_value_changed

    @on_value_changed.setter
    def on_value_changed(self, value: Callable[[int], Any]):
        self._on_value_changed = lambda x, y, z: value(self.value)
        self.variable.trace_add('write', self._on_value_changed)

    @property
    def enabled(self) -> bool:
        """Return True if the widget is enabled; otherwise False."""
        return self.widget.cget('state') != 'disabled'

    @enabled.setter
    def enabled(self, value: bool):
        self.widget.configure(state='normal' if value else 'disabled')

    @property
    def cursor(self) -> str:
        """Get or set the mouse cursor when hovering over the widget."""
        return self.widget.cget('cursor')

    @cursor.setter
    def cursor(self, value: str):
        self.widget.configure(cursor=value)

    @property
    def width(self) -> int:
        """Get or set the width of the widget in text units."""
        return self.widget.cget('width')

    @width.setter
    def width(self, value: int):
        self.widget.configure(width=value)

    @property
    def take_focus(self) -> bool:
        """Get or set whether the widget can take focus with the keyboard."""
        return self.widget.cget('takefocus')

    @take_focus.setter
    def take_focus(self, value: bool):
        self.widget.configure(takefocus=value)

    @property
    def compound(self) -> str:
        """Get or set the layout of image and text in the widget."""
        return self.widget.cget("compound")

    @compound.setter
    def compound(self, value: Literal["top", "bottom", "left", "right", "center", "none"]):
        self.widget.configure(compound=value)

    @property
    def padding(self) -> Union[int, Tuple[int, int], Tuple[int, int, int, int]]:
        """Get or set the internal padding of the widget."""
        return self.widget.cget("padding")

    @padding.setter
    def padding(self, value: Union[int, Tuple[int, int], Tuple[int, int, int, int]]):
        self.widget.configure(padding=value)

    @property
    def on_value(self) -> int:
        """Return the value used when the checkbutton is selected."""
        return self.widget.cget("onvalue")

    @property
    def off_value(self) -> int:
        """Return the value used when the checkbutton is deselected."""
        return self.widget.cget("offvalue")

    @property
    def image(self) -> Optional[PhotoImage]:
        """Return the rendered icon image, if available."""
        return self._image

    @property
    def selected(self) -> bool:
        return self.value == self.on_value
