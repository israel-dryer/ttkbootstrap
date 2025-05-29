from tkinter import DoubleVar, Misc
from tkinter.ttk import Scale as ttkScale
from typing import Any, Callable, Literal, Optional, TypedDict, Unpack

from ttkbootstrap.ttk_types import StyleColor
from ttkbootstrap.utils import keys_to_lower
from ttkbootstrap.widgets.mixins import (
    BackgroundMixin,
    BaseMixin,
    StyleMixin,
)


class SliderOptions(TypedDict, total=False):
    """Typed dictionary for supported ttk slider options."""
    compound: Literal['text', 'image', 'center', 'top', 'bottom', 'left', 'right', 'none']
    cursor: str
    take_focus: bool
    length: int
    inherit_background: bool


class Slider(StyleMixin, BaseMixin, BackgroundMixin):
    """
     A styled `ttk.Scale` widget with theme-aware styling, value precision control,
     event callbacks, and variable binding support.

     Args:
         master (Optional[Misc]): Parent widget.
         value (float): Initial value of the slider.
         min_value (float): Minimum slider value.
         max_value (float): Maximum slider value.
         precision (int): Number of decimal places to round the value.
         orient (Literal['horizontal', 'vertical']): Orientation of the slider.
         color (StyleColor): Named theme color for the slider (e.g., 'primary', 'success').
         on_click (Optional[Callable]): Callback triggered when the slider is dragged.
         on_value_changed (Optional[Callable[[float], Any]]): Callback triggered when the value changes.
         **kwargs (Unpack[SliderOptions]): Additional configuration options passed to the internal ttk.Scale.

     Example:
         ```python
         def on_change(value):
             print(f"New value: {value}")

         Slider(
             root,
             value=50,
             min_value=0,
             max_value=100,
             precision=1,
             color="info",
             on_value_changed=on_change
         )
         ```
     """

    def __init__(
        self,
        master: Optional[Misc] = None,
        value=0.0,
        min_value=0.0,
        max_value=100.0,
        precision=2,
        orient: Literal['horizontal', 'vertical'] = "horizontal",
        color: StyleColor = "default",
        on_click: Optional[Callable] = None,
        on_value_changed: Optional[Callable] = None,
        **kwargs: Unpack[SliderOptions]
    ):
        kw = dict(kwargs)
        self._master = master
        self._color = color
        self._orient = orient
        self._on_click = on_click
        self._on_value_changed = on_value_changed
        self._kwargs = kw
        self._extras = {"orient": orient}
        self._min_value = min_value
        self._max_value = max_value
        self._precision = precision
        self._inherit_background = kw.pop('inherit_background', False)
        self._variable = DoubleVar(master, value)
        self._widget: Misc
        self._prev_value = value
        self._render_widget()

    def _render_widget(self):
        """Create and initialize the internal ttk.Radiobutton widget."""
        self._widget: ttkScale = ttkScale(
            self._master,
            from_=self._min_value,
            to=self._max_value,
            command=self._on_click,
            variable=self._variable,
            orient=self._orient,
            **keys_to_lower(self._kwargs)
        )

        self._initialize_style(
            'slider',
            color=self._color,
            extras=self._extras,
            **self._kwargs
        )

        if self._on_value_changed:
            func = self._on_value_changed
            self._on_value_changed = lambda x, y, z: self._value_changed_wrapper(func)
            self.variable.trace_add('write', self._on_value_changed)

    @property
    def widget(self) -> ttkScale:
        """Return the internal slider widget."""
        return self._widget

    @property
    def variable(self):
        """Return the Variable linked to the slider value."""
        return self._variable

    @property
    def value(self):
        """Get or set the slider value."""
        return round(self._variable.get(), self._precision)

    @value.setter
    def value(self, value: float):
        self._variable.set(value)

    @property
    def enabled(self) -> bool:
        """Return True if the slider is enabled; otherwise False."""
        return self.widget.cget('state') != 'disabled'

    @enabled.setter
    def enabled(self, value: bool):
        self.widget.configure(state='normal' if value else 'disabled')

    @property
    def on_click(self) -> Optional[Callable]:
        """Get or set the command function triggered on button click."""
        return self._on_click

    @on_click.setter
    def on_click(self, func: Callable):
        self._on_click = func
        self.widget.configure(command=func)

    @property
    def on_value_changed(self):
        """Get or set the callback function triggered when the slider value changes."""
        return self._on_value_changed

    @on_value_changed.setter
    def on_value_changed(self, func: Callable[[float], Any]):
        self._on_value_changed = lambda x, y, z: self._value_changed_wrapper(func)
        self.variable.trace_add('write', self._on_value_changed)

    def _value_changed_wrapper(self, func: Callable[[float], Any]):
        if (self.value == self._prev_value):
            return "break"
        else:
            func(self.value)
            self._prev_value = self.value

    @property
    def cursor(self) -> str:
        """Get or set the mouse cursor when hovering over the slider."""
        return self.widget.cget('cursor')

    @cursor.setter
    def cursor(self, value: str):
        self.widget.configure(cursor=value)

    @property
    def length(self) -> int:
        """Get or set the length of the slider (long-dimension) in screen units."""
        return self.widget.cget('width')

    @length.setter
    def length(self, value: int):
        self.widget.configure(length=value)

    @property
    def take_focus(self) -> bool:
        """Get or set whether the button can take focus via keyboard navigation."""
        return self.widget.cget('takefocus')

    @take_focus.setter
    def take_focus(self, value: bool):
        self.widget.configure(takefocus=value)
