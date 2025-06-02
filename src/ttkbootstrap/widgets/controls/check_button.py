from tkinter import IntVar, Misc, StringVar
from tkinter.ttk import Checkbutton as ttkCheckButton
from typing import Any, Callable, Literal, Optional, Tuple, TypedDict, Union, Unpack

from ttkbootstrap.ttk_types import StyleColor
from ttkbootstrap.utils import keys_to_lower
from ttkbootstrap.widgets.mixins import BackgroundMixin, BaseMixin, StyleMixin


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


class CheckButton(StyleMixin, BaseMixin, BackgroundMixin):
    """
    A styled `Checkbutton` widget with theme-aware styling, value binding,
    icon support, and event callbacks.

    Attributes:
        widget (ttkCheckButton): The internal checkbutton widget.
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
        on_click: Optional[Callable] = None,
        on_value_changed: Optional[Callable] = None,
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
            on_click (Optional[Callable]): Callback triggered when clicked.
            on_value_changed (Optional[Callable]): Callback when value changes.
            **kwargs (CheckButtonOptions): Additional ttk options.
        """
        kw = dict(kwargs)
        self._master = master
        self._icon = icon
        self._color = color
        self._on_click = on_click
        self._on_value_changed = on_value_changed
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
            command=self._on_click,
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
        if self._on_value_changed:
            func = self._on_value_changed
            self._on_value_changed = lambda x, y, z: func(self.value)
            self.variable.trace_add('write', self._on_value_changed)

    def invoke(self):
        """
        Programmatically trigger the checkbutton's action.

        Returns:
            Any: The result of the command callback, if defined.
        """
        return self.widget.invoke()

    @property
    def widget(self) -> ttkCheckButton:
        """Return the internal `ttk.Checkbutton` widget."""
        return self._widget

    @property
    def text(self) -> str:
        """Get or set the checkbutton's label text."""
        return self._text_variable.get()

    @text.setter
    def text(self, value: str):
        self._text_variable.set(value)

    @property
    def value(self):
        """Get or set the current value of the checkbutton."""
        return self._variable.get()

    @value.setter
    def value(self, value: Literal[-1, 0, 1]):
        self._variable.set(value)
        if value == -1:
            self.widget.state(['alternate'])

    @property
    def enabled(self) -> bool:
        """Get or set whether the checkbutton is enabled."""
        return self.widget.cget('state') != 'disabled'

    @enabled.setter
    def enabled(self, value: bool):
        self.widget.configure(state='normal' if value else 'disabled')

    @property
    def on_click(self) -> Optional[Callable]:
        """Get or set the function triggered when clicked."""
        return self._on_click

    @on_click.setter
    def on_click(self, value: Callable):
        self._on_click = value
        self.widget.configure(command=value)

    @property
    def on_value_changed(self):
        """Get or set the callback when the checkbutton value changes."""
        return self._on_value_changed

    @on_value_changed.setter
    def on_value_changed(self, value: Callable[[int], Any]):
        self._on_value_changed = lambda x, y, z: value(self.value)
        self.variable.trace_add('write', self._on_value_changed)

    @property
    def cursor(self) -> str:
        """Get or set the mouse cursor when hovering."""
        return self.widget.cget('cursor')

    @cursor.setter
    def cursor(self, value: str):
        self.widget.configure(cursor=value)

    @property
    def width(self) -> int:
        """Get or set the width of the checkbutton in text units."""
        return self.widget.cget('width')

    @width.setter
    def width(self, value: int):
        self.widget.configure(width=value)

    @property
    def padding(self) -> Union[int, Tuple[int, int], Tuple[int, int, int, int]]:
        """Get or set internal widget padding."""
        return self.widget.cget('padding')

    @padding.setter
    def padding(self, value: Union[int, Tuple[int, int], Tuple[int, int, int, int]]):
        self.widget.configure(padding=value)

    @property
    def take_focus(self) -> bool:
        """Get or set whether the widget takes keyboard focus."""
        return self.widget.cget('takefocus')

    @take_focus.setter
    def take_focus(self, value: bool):
        self.widget.configure(takefocus=value)

    @property
    def underline(self) -> int:
        """Get or set the index of the character to underline in the text."""
        return self.widget.cget('underline')

    @underline.setter
    def underline(self, value: int):
        self.widget.configure(underline=value)

    @property
    def text_variable(self) -> StringVar:
        """Return the StringVar used to hold the checkbutton's label text."""
        return self._text_variable

    @property
    def variable(self) -> IntVar:
        """Return the IntVar used to hold the checkbutton's value."""
        return self._variable

    @property
    def on_value(self) -> int:
        """Return the value used when the checkbutton is selected."""
        return self.widget.cget("onvalue")

    @property
    def off_value(self) -> int:
        """Return the value used when the checkbutton is deselected."""
        return self.widget.cget("offvalue")

    @property
    def selected(self) -> bool:
        return self.value == self.on_value
