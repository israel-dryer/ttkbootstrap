"""Field widget module.

Provides a flexible generic entry field composite widget used as the foundation
for creating specialized entry widgets like TextEntry, PasswordEntry, NumberEntry, etc.
"""

from tkinter import TclError, Variable
from typing import Any, Callable, Literal, Type, TypedDict, Union, cast

from ttkbootstrap.core.signals import Signal
from ttkbootstrap.widgets.primitives.button import Button
from ttkbootstrap.widgets.primitives.frame import Frame
from ttkbootstrap.widgets.primitives.label import Label
from ttkbootstrap.widgets.primitives.checkbutton import CheckButton
from ttkbootstrap.widgets.mixins import configure_delegate
from ttkbootstrap.widgets.mixins.entry_mixin import EntryMixin
from ttkbootstrap.widgets.parts.numberentry_part import NumberEntryPart
from ttkbootstrap.widgets.parts.textentry_part import TextEntryPart
from ttkbootstrap.widgets.parts.spinnerentry_part import SpinnerEntryPart
from ttkbootstrap.widgets.types import Master

FieldKind = Literal['text', 'numeric', 'spinbox']
"""Type alias for field kind specification.

Determines which entry part widget to use:
    - 'text': Uses TextEntryPart for text input with formatting support
    - 'numeric': Uses NumberEntryPart for numeric input with bounds and stepping
    - 'spinbox': Uses SpinnerEntryPart for spinner input (supports text or numeric values)
"""


class FieldOptions(TypedDict, total=False):
    """Type hints for Field widget configuration options.

    Attributes:
        allow_blank: If True, empty input is allowed. If False, empty input preserves previous value.
        accent: Accent token for the focus ring and active border of the input.
        variant: Style variant (if applicable).
        bootstyle: DEPRECATED - Use accent instead.
        cursor: Cursor to display when hovering over the widget.
        value_format: ICU format pattern for parsing/formatting (e.g., '$#,##0.00' for currency).
        exportselection: If True, selected text is exported to X selection.
        font: Font to use for text display.
        foreground: Text color.
        initial_focus: If True, widget receives focus when created.
        justify: Text justification ('left', 'center', 'right').
        show_message: If True, displays message text below the field.
        padding: Padding around the entry widget.
        show: Character to display instead of typed characters (for password fields).
        state: The widget state. One of 'normal', 'disabled', or 'readonly'.
        takefocus: If True, widget can receive focus via Tab key.
        textvariable: Tkinter Variable to link with the entry text.
        textsignal: Signal object for reactive text updates.
        width: Width of the entry in characters.
        required: If True, field cannot be empty (adds validation rule).
        xscrollcommand: Callback for horizontal scrolling.
        localize: Determines the field label localization mode. 'auto', True, False.
    """
    allow_blank: bool
    bootstyle: str  # DEPRECATED: Use accent instead
    accent: str
    variant: str
    cursor: str
    value_format: str
    exportselection: bool
    font: str
    foreground: str
    initial_focus: bool
    justify: str
    show_message: bool
    padding: str
    show: str
    state: Literal['normal', 'disabled', 'readonly']
    takefocus: bool
    textvariable: Variable
    textsignal: Signal
    width: int
    required: bool
    xscrollcommand: Callable[[int, int], None]
    localize: bool | Literal['auto']


