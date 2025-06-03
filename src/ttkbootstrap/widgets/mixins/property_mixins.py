from tkinter import PhotoImage, StringVar
from typing import Any, Callable, Literal, Tuple, Union

from ttkbootstrap.ttk_types import Variable


class TextVariableMixin:
    _text_variable: StringVar = None

    @property
    def text_variable(self):
        """The text_variable associated with the widget"""
        return self._text_variable

    @text_variable.setter
    def text_variable(self, value: StringVar):
        self._text_variable = value
        self.widget.configure(textvariable=value)

    @property
    def text(self):
        """The value of the text"""
        return self._text_variable.get()

    @text.setter
    def text(self, value):
        self._text_variable.set(value)

    @property
    def underline(self) -> int:
        """Specifies the integer index (0-based) of a character to underline in the text string. end corresponds to the last character, end-1 to the before last character, and so on."""
        return self.widget.cget('underline')

    @underline.setter
    def underline(self, value: int):
        self.widget.configure(underline=value)


class ImageMixin:
    """Exposes the -image option of a ttk widget."""

    @property
    def image(self):
        """The image associated with the widget."""
        return self.widget.cget("image")

    @image.setter
    def image(self, value: Union[str, PhotoImage]):
        self.widget.configure(image=value)

    @property
    def compound(self):
        """Specifies how to display the image relative to the text, in the case both text and image are present."""
        return self.widget.cget("compound")

    @compound.setter
    def compound(self, value: Literal['text', 'image', 'center', 'top', 'bottom', 'left', 'right', 'none']):
        self.widget.configure(compound=value)


class OnClickMixin:
    _on_click: Callable = None

    @property
    def on_click(self):
        """A function executed when the widget is clicked."""
        return self.widget.cget("command")

    @on_click.setter
    def on_click(self, value):
        self._on_click = value
        self.widget.configure(command=value)


class VariableMixin:
    _variable: Variable
    _precision: int

    @property
    def variable(self):
        """Get the variable associated with the widget."""
        return self._variable

    @variable.setter
    def variable(self, value):
        self._variable = value
        self.widget.configure(variable=value)

    @property
    def value(self):
        """The value of the widget"""
        if not hasattr(self, '_precision'):
            return self.variable.get() if self.variable else None
        else:
            return round(self._variable.get(), self._precision) if self.variable else None

    @value.setter
    def value(self, val):
        if self.variable:
            self.variable.set(val)


class PaddingMixin:

    @property
    def padding(self) -> Union[str, Tuple[int, int]]:
        """Get or set the internal padding inside the widget."""
        return self.widget.cget("padding")

    @padding.setter
    def padding(self, value: Union[str, Tuple[int, int]]):
        self.widget.configure(padding=value)


class WrapLengthMixin:

    @property
    def wrap_length(self) -> int:
        """Specifies the maximum line length."""
        return self.widget.cget("wraplength")

    @wrap_length.setter
    def wrap_length(self, value: int):
        self.widget.configure(wraplength=value)


class WidthMixin:

    @property
    def width(self):
        """The widget of the widget"""
        return self.widget.cget("width")

    @width.setter
    def width(self, value: int):
        self.widget.configure(width=value)


class EnabledMixIn:
    @property
    def enabled(self) -> bool:
        """Enable or disable the widget from user interaction"""
        return self.widget.cget('state') != 'disabled'

    @enabled.setter
    def enabled(self, value: bool):
        self.widget.configure(state='normal' if value else 'disabled')


class HeightMixin:
    @property
    def height(self):
        """The height of the widget"""

        return self.widget.cget("height")

    @height.setter
    def height(self, value):
        self.widget.configure(height=value)


class JustifyMixin:
    @property
    def justify(self):
        """If there are multiple lines of text, specifies how the lines are laid out relative to one another."""
        return self.widget.cget("justify")

    @justify.setter
    def justify(self, value: Literal['left', 'right', 'center']):
        self.widget.configure(justify=value)


class OrientMixin:
    @property
    def orient(self):
        """The orientation of the widget"""
        return self.widget.cget("orient")

    @orient.setter
    def orient(self, value: Literal['horizontal', 'vertical']):
        self.widget.configure(orient=value)


class MinMaxMixin:

    @property
    def min_value(self):
        """The lowest value allowed"""

        return self.widget.cget("from")

    @min_value.setter
    def min_value(self, value):
        self.widget.configure(from_=value)

    @property
    def max_value(self):
        """The highest value allowed"""
        return self.widget.cget("to")

    @max_value.setter
    def max_value(self, value):
        self.widget.configure(to=value)


class LengthMixin:

    @property
    def length(self):
        """The length of the long dimension in screen units"""
        return self.widget.cget("length")

    @length.setter
    def length(self, value):
        self.widget.configure(length=value)


class FontMixin:

    @property
    def font(self):
        """Font to use for the text displayed by the widget."""
        return self.widget.cget("font")

    @font.setter
    def font(self, value):
        self.widget.configure(font=value)


class AnchorMixin:

    @property
    def anchor(self):
        """Specifies how the information in the widget is positioned relative to the inner margins."""
        return self.widget.cget("anchor")

    @anchor.setter
    def anchor(self, value):
        self.widget.configure(anchor=value)


class DefaultMixin:

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


class ValidationMixin:

    @property
    def validation_mode(self):
        """Specifies the mode in which validation should operate: none, focus, focusin, focusout, key, or all."""
        return self.widget.cget("validate")

    @validation_mode.setter
    def validation_mode(self, value):
        self.widget.configure(validate=value)

    @property
    def on_validated(self):
        """A function executed whenever validation is triggered"""

        return self.widget.cget("validatecommand")

    @on_validated.setter
    def on_validated(self, value):
        self.widget.configure(validatecommand=value)

    @property
    def on_invalid(self):
        """A function executed whenever validation returns False"""
        return self.widget.cget("invalidcommand")

    @on_invalid.setter
    def on_invalid(self, value):
        self.widget.configure(invalidcommand=value)


class OnChangeMixin:
    variable: Variable
    value: Any
    _prev_value: Any

    @property
    def on_change(self):
        """A function called when the value changes"""
        return self._on_change

    @on_change.setter
    def on_change(self, value: Callable[[Any], Any]):
        self._on_change = lambda x, y, z: self._value_change_wrapper(value)
        self.variable.trace_add('write', self._on_change)

    def _value_change_wrapper(self, func: Callable[[float], Any]):
        # no previous value defined
        if not hasattr(self, '_prev_value'):
            return func(self.value)

        if (self.value == self._prev_value):
            return "break"
        else:
            func(self.value)
            self._prev_value = self.value


class OnOffValueMixin:

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
