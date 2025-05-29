from tkinter import Misc, StringVar
from tkinter.ttk import Radiobutton as ttkRadioButton
from typing import Any, Callable, Literal, Optional, Tuple, TypedDict, Union, Unpack

from ttkbootstrap.ttk_types import StyleColor, Variable
from ttkbootstrap.utils import keys_to_lower
from ttkbootstrap.widgets.mixins import (
    BackgroundMixin,
    BaseMixin,
    StyleMixin,
)


class RadioButtonOptions(TypedDict, total=False):
    """Typed dictionary for supported ttk checkbutton options."""
    compound: Literal['text', 'image', 'center', 'top', 'bottom', 'left', 'right', 'none']
    cursor: str
    take_focus: bool
    width: int
    inherit_background: bool


class RadioButton(StyleMixin, BaseMixin, BackgroundMixin):
    """
    A styled `RadioButton` widget with theme-aware styling, value binding, and event callbacks.

    Args:
        master (Optional[Misc]): Parent widget.
        text (Optional[str]): The label text of the radiobutton.
        value (Optional[Union[str, int]]: The value of the radiobutton when selected.
        selected (bool): Whether the radiobutton is selected by default. If `True`, the `value` parameter is required.
        group (str): The button group associated with this radiobutton.
        color (StyleColor): Named style color for theming.
        on_click (Optional[Callable]): Callback function when the checkbutton is clicked.
        on_value_changed (Optional[Callable]): Callback function when the value changes.
        **kwargs (Unpack[CheckButtonOptions]): Additional keyword options passed to ttk.Checkbutton.

    Example:
        ```python
        RadioButton(root, text="Generator", group="options", value="gen", color="success", on_value_changed=on_toggle)
        ```
    """

    def __init__(
        self,
        master: Optional[Misc] = None,
        text: Optional[str] = None,
        value: Optional[Union[str, int]] = None,
        selected: bool = False,
        group: Optional[str] = None,
        color: StyleColor = "default",
        on_click: Optional[Callable] = None,
        on_value_changed: Optional[Callable] = None,
        **kwargs: Unpack[RadioButtonOptions]
    ):
        kw = dict(kwargs)
        self._master = master
        self._group = group
        self._color = color
        self._on_click = on_click
        self._on_value_changed = on_value_changed
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
            command=self._on_click,
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

        if self._on_value_changed:
            func = self._on_value_changed
            self._on_value_changed = lambda x, y, z: func(self.value)
            self.variable.trace_add('write', self._on_value_changed)

    @property
    def widget(self) -> Misc:
        """Return the internal checkbutton widget."""
        return self._widget

    @property
    def text_variable(self) -> StringVar:
        """Return the StringVar linked to the checkbutton label."""
        return self._text_variable

    @property
    def variable(self):
        """Return the Variable linked to the checkbutton value."""
        return self._variable

    @property
    def text(self) -> str:
        """Get or set the button label text."""
        return self.text_variable.get()

    @text.setter
    def text(self, value: str):
        self.text_variable.set(value)

    @property
    def value(self):
        """Get or set the checkbutton value."""
        return self._variable.get()

    @value.setter
    def value(self, value: Literal[-1, 0, 1]):
        self._variable.set(value)
        if value == -1:
            self.widget.state(['alternate'])

    @property
    def enabled(self) -> bool:
        """Return True if the checkbutton is enabled; otherwise False."""
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
    def on_value_changed(self):
        """Get or set the callback function triggered when the checkbutton value changes."""
        return self._on_value_changed

    @on_value_changed.setter
    def on_value_changed(self, value: Callable[[int], Any]):
        self._on_value_changed = lambda x, y, z: value(self.value)
        self.variable.trace_add('write', self._on_value_changed)

    @property
    def cursor(self) -> str:
        """Get or set the mouse cursor when hovering over the checkbutton."""
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
    def take_focus(self) -> bool:
        """Get or set whether the button can take focus via keyboard navigation."""
        return self.widget.cget('takefocus')

    @take_focus.setter
    def take_focus(self, value: bool):
        self.widget.configure(takefocus=value)

    def invoke(self):
        """
        Programmatically trigger the radiobutton's click action.

        Returns:
            Any: The return value of the associated on_click function, if any.
        """
        return self.widget.invoke()