class Field(EntryMixin, Frame):
    """A flexible generic composite entry field widget.

    Field is a base composite widget that combines a label, entry input, and
    message area into a complete input field component. It serves as the foundation
    for creating specialized entry widgets like TextEntry, PasswordEntry, NumberEntry,
    and other custom entry types.

    The widget automatically handles layout, focus states, validation feedback, and
    provides a consistent API for all entry-based components. It supports both text
    and numeric input types through the ``kind`` parameter.

    !!! note "Events"

        - ``<<Input>>``: Triggered on each keystroke.
          Provides ``event.data`` with keys: ``text``.

        - ``<<Change>>``: Triggered when value changes after commit.
          Provides ``event.data`` with keys: ``value``, ``prev_value``, ``text``.

        - ``<<Valid>>``: Triggered when validation passes.
          Provides ``event.data`` with keys: ``value``, ``is_valid`` (True), ``message``.

        - ``<<Invalid>>``: Triggered when validation fails.
          Provides ``event.data`` with keys: ``value``, ``is_valid`` (False), ``message``.

        - ``<<Validate>>``: Triggered after any validation.
          Provides ``event.data`` with keys: ``value``, ``is_valid`` (bool), ``message``.

    Attributes:
        variable (Variable): Tkinter Variable linked to entry text.
        signal (Signal): Signal object for reactive updates.
    """

    def __init__(
            self,
            master: Master = None,
            *,
            value: str | int | float = None,
            label: str = None,
            message: str = None,
            show_message: bool = False,
            required: bool = False,
            kind: FieldKind = "text",
            **kwargs: Any
    ):
        """Initialize a Field widget.

        Creates a composite entry field with optional label, message area, and
        validation support. The field type is determined by the 'kind' parameter,
        which selects either TextEntryPart or NumberEntryPart as the underlying
        entry widget.

        Args:
            master: Parent widget. If None, uses the default root window.
            value: Initial value to display. Can be str, int, or float depending
                on the field kind. For 'text' kind, should be a string. For
                'numeric' kind, can be int or float. Default is None.
            label: Optional label text to display above the entry field.
                If required=True, an asterisk (*) is automatically appended to
                indicate the field is mandatory.
            message: Optional message text to display below the entry field.
                Used for hints, instructions, or help text. This text is replaced
                by validation error messages when validation fails, and restored
                when validation passes. Default is None (no message).
            show_message: If True, displays the message area below the field.
                If False, hides the message area entirely (validation errors
                won't be shown). Default is True.
            required: If True, marks the field as required and automatically adds
                a 'required' validation rule. An asterisk (*) is appended to the
                label. The field cannot be left empty. Default is False.
            kind: Type of entry field to create. Either 'text' for text input
                (uses TextEntryPart) or 'numeric' for numeric input (uses
                NumberEntryPart). Default is 'text'.

        Other Parameters:
            value_format (str): ICU format pattern for parsing/formatting.
            allow_blank (bool): Allow empty input.
            locale (str): Locale for formatting (e.g., 'en_US').
            initial_focus (bool): Focus on creation.
            show (str): Character to mask input (e.g., '*' for passwords).
            width (int): Width in characters.
            font (str): Font specification.
            justify (str): Text alignment ('left', 'center', 'right').
            minvalue (int | float): Minimum allowed value (numeric kind only).
            maxvalue (int | float): Maximum allowed value (numeric kind only).
            increment (int | float): Step size for up/down arrows (numeric kind only).
            wrap (bool): Wrap around at boundaries (numeric kind only).
        """
        # Accept legacy parameter name and prevent it from reaching the Tk widget.
        if 'show_messages' in kwargs:
            show_message = kwargs.pop('show_messages')
        # Track if user explicitly provided show_message
        show_message_explicit = 'show_message' in kwargs
        show_message = kwargs.pop('show_message', show_message)

        # Auto-enable show_message if message is provided and user didn't explicitly disable it
        if message and not show_message_explicit:
            show_message = True

        # Extract accent - support legacy 'bootstyle' parameter
        accent = kwargs.pop('accent', None)
        bootstyle = kwargs.pop('bootstyle', None)  # Legacy support
        self._localize = cast(bool | Literal['auto'], kwargs.pop('localize', 'auto'))

        # Field itself (outer Frame) doesn't need styling - only pass master
        super().__init__(master)

        # Set accent AFTER super().__init__ to avoid being overwritten by wrapper
        self._accent = accent or bootstyle

        # configuration
        self._message_text = message
        self._show_messages = show_message
        self._addons: dict[str, Button | Label | CheckButton] = {}
        self._required = required
        self._kind = kind
        self._label_text = label
        self._value = value

        self._entry: TextEntryPart | NumberEntryPart | SpinnerEntryPart
        self._addons: dict[str, Union[Button, Label, CheckButton]] = {}

        # layout
        label_text = self._label_text or ''
        self._label_lbl = Label(
            self,
            localize=self._localize,
            text=f"{label_text}*" if required else label_text,
            font="label[normal]"
        )
        self._message_lbl = Label(self, localize=self._localize, text=message or '', font="caption", accent="secondary")

        # field container & field
        self._field = Frame(self, accent=self._accent, padding=5, ttk_class="TField")

        if kind == "numeric":
            self._entry = NumberEntryPart(self._field, value=value, **kwargs)
        elif kind == "spinbox":
            self._entry = SpinnerEntryPart(self._field, value=value, **kwargs)
        else:
            self._entry = TextEntryPart(self._field, value=value, **kwargs)

        # attach widgets
        if label:
            self._label_lbl.pack(side='top', fill='x', padx=(4, 0))

        self._field.pack(side='top', fill='x', expand=True)
        self._entry.pack(side='left', fill='x', expand=True, padx=0, pady=0)

        self._entry.bind('<<StateChanged>>', self._sync_addon_state, add=True)
        self._sync_addon_state()

        if self._show_messages:
            self._message_lbl.pack(side='top', fill='x', padx=4)

        self._entry.bind('<<Invalid>>', self._show_error, add=True)
        self._entry.bind('<<Valid>>', self._clear_error, add=True)

        # bind focus styling to the field frame
        self._entry.bind('<FocusIn>', lambda _: self._field.state(['focus']), add=True)
        self._entry.bind('<FocusOut>', lambda _: self._field.state(['!focus']), add=True)

        # add required validation
        if required:
            self._entry.add_validation_rule("required")

        # forward reference entry methods
        self.on_input = self._entry.on_input
        self.off_input = self._entry.off_input
        self.on_changed = self._entry.on_changed
        self.off_changed = self._entry.off_changed
        self.on_enter = self._entry.on_enter
        self.off_enter = self._entry.off_enter
        self.on_invalid = self._entry.on_invalid
        self.off_invalid = self._entry.off_invalid
        self.on_valid = self._entry.on_valid
        self.off_valid = self._entry.off_valid
        self.on_validated = self._entry.on_validated
        self.off_validated = self._entry.off_validated

        # entry state
        self.variable = self._entry.textvariable
        self.signal = self._entry.textsignal

        # enty validation
        self.add_validation_rule = self._entry.add_validation_rule
        self.add_validation_rules = self._entry.add_validation_rules
        self.validation = self._entry.validate

        # Copy Field's delegate handlers to entry for configuration forwarding
        for key, method_name in self._configure_delegate_map.items():
            if hasattr(self, method_name):
                # Attach the Field's handler method to the entry instance
                setattr(self._entry, method_name, getattr(self, method_name))
                # Add to entry's delegate map
                self._entry._configure_delegate_map[key] = method_name

        # Forward configuration methods to entry widget
        self.configure = self._entry.configure
        self.config = self._entry.config
        self.cget = self._entry.cget
        self.__getitem__ = self._entry.__getitem__
        self.__setitem__ = self._entry.__setitem__

    @property
    def value(self):
        """Get or set the parsed value via the underlying entry widget."""
        return self._entry.value()

    @value.setter
    def value(self, value):
        self._entry.value(value)

    def get(self):
        """Return the raw text from the underlying entry widget."""
        return self._entry.get()

    @property
    def entry_widget(self) -> NumberEntryPart | TextEntryPart:
        """Get the underlying entry widget."""
        return self._entry

    @property
    def label_widget(self):
        """Get the label widget."""
        return self._label_lbl

    @property
    def message_widget(self):
        """Get the message widget."""
        return self._message_lbl

    @property
    def addons(self):
        """Get the dictionary of inserted addon widgets"""
        return self._addons

    @configure_delegate
    def _config_accent(self, value=None):
        if value is None:
            return self._accent
        else:
            self._accent = value
            self._field['accent'] = value
        return None

    @configure_delegate
    def _config_bootstyle(self, value=None):
        """DEPRECATED: Use accent instead."""
        if value is None:
            return self._accent
        else:
            self._accent = value
            self._field['accent'] = value
        return None

    def disable(self):
        """Disable the field, preventing user input."""
        self._entry.state(['disabled !readonly'])
        self._field.state(['disabled'])
        self._set_addons_state(True)

    def enable(self):
        """Enable the field, allowing user input."""
        self._entry.state(['!disabled !readonly'])
        self._field.state(['!disabled'])
        self._set_addons_state(False)

    def readonly(self, value: bool = None):
        """Set or toggle the readonly state of the field."""
        if value == False:
            self._field.state(['disabled'])
            self._entry.state(['readonly'])
        elif value:
            self._field.state(['!disabled'])
            self._entry.state(['readonly'])
        else:
            self._entry.state(['readonly !disabled'])
            self._field.state(['disabled'])
        self._sync_addon_state()

    def insert_addon(
            self,
            widget: Type[Union[Button, Label, CheckButton]],
            position: Literal['before', 'after'],
            name: str | None = None,
            pack_options: dict[str, Any] = None,
            **kwargs: Any
    ):
        """Insert a widget addon before or after the entry input.

        Addons are Button, Label, or Checkbutton widgets positioned inside the field container,
        either before (left of) or after (right of) the entry input. Common use
        cases include search buttons, icons, clear buttons, or status indicators.

        The addon widget automatically:
        - Inherits the field's disabled state
        - Participates in focus state styling (highlights field on addon focus)
        - Is stored in the addons dictionary for later reference

        Args:
            widget: Widget class to instantiate. Must be Button, Label, or Checkbutton.
            position: Position relative to the entry input:
                - 'before': Insert to the left of the entry (prefix)
                - 'after': Insert to the right of the entry (suffix)
            name: Optional name for the addon. If provided, the addon can be
                retrieved from the addons dictionary using this name. If None,
                the widget's string representation is used as the key.
            pack_options: Optional dictionary of additional pack() options to
                apply when placing the addon widget. Common options include
                padx, pady, etc. The side and after/before options are set
                automatically based on position.
            **kwargs (Any): Additional keyword arguments passed to the widget constructor.
                For Button: text, command, icon, bootstyle, etc.
                For Label: text, icon, image, bootstyle, etc.
                Note: bootstyle and takefocus are set automatically but can be
                overridden.
        """
        variant = "suffix" if position == "after" else "prefix"
        kwargs.setdefault('ttk_class', 'TField')
        kwargs.setdefault('variant', variant)
        kwargs.setdefault('takefocus', False)

        if widget in (Button, CheckButton):
            if 'style_options' in kwargs:
                kwargs['style_options'].update(use_active_states=True)
            else:
                kwargs['style_options'] = dict(use_active_states=True)
        instance = widget(master=self._field, **kwargs)
        key = name or str(instance)
        self._addons[key] = instance

        # configure layout
        options = pack_options or {}
        if position == "after":
            options.update(side="right", after=self._entry)
        else:
            options.update(side="left", before=self._entry)
        instance.pack(**options)

        # match parent disabled state
        self._sync_addon_state()

        # bind focus events to field frame
        instance.bind('<FocusIn>', lambda _: self._field.state(['focus']), add=True)
        instance.bind('<FocusOut>', lambda _: self._field.state(['!focus']), add=True)

    def _show_error(self, event: Any) -> None:
        """Display a validation error message below the input field."""
        self._message_lbl['text'] = event.data['message']
        self._message_lbl['accent'] = "danger"
        self._message_lbl.pack(side='top', after=self._field, padx=4)

    def _clear_error(self, _: Any) -> None:
        """Clear the error message and restore the original message text."""
        self._message_lbl['text'] = self._message_text
        self._message_lbl['accent'] = "secondary"

    def _set_addons_state(self, disabled: bool) -> None:
        """Configure addon widgets based on whether the entry is interactive."""
        state_value = 'disabled' if disabled else '!disabled'
        for item in self._addons.values():
            try:
                item.configure(state=state_value)
            except TclError:
                pass

    def _sync_addon_state(self, event: Any = None) -> None:
        """Ensure addons match the entry's interactivity state."""
        entry_states = self._entry.state()
        disabled = 'disabled' in entry_states or 'readonly' in entry_states
        self._set_addons_state(disabled)
