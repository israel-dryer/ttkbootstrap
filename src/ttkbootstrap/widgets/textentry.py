from tkinter import Variable
from typing import Callable, TypedDict

from typing_extensions import Unpack

from ttkbootstrap.signals import Signal
from ttkbootstrap.widgets.field import Field


class TextEntryOptions(TypedDict, total=False):
    """Type hints for TextEntry widget configuration options.

    Attributes:
        allow_blank: If True, empty input is allowed. If False, empty input preserves previous value.
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
        take_focus: If True, widget can receive focus via Tab key.
        textvariable: Tkinter Variable to link with the entry text.
        textsignal: Signal object for reactive text updates.
        width: Width of the entry in characters.
        required: If True, field cannot be empty (adds validation rule).
        xscrollcommand: Callback for horizontal scrolling.
    """
    allow_blank: bool
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
    take_focus: bool
    textvariable: Variable
    textsignal: Signal
    width: str
    required: bool
    xscrollcommand: Callable[[int, int], None]


class TextEntry(Field):
    """A text entry field widget with label, validation, and formatting support.

    TextEntry is a composite widget that combines a label, text entry input, and
    message area into a single component. It provides internationalization-aware
    text input with deferred parsing, validation support, and visual feedback.

    The widget separates user input (display text) from the committed/parsed value,
    only parsing and formatting when the user commits via <FocusOut> or <Return>.

    Features:
        - Optional label with required field indicator (*)
        - Deferred parsing and formatting on commit
        - International formatting support (numbers, currency, dates, etc.)
        - Built-in validation with visual error feedback
        - Message area for hints or error messages
        - Add-on widget support (prefix/suffix icons or buttons)
        - Three-tier event system:
            - <<Input>>: Fires on every keystroke with raw text
            - <<Changed>>: Fires when committed value changes
            - <<Valid>>/<<Invalid>>: Fires on validation results

    Events:
        <<Input>>: Triggered on each keystroke
            event.data = {"text": str}

        <<Changed>>: Triggered when value changes after commit (FocusOut/Return)
            event.data = {"value": Any, "prev_value": Any, "text": str}

        <<Valid>>: Triggered when validation passes
            event.data = {"value": Any, "is_valid": True, "message": str}

        <<Invalid>>: Triggered when validation fails
            event.data = {"value": Any, "is_valid": False, "message": str}

        <<Validated>>: Triggered after any validation
            event.data = {"value": Any, "is_valid": bool, "message": str}

    Example:
        ```python
        import ttkbootstrap as ttk
        from ttkbootstrap.widgets.textentry import TextEntry

        root = ttk.Window()

        # Simple text entry with label
        entry1 = TextEntry(
            root,
            label="Name",
            message="Enter your full name",
            required=True
        )
        entry1.pack(padx=20, pady=10, fill='x')

        # Currency entry with formatting
        entry2 = TextEntry(
            root,
            label="Amount",
            value="1234.56",
            value_format='$#,##0.00',
            locale='en_US'
        )
        entry2.pack(padx=20, pady=10, fill='x')

        # Password entry
        entry3 = TextEntry(
            root,
            label="Password",
            show='*',
            required=True
        )
        entry3.pack(padx=20, pady=10, fill='x')

        # Entry with addon button
        entry4 = TextEntry(root, label="Search")
        entry4.insert_addon(ttk.Button, 'after', text='Go')
        entry4.pack(padx=20, pady=10, fill='x')

        # Bind to events
        def on_changed(event):
            print(f"Value changed to: {event.data['value']}")

        entry1.on_changed(on_changed)

        root.mainloop()
        ```

    Validation:
        ```python
        # Add validation rules
        entry = TextEntry(root, label="Email", required=True)
        entry.add_validation_rule('email', message='Invalid email address')

        # Handle validation events
        def handle_invalid(event):
            print(f"Error: {event.data['message']}")

        entry.bind('<<Invalid>>', handle_invalid)
        ```

    Inherited Properties:
        entry_widget: Access to the underlying TextEntryPart widget
        label_widget: Access to the label widget
        message_widget: Access to the message label widget
        addons: Dictionary of inserted addon widgets
        variable: Tkinter Variable linked to entry text
        signal: Signal object for reactive updates
    """

    def __init__(
            self, master=None, value: str = "", label: str = None, message: str = None,
            **kwargs: Unpack[TextEntryOptions]):
        """Initialize a TextEntry widget.

        Creates a composite text entry field with optional label, validation,
        and formatting support. The widget includes a label area, entry input,
        and message area for displaying hints or validation errors.

        Args:
            master: Parent widget. If None, uses the default root window.
            value: Initial value to display. Default is empty string.
            label: Optional label text to display above the entry field.
                If required=True, an asterisk (*) is automatically appended.
            message: Optional message text to display below the entry field.
                This is replaced by validation error messages when validation fails.
            **kwargs: Additional keyword arguments from TextEntryOptions:
                allow_blank (bool): Allow empty input. Default is False.
                cursor (str): Cursor style when hovering.
                value_format (str): ICU format pattern for parsing/formatting.
                    Examples: '$#,##0.00' (currency), '#,##0.00' (decimal),
                    'yyyy-MM-dd' (date), '#,##0.00%' (percent)
                exportselection (bool): Export selection to clipboard.
                font (str): Font for text display.
                foreground (str): Text color.
                initial_focus (bool): If True, widget receives focus on creation.
                justify (str): Text alignment ('left', 'center', 'right').
                show_message (bool): If True, displays message area. Default is True.
                padding (str): Padding around entry widget.
                show (str): Character to mask input (e.g., '*' for passwords).
                take_focus (bool): If True, widget accepts Tab focus.
                textvariable (Variable): Tkinter Variable to link with text.
                textsignal (Signal): Signal object for reactive updates.
                width (str): Width in characters.
                required (bool): If True, field cannot be empty. Adds 'required'
                    validation rule and appends '*' to label.
                xscrollcommand (Callable): Callback for horizontal scrolling.

        Example:
            ```python
            # Basic text entry
            entry = TextEntry(root, label="Username", required=True)

            # Currency entry with formatting
            entry = TextEntry(
                root,
                label="Price",
                value="99.99",
                value_format='¤#,##0.00',
                locale='en_US',
                message="Enter product price"
            )

            # Password entry
            entry = TextEntry(
                root,
                label="Password",
                show='*',
                required=True,
                message="Must be at least 8 characters"
            )

            # Email entry with validation
            entry = TextEntry(root, label="Email", required=True)
            entry.add_validation_rule('email')
            ```

        Note:
            The widget automatically sets up event handlers for focus, validation,
            and value commits. Use on_input(), on_changed(), on_valid(), and
            on_invalid() methods to bind callbacks to widget events.
        """
        super().__init__(master, value=value, label=label, message=message, **kwargs)
