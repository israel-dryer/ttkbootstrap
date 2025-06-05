from tkinter import Misc, StringVar
from tkinter.ttk import Spinbox as ttkSpinbox
from typing import Callable

from ..mixins import BaseMixin, MinMaxMixin, StyleMixin, EntryMixin
from ...ttk_types import StyleColor
from ...utils import keys_to_lower


class NumberBox(
    BaseMixin,
    StyleMixin,
    EntryMixin,
    MinMaxMixin,
):
    def __init__(
        self,
        master: Misc = None,
        value: float | int = 0,
        min_value: float | int = 0,
        max_value: float | int = 100,
        increment: float | int = 1,
        format: str = None,
        color: StyleColor = "default",
        on_change: Callable = None,
        **kwargs
    ):
        self._master = master
        self._kwargs = dict(kwargs)
        self._min_value = min_value
        self._max_value = max_value
        self._increment = increment
        self._on_change = on_change
        self._color = color
        self._variant = "default"
        self._format = format
        self._inherit_background = self._kwargs.pop('inherit_background', False)
        self._text = value
        self._prev_text = value
        self._text_variable = StringVar(master, (str(value)))
        self._extras = {}
        self._widget: "ttkSpinbox"

        # set a default font if not provided
        if 'font' not in self._kwargs:
            self._kwargs['font'] = '-size 12'

        self._render_widget()

    def _render_widget(self):
        """Create and initialize the internal ttk widget."""
        self._widget: "ttkSpinbox" = ttkSpinbox(
            self._master,
            from_=self._min_value,
            to=self._max_value,
            increment=self._increment,
            format=self._format,
            textvariable=self._text_variable,
            **keys_to_lower(self._kwargs)
        )
        self._initialize_style(
            'spinbox',
            color=self._color,
            variant=self._variant,
            extras=self._extras,
            **self._kwargs
        )

        if self._on_change:
            self.on_change = self._on_change

        """
            TODO this works for now, but in the future, I want the on_change to behave more like a
            number input box where the value changes on focus-out

            TODO the value should be treated as a number instead of as text.
        """
        self.widget.bind('<FocusOut>', self._clamp_value)

    def _clamp_value(self, _):
        """Prevent the user from using a number outside of bounds"""
        print(isinstance(self.min_value, int))
        if (isinstance(self.min_value, float)):
            # treat this as a floating value
            self.text = min(max(float(self.min_value), float(self.value)), float(self.max_value))
        else:
            try:
                # treat as an integer
                self.text = min(max(int(self.min_value), int(self.value)), int(self.max_value))
            except:
                # should be an integer, but a float was typed into the entry, so treat as a float
                self.text = min(max(float(self.min_value), float(self.value)), float(self.max_value))

    @property
    def value(self):
        return self.text

    @value.setter
    def value(self, value):
        self._text = value

    @property
    def _prev_value(self):
        return self.text

    @_prev_value.setter
    def _prev_value(self, value):
        self._prev_text = value
