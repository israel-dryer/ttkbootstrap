from tkinter import Misc, StringVar
from tkinter.ttk import Entry as ttkEntry
from typing import Callable

from ..mixins import BaseMixin, StyleMixin, EntryMixin
from ..mixins.property_mixins import ValidationMode
from ...ttk_types import StyleColor
from ...utils import keys_to_lower


class TextBox(
    BaseMixin,
    StyleMixin,
    EntryMixin
):

    def __init__(
        self,
        master: Misc = None,
        text: str = "",
        color: StyleColor = "default",
        validation_mode: ValidationMode = "none",
        on_validated: Callable = None,
        on_invalid: Callable = None,
        on_change: Callable = None,
        **kwargs
    ):
        self._master = master
        self._kwargs = dict(kwargs)
        self._validation_mode = validation_mode
        self._on_validated = on_validated
        self._on_invalid = on_invalid
        self._on_change = on_change
        self._color = color
        self._variant = "default"
        self._inherit_background = self._kwargs.pop('inherit_background', False)
        self._text = text
        self._prev_text = text
        self._text_variable = StringVar(master, text)
        self._extras = {}
        self._widget: "ttkEntry"

        # set a default font if not provided
        if 'font' not in self._kwargs:
            self._kwargs['font'] = '-size 12'

        self._render_widget()

    def _render_widget(self):
        """Create and initialize the internal ttk.Button widget."""
        self._widget: "ttkEntry" = ttkEntry(
            self._master,
            validate=self._validation_mode,
            validatecommand=self._on_validated,
            invalidcommand=self._on_invalid,
            textvariable=self._text_variable,
            **keys_to_lower(self._kwargs)
        )
        self._initialize_style(
            'input',
            color=self._color,
            variant=self._variant,
            extras=self._extras,
            **self._kwargs
        )

        if self._on_change:
            self.on_change = self._on_change
