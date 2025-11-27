"""Field widget module.

Provides a flexible generic entry field composite widget used as the foundation
for creating specialized entry widgets like TextEntry, PasswordEntry, NumberEntry, etc.
"""

from tkinter import TclError, Variable
from typing import Any, Callable, Literal, Type, TypedDict, Union

from ttkbootstrap.signals import Signal
from ttkbootstrap.widgets.button import Button
from ttkbootstrap.widgets.frame import Frame
from ttkbootstrap.widgets.label import Label
from ttkbootstrap.widgets.mixins import configure_delegate
from ttkbootstrap.widgets.mixins.entry_mixin import EntryMixin
from ttkbootstrap.widgets.parts.numberentry_part import NumberEntryPart
from ttkbootstrap.widgets.parts.textentry_part import TextEntryPart

FieldKind = Literal['text', 'numeric']
"""Type alias for field kind specification.

Determines which entry part widget to use:
    - 'text': Uses TextEntryPart for text input with formatting support
    - 'numeric': Uses NumberEntryPart for numeric input with bounds and stepping
"""


class FieldOptions(TypedDict, total=False):
    """Type hints for Field widget configuration options.

    Attributes:
        allow_blank: If True, empty input is allowed. If False, empty input preserves previous value.
        bootstyle: The accent color of the focus ring and active border of the input.
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
    bootstyle: str
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


class Field(EntryMixin, Frame):
    """A flexible generic composite entry field widget.

    Field is a base composite widget that combines a label, entry input, and
    message area into a complete input field component. It serves as the foundation
    for creating specialized entry widgets like TextEntry, PasswordEntry, NumberEntry,
    and other custom entry types.

    The widget automatically handles layout, focus states, validation feedback, and
    provides a consistent API for all entry-based components. It supports both text
    and numeric input types through the 'kind' parameter.

    Architecture:
        - Label area (optional): Displays field label with required indicator (*)
        - Field container: Styled frame that contains the entry and any addons
        - Entry widget: Either TextEntryPart or NumberEntryPart based on 'kind'
        - Message area (optional): Displays hints or validation error messages
        - Addon support: Insert Button or Label widgets before/after the entry

    Features:
        - Automatic label and message layout
        - Required field indicator (asterisk)
        - Focus state styling on field container
        - Validation feedback with automatic error message display
        - Add-on widget support (prefix/suffix icons, buttons)
        - Entry method forwarding (delegates to underlying entry widget)
        - Consistent state management (disable, enable, readonly)
        - Event forwarding from underlying entry widget

    Events (forwarded from entry widget):
        <<Input>>: Triggered on each keystroke
            event.data = {"text": str}

        <<Changed>>: Triggered when value changes after commit
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
        from ttkbootstrap.widgets.parts.field import Field

        root = ttk.Window()

        # Text field with label and message
        field1 = Field(
            root,
            kind='text',
            label='Username',
            message='Enter your username',
            required=True
        )
        field1.pack(padx=20, pady=10, fill='x')

        # Numeric field with bounds
        field2 = Field(
            root,
            kind='numeric',
            label='Age',
            value=25,
            minvalue=0,
            maxvalue=120,
            required=True
        )
        field2.pack(padx=20, pady=10, fill='x')

        # Field with addon button
        field3 = Field(root, label='Search', kind='text')
        field3.insert_addon(ttk.Button, 'after', text='Go')
        field3.pack(padx=20, pady=10, fill='x')

        # Custom validation
        field4 = Field(root, label='Email', required=True)
        field4.add_validation_rule('email', message='Invalid email')
        field4.pack(padx=20, pady=10, fill='x')

        root.mainloop()
        ```

    Subclassing:
        ```python
        from ttkbootstrap.widgets.parts.field import Field

        class PasswordEntry(Field):
            '''Password entry field with masked input.'''

            def __init__(self, master=None, **kwargs):
                # Force text kind and mask characters
                kwargs.update(show='*')
                super().__init__(master, kind='text', **kwargs)
        ```

    Properties:
        entry_widget: The underlying TextEntryPart or NumberEntryPart widget
        label_widget: The Label widget for the field label
        message_widget: The Label widget for messages/errors
        addons: Dictionary of inserted addon widgets (Button or Label)
        variable: Tkinter Variable linked to entry text
        signal: Signal object for reactive updates

    Forwarded Methods:
        on_input(callback): Bind callback to <<Input>> event
        on_changed(callback): Bind callback to <<Changed>> event
        on_enter(callback): Bind callback to <Return> event
        on_invalid(callback): Bind callback to <<Invalid>> event
        on_valid(callback): Bind callback to <<Valid>> event
        on_validated(callback): Bind callback to <<Validated>> event
        add_validation_rule(rule_type, **kwargs): Add a validation rule
        add_validation_rules(rules): Replace all validation rules
        validation(value, trigger): Run validation against a value

    Inherited from EntryMixin:
        delete(first, last), insert(index, text), get(), selection_*(), etc.
    """

    def __init__(
            self,
            master=None,
            value: str | int | float = None,
            label: str = None,
            message: str = None,
            show_messages: bool = True,
            required: bool = False,
            kind: FieldKind = "text",
            **kwargs
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
            show_messages: If True, displays the message area below the field.
                If False, hides the message area entirely (validation errors
                won't be shown). Default is True.
            required: If True, marks the field as required and automatically adds
                a 'required' validation rule. An asterisk (*) is appended to the
                label. The field cannot be left empty. Default is False.
            kind: Type of entry field to create. Either 'text' for text input
                (uses TextEntryPart) or 'numeric' for numeric input (uses
                NumberEntryPart). Default is 'text'.
            **kwargs: Additional keyword arguments passed to the underlying entry
                widget (TextEntryPart or NumberEntryPart). Common options include:

                For text kind:
                    - value_format (str): ICU format pattern for parsing/formatting
                    - allow_blank (bool): Allow empty input
                    - locale (str): Locale for formatting (e.g., 'en_US')
                    - initial_focus (bool): Focus on creation
                    - show (str): Character to mask input (e.g., '*' for passwords)
                    - width (int): Width in characters
                    - font (str): Font specification
                    - justify (str): Text alignment ('left', 'center', 'right')

                For numeric kind:
                    - minvalue (int|float): Minimum allowed value
                    - maxvalue (int|float): Maximum allowed value
                    - increment (int|float): Step size for up/down arrows
                    - wrap (bool): Wrap around at boundaries
                    - value_format (str): Number format pattern
                    - allow_blank (bool): Allow empty input

        Example:
            ```python
            # Simple text field
            field1 = Field(
                root,
                kind='text',
                label='Name',
                message='Enter your full name',
                required=True
            )

            # Numeric field with bounds
            field2 = Field(
                root,
                kind='numeric',
                label='Age',
                value=25,
                minvalue=0,
                maxvalue=120,
                increment=1
            )

            # Currency field
            field3 = Field(
                root,
                kind='text',
                label='Price',
                value='99.99',
                value_format='$#,##0.00',
                locale='en_US'
            )

            # Password field
            field4 = Field(
                root,
                kind='text',
                label='Password',
                show='*',
                required=True,
                message='Minimum 8 characters'
            )

            # Field without message area
            field5 = Field(
                root,
                label='Code',
                show_messages=False
            )
            ```

        Note:
            The widget automatically:
            - Sets up validation event bindings (<<Valid>>, <<Invalid>>)
            - Adds focus state styling to the field container
            - Forwards entry methods (on_input, on_changed, etc.)
            - Creates a 'required' validation rule if required=True
            - Manages message display for validation feedback
        """
        self._bootstyle = kwargs.pop('bootstyle', 'default')

        super().__init__(master)

        # configuration
        self._message_text = message
        self._show_messages = show_messages
        self._addons: dict[str, Button | Label] = {}
        self._required = required
        self._kind = kind
        self._label_text = label
        self._value = value

        self._entry: TextEntryPart | NumberEntryPart
        self._addons: dict[str, Union[Button, Label]] = {}

        # layout
        self._label_lbl = Label(self, text=self._label_text + '*' if required else '', font="label[normal]")
        self._message_lbl = Label(self, text=message or '', font="caption", bootstyle="secondary")

        # field container & field
        self._field = Frame(self, bootstyle=self._bootstyle, padding=6, class_="TField")

        if kind == "numeric":
            self._entry = NumberEntryPart(self._field, value=value, **kwargs)
        else:
            self._entry = TextEntryPart(self._field, value=value, **kwargs)

        # attach widgets
        if label:
            self._label_lbl.pack(side='top', fill='x', padx=(4, 0))

        self._field.pack(side='top', fill='x', expand=True)
        self._entry.pack(side='top', fill='both', expand=True)

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
        self.on_changed = self._entry.on_changed
        self.on_enter = self._entry.on_enter
        self.on_invalid = self._entry.on_invalid
        self.on_valid = self._entry.on_valid
        self.on_validated = self._entry.on_validated

        # entry state
        self.variable = self._entry.textvariable
        self.signal = self._entry.textsignal

        # enty validation
        self.add_validation_rule = self._entry.add_validation_rule
        self.add_validation_rules = self._entry.add_validation_rules
        self.validation = self._entry.validate

    @property
    def entry_widget(self) -> NumberEntryPart | TextEntryPart:
        """Get the underlying entry widget.

        Returns:
            The TextEntryPart or NumberEntryPart widget that handles user input,
            depending on the 'kind' specified during initialization.

        Example:
            ```python
            field = Field(root, kind='text', label='Name')
            entry = field.entry_widget
            entry.insert(0, 'John')  # Direct access to entry methods
            ```
        """
        return self._entry

    @property
    def label_widget(self):
        """Get the label widget.

        Returns:
            The Label widget that displays the field label text (with optional
            asterisk for required fields).

        Example:
            ```python
            field = Field(root, label='Name', required=True)
            label = field.label_widget
            label.configure(foreground='blue')  # Customize label appearance
            ```
        """
        return self._label_lbl

    @property
    def message_widget(self):
        """Get the message widget.

        Returns:
            The Label widget that displays message text below the entry field.
            This widget shows hints, help text, or validation error messages.

        Example:
            ```python
            field = Field(root, label='Email', message='Required')
            msg = field.message_widget
            msg.configure(font='italic')  # Customize message appearance
            ```
        """
        return self._message_lbl

    @property
    def addons(self):
        """Get the dictionary of inserted addon widgets.

        Returns:
            Dictionary mapping addon names (or widget IDs) to Button or Label
            widgets that have been inserted before or after the entry using
            insert_addon().

        Example:
            ```python
            field = Field(root, label='Search')
            field.insert_addon(Button, 'after', name='search_btn', text='Go')
            search_button = field.addons['search_btn']
            search_button.configure(command=do_search)
            ```
        """
        return self._addons

    @configure_delegate
    def _config_bootstyle(self, value=None):
        if value is None:
            return self._bootstyle
        else:
            self._bootstyle = value
            self._field['bootstyle'] = self._bootstyle
        return None

    def disable(self):
        """Disable the field, preventing user input.

        Sets the entry widget and field container to disabled state. Also
        disables all addon widgets (buttons, labels). When disabled, the
        field cannot receive focus and user input is blocked.

        Example:
            ```python
            field = Field(root, label='Name')
            field.disable()  # User cannot type in the field

            # Later re-enable
            field.enable()
            ```

        Note:
            This method affects the entire field including all addons. Use
            readonly() if you want the field to remain focusable but not editable.
        """
        self._entry.state(['disabled !readonly'])
        self._field.state(['disabled'])
        for item in self._addons.values():
            try:
                item.configure(state="disabled")
            except TclError:
                pass

    def enable(self):
        """Enable the field, allowing user input.

        Removes disabled and readonly states from the entry widget and field
        container. Also enables all addon widgets. The field becomes fully
        interactive and can receive focus and user input.

        Example:
            ```python
            field = Field(root, label='Name')
            field.disable()
            # ... do something ...
            field.enable()  # User can now type again
            ```

        Note:
            This method clears both disabled and readonly states, making the
            field fully editable.
        """
        self._entry.state(['!disabled !readonly'])
        self._field.state(['!disabled'])
        for item in self._addons.values():
            try:
                item.configure(state='!disabled')
            except TclError:
                pass

    def readonly(self, value: bool = None):
        """Set or toggle the readonly state of the field.

        In readonly mode, the field can receive focus and text can be selected
        and copied, but the user cannot modify the content. The field container
        is disabled to provide visual feedback.

        Args:
            value: If True, removes readonly state (makes editable).
                If False, sets readonly state (prevents editing).
                If None, sets readonly state (default behavior).

        Example:
            ```python
            field = Field(root, label='ID', value='12345')

            # Make readonly (user can select but not edit)
            field.readonly()

            # Explicitly set readonly
            field.readonly(False)

            # Remove readonly (make editable)
            field.readonly(True)

            # Fully enable (alternative)
            field.enable()
            ```

        Note:
            Unlike disable(), readonly fields can still receive focus and allow
            text selection/copying. This is useful for displaying values that
            users should see but not modify.
        """
        if value == False:
            self._field.state(['disabled'])
            self._entry.state(['readonly'])
        elif value:
            self._field.state(['!disabled'])
            self._entry.state(['!readonly'])
        else:
            self._entry.state(['readonly !disabled'])
            self._field.state(['disabled'])

    def insert_addon(
            self,
            widget: Type[Union[Button, Label]],
            position: Literal['before', 'after'],
            name=None, pack_options: dict[str, Any] = None,
            **kwargs
    ):
        """Insert a widget addon before or after the entry input.

        Addons are Button or Label widgets positioned inside the field container,
        either before (left of) or after (right of) the entry input. Common use
        cases include search buttons, icons, clear buttons, or status indicators.

        The addon widget automatically:
        - Inherits the field's disabled state
        - Participates in focus state styling (highlights field on addon focus)
        - Is stored in the addons dictionary for later reference

        Args:
            widget: Widget class to instantiate. Must be Button or Label.
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
            **kwargs: Additional keyword arguments passed to the widget constructor.
                For Button: text, command, icon, bootstyle, etc.
                For Label: text, icon, image, bootstyle, etc.
                Note: bootstyle and takefocus are set automatically but can be
                overridden.

        Example:
            ```python
            # Search field with button
            field = Field(root, label='Search')
            field.insert_addon(
                Button,
                'after',
                name='search_btn',
                text='Go',
                command=do_search
            )
            search_btn = field.addons['search_btn']

            # Field with icon prefix
            field2 = Field(root, label='Email')
            field2.insert_addon(
                Label,
                'before',
                name='email_icon',
                icon='envelope-fill'
            )

            # Field with clear button
            field3 = Field(root, label='Name')
            field3.insert_addon(
                Button,
                'after',
                text='×',
                command=lambda: field3.delete(0, 'end')
            )

            # Addon with custom pack options
            field4 = Field(root, label='Amount')
            field4.insert_addon(
                Label,
                'before',
                text='$',
                pack_options={'padx': (5, 0)}
            )
            ```

        Note:
            Addon widgets are automatically styled with 'prefix-field' or
            'suffix-field' bootstyle. They don't accept keyboard focus by
            default (takefocus=False) but can trigger field focus state styling.
        """
        bootstyle = "suffix-field" if position == "after" else "prefix-field"
        kwargs.update(bootstyle=bootstyle, takefocus=False)
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
        if 'disabled' in self._entry.state():
            try:
                instance.configure(state="disabled")
            except TclError:
                pass

        # bind focus events to field frame
        instance.bind('<FocusIn>', lambda _: self._field.state(['focus']), add=True)
        instance.bind('<FocusOut>', lambda _: self._field.state(['!focus']), add=True)

    def _show_error(self, event: Any) -> None:
        """Display a validation error message below the input field.

        Called automatically when the <<Invalid>> event is triggered by the
        underlying entry widget. Updates the message label to show the error
        message with danger styling.

        Args:
            event: Event object with data attribute containing validation info.
                event.data['message'] contains the error message to display.

        Note:
            This is an internal method bound to the <<Invalid>> event. It
            temporarily replaces the normal message text with the error message
            until validation passes.
        """
        self._message_lbl['text'] = event.data['message']
        self._message_lbl['bootstyle'] = "danger"
        self._message_lbl.pack(side='top', after=self._field, padx=4)

    def _clear_error(self, _: Any) -> None:
        """Clear the error message and restore the original message text.

        Called automatically when the <<Valid>> event is triggered by the
        underlying entry widget. Restores the message label to show the
        original message text with secondary styling.

        Args:
            _: Event object (unused).

        Note:
            This is an internal method bound to the <<Valid>> event. It
            restores the message area to its normal state after an error
            has been corrected.
        """
        self._message_lbl['text'] = self._message_text
        self._message_lbl['bootstyle'] = "secondary"
