"""Password entry field widget with visibility toggle.

Provides a specialized text entry field for password input with masked characters
and an optional visibility toggle button.
"""

from ttkbootstrap.widgets.primitives.button import Button
from ttkbootstrap.widgets.composites.field import Field, FieldOptions
from ttkbootstrap.widgets.types import Master
from typing_extensions import Unpack


class PasswordEntry(Field):
    """A password entry field widget with masked input and visibility toggle.

    PasswordEntry extends the Field widget to provide password-specific functionality,
    including character masking and a toggle button to temporarily reveal the password.
    The widget automatically inserts a visibility toggle button (eye icon) that shows
    the password while pressed and hides it when released.

    !!! note "Events"

        - ``<<Input>>``: Triggered on each keystroke.
        - ``<<Change>>``: Triggered when value changes after commit.
        - ``<<Valid>>``: Triggered when validation passes.
        - ``<<Invalid>>``: Triggered when validation fails.
        - ``<<Validate>>``: Triggered after any validation.

    Attributes:
        entry_widget (TextEntryPart): The underlying text entry widget.
        label_widget (Label): The label widget above the entry.
        message_widget (Label): The message label widget below the entry.
        addons (dict[str, Widget]): Dictionary of inserted addon widgets by name.
        variable (Variable): Tkinter Variable linked to entry text.
        signal (Signal): Signal object for reactive updates.
    """

    def __init__(
            self,
            master: Master = None,
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
                (eye icon) that reveals the password while pressed. Default is True.

        Other Parameters:
            show (str): Character to mask password input. Default is '•'.
            required (bool): If True, field cannot be empty.
            bootstyle (str): The accent color of the focus ring and active border.
            allow_blank (bool): Allow empty input.
            cursor (str): Cursor style when hovering.
            font (str): Font for text display.
            foreground (str): Text color.
            initial_focus (bool): If True, widget receives focus on creation.
            justify (str): Text alignment.
            show_message (bool): If True, displays message area.
            padding (str): Padding around entry widget.
            take_focus (bool): If True, widget accepts Tab focus.
            textvariable (Variable): Tkinter Variable to link with text.
            textsignal (Signal): Signal object for reactive updates.
            width (int): Width in characters.

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
            icon_only=True
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

