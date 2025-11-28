"""Password entry field widget with visibility toggle.

Provides a specialized text entry field for password input with masked characters
and an optional visibility toggle button.
"""

from ttkbootstrap.widgets.button import Button
from ttkbootstrap.widgets.field import Field, FieldOptions
from typing_extensions import Unpack


class PasswordEntry(Field):
    """A password entry field widget with masked input and visibility toggle.

    PasswordEntry extends the Field widget to provide password-specific functionality,
    including character masking and a toggle button to temporarily reveal the password.
    The widget automatically inserts a visibility toggle button (eye icon) that shows
    the password while pressed and hides it when released.

    Features:
        - Automatic character masking (default: '•')
        - Press-and-hold visibility toggle button
        - Customizable mask character
        - All Field features (label, validation, messages, etc.)
        - Toggle button can be shown/hidden programmatically

    Events (inherited from Field):
        <<Input>>: Triggered on each keystroke
        <<Changed>>: Triggered when value changes after commit
        <<Valid>>: Triggered when validation passes
        <<Invalid>>: Triggered when validation fails
        <<Validated>>: Triggered after any validation

    Example:
        ```python
        import ttkbootstrap as ttk
        from ttkbootstrap.widgets.passwordentry import PasswordEntry

        root = ttk.Window()

        # Basic password entry
        password = PasswordEntry(
            root,
            label="Password",
            required=True,
            message="Enter your password"
        )
        password.pack(padx=20, pady=10, fill='x')

        # Custom mask character
        password2 = PasswordEntry(
            root,
            label="PIN",
            show='*',
            message="4-digit PIN"
        )
        password2.pack(padx=20, pady=10, fill='x')

        # Without visibility toggle
        password3 = PasswordEntry(
            root,
            label="Secret",
            show_visible_toggle=False
        )
        password3.pack(padx=20, pady=10, fill='x')

        # With validation
        password4 = PasswordEntry(root, label="Password", required=True)
        password4.add_validation_rule(
            'stringLength',
            min=8,
            message='Password must be at least 8 characters'
        )
        password4.pack(padx=20, pady=10, fill='x')

        root.mainloop()
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
            self,
            master=None,
            value: str = None,
            label: str = None,
            message: str = None,
            show_visible_toggle: bool = True,
            **kwargs: Unpack[FieldOptions]):
        """Initialize a PasswordEntry widget.

        Creates a password entry field with character masking and an optional
        visibility toggle button. The widget automatically masks input characters
        (default: '•') and provides a button to temporarily reveal the password
        while pressed.

        Args:
            master: Parent widget. If None, uses the default root window.
            value: Initial password value to display (masked). Default is None.
            label: Optional label text to display above the entry field.
                If required=True, an asterisk (*) is automatically appended.
            message: Optional message text to display below the entry field.
                Used for hints or help text. Replaced by validation errors when
                validation fails.
            show_visible_toggle: If True, displays the visibility toggle button
                (eye icon) that reveals the password while pressed. If False,
                hides the toggle button. Default is True.
            **kwargs: Additional keyword arguments from FieldOptions:
                show: Character to mask password input. Default is '•'. Can be
                    customized to any character (e.g., '*', '●', etc.)
                required: If True, field cannot be empty
                bootstyle: The accent color of the focus ring and active border
                allow_blank: Allow empty input
                cursor: Cursor style when hovering
                value_format: ICU format pattern for parsing/formatting
                exportselection: Export selection to clipboard
                font: Font for text display
                foreground: Text color
                initial_focus: If True, widget receives focus on creation
                justify: Text alignment
                show_message: If True, displays message area
                padding: Padding around entry widget
                take_focus: If True, widget accepts Tab focus
                textvariable: Tkinter Variable to link with text
                textsignal: Signal object for reactive updates
                width: Width in characters
                xscrollcommand: Callback for horizontal scrolling

        Note:
            The visibility toggle button uses a press-and-hold interaction.
            The password is only visible while the button is actively pressed,
            providing a secure way to verify input without leaving it exposed.
        """
        # set default mask if not provided
        self._show_indicator = kwargs.get('show', '•')
        kwargs.setdefault('show', self._show_indicator)
        super().__init__(master, value=value, label=label, message=message, **kwargs)

        # configuration
        self._show_visible_toggle = show_visible_toggle
        self._show_visible_pack = {}

        self.insert_addon(
            Button,
            position="after",
            name="visibility",
            icon={"name": "eye", "state": [("pressed", "eye-slash")]},
            compound="image",
            style_options={"icon_only": True}
        )
        addon = self.addons['visibility']
        addon.bind('<ButtonPress>', self._show_password, add=True)
        addon.bind('<ButtonRelease>', self._hide_password, add=True)

    @property
    def _visibility_toggle(self):
        """Get the visibility toggle button widget."""
        return self.addons['visibility']

    def _show_password(self, _):
        """Reveal the password by removing character masking."""
        self.entry_widget['show'] = ''

    def _hide_password(self, _):
        """Hide the password by restoring character masking."""
        self.entry_widget['show'] = self._show_indicator

    def show_visible_toggle(self, value: bool):
        """Show or hide the visibility toggle button."""
        if value and not self._visibility_toggle.winfo_ismapped():
            self._visibility_toggle.pack(**self._show_visible_pack)
        else:
            self._show_visible_pack = self._visibility_toggle.pack_info()
            self._visibility_toggle.pack_forget()
