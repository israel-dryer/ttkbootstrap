from typing import Any

from typing_extensions import Unpack

from ttkbootstrap.widgets.composites.field import Field, FieldOptions
from ttkbootstrap.widgets.types import Master


class TextEntry(Field):
    """A text entry field widget with label, validation, and formatting support.

    TextEntry is a composite widget that combines a label, text entry input, and
    message area into a single component. It provides internationalization-aware
    text input with deferred parsing, validation support, and visual feedback.

    The widget separates user input (display text) from the committed/parsed value,
    only parsing and formatting when the user commits via ``<FocusOut>`` or ``<Return>``.

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
        entry_widget (TextEntryPart): The underlying text entry widget.
        label_widget (Label): The label widget above the entry.
        message_widget (Label): The message label widget below the entry.
        addons (dict[str, Widget]): Dictionary of inserted addon widgets by name.
        variable (Variable): Tkinter Variable linked to entry text.
        signal (Signal): Signal object for reactive updates.
    """

    def __init__(
            self, master: Master = None, value: Any = None, label: str = None, message: str = None,
            **kwargs: Unpack[FieldOptions]):
        """Initialize a TextEntry widget.

        Creates a composite text entry field with optional label, validation,
        and formatting support. The widget includes a label area, entry input,
        and message area for displaying hints or validation errors.

        Args:
            master: Parent widget. If None, uses the default root window.
            value: Initial value to display. Default is None.
            label: Optional label text to display above the entry field.
                If required=True, an asterisk (*) is automatically appended.
            message: Optional message text to display below the entry field.
                This is replaced by validation error messages when validation fails.

        Other Parameters:
            allow_blank (bool): Allow empty input. Default is True.
            color (str): Color token for the focus ring and active border.
            bootstyle (str): DEPRECATED - Use `color` instead.
            cursor (str): Cursor style when hovering.
            value_format (str): ICU format pattern for parsing/formatting.
            exportselection (bool): Export selection to clipboard.
            font (str): Font for text display.
            foreground (str): Text color.
            initial_focus (bool): If True, widget receives focus on creation.
            justify (str): Text alignment ('left', 'center', 'right').
            show_message (bool): If True, displays message area. Default is True.
            padding: Padding around entry widget.
            show (str): Character to mask input (e.g., '*' for passwords).
            takefocus (bool): If True, widget accepts Tab focus.
            textvariable (Variable): Tkinter Variable to link with text.
            textsignal (Signal): Signal object for reactive updates.
            width (int): Width in characters.
            required (bool): If True, field cannot be empty. Adds 'required'
                validation rule and appends '*' to label.
            xscrollcommand: Callback for horizontal scrolling.

        Note:
            The widget automatically sets up event handlers for focus, validation,
            and value commits. Use on_input(), on_changed(), on_valid(), and
            on_invalid() methods to bind callbacks to widget events.
        """
        super().__init__(master, value=value, label=label, message=message, **kwargs)

