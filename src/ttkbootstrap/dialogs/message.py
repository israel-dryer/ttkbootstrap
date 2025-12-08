"""Message dialogs and messagebox facade for ttkbootstrap."""

import logging
import textwrap
import tkinter
from typing import Any, Callable, List, Optional

import ttkbootstrap as ttk
from ttkbootstrap_icons_bs import BootstrapIcon
from ttkbootstrap.constants import *
from ttkbootstrap.localization import MessageCatalog
from .dialog import ButtonRole, Dialog, DialogButton

logger = logging.getLogger(__name__)


class MessageDialog:
    """A simple modal dialog class that can be used to build simple
    message dialogs.

    Displays a message and a set of buttons. Each of the buttons in the
    message window is identified by a unique symbolic name. After the
    message window is popped up, the message box awaits for the user to
    select one of the buttons. Then it returns the symbolic name of the
    selected button. Use a `Toplevel` widget for more advanced modal
    dialog designs.

    Emits:
        ``<<DialogResult>>`` with ``event.data = {"result": <str>, "confirmed": True}``.
    """

    def __init__(
            self,
            message: str,
            title: str = " ",
            buttons: Optional[List[str]] = None,
            command: Optional[Callable[[], None]] = None,
            width: int = 50,
            master: Optional[tkinter.Misc] = None,
            alert: bool = False,
            default: Optional[str] = None,
            padding: tuple[int, int] | int = (20, 20),
            icon: Optional[str | dict] = None,
            **kwargs: Any,
    ) -> None:
        """Create a message dialog.

        Args:
            message: The message text to display. Supports multiline strings.
            title: The dialog window title.
            buttons: List of button labels. Can specify bootstyle as "label:bootstyle".
                If None, defaults to ["Cancel", "OK"].
            command: Optional callback function to execute when any button is pressed.
            width: Maximum width in characters for text wrapping.
            master: Parent widget for the dialog.
            alert: If True, rings the system bell when shown.
            default: The button label to use as default. Receives primary bootstyle and focus.
            padding: Padding around the message content.
            icon: Optional icon specification. Can be a string (icon name) or dict with
                keys: 'name' (required), 'size' (default 32), 'color' (optional).
            **kwargs: Additional keyword arguments. Supports 'localize' to enable translation.
        """
        self._message = message
        self._command = command
        self._width = width
        self._padding = padding
        self._icon = icon
        self._localize = kwargs.get("localize")
        self._img = None  # Store icon image to prevent garbage collection

        if buttons is None:
            button_labels = [
                f"{MessageCatalog.translate('Cancel')}",
                f"{MessageCatalog.translate('OK')}",
            ]
        else:
            button_labels = buttons

        # Parse button labels and create DialogButton specs
        button_specs = self._parse_buttons(button_labels, default)

        # Create the underlying dialog
        self._dialog = Dialog(
            master=master,
            title=title,
            content_builder=self._create_content,
            buttons=button_specs,
            alert=alert,
            minsize=(300, 100),
        )
        self._master = master

    def _create_content(self, parent: tkinter.Widget) -> None:
        """Create the message body with optional icon."""
        container = ttk.Frame(parent, padding=self._padding)

        if self._icon:
            try:
                # Parse icon specification - initialize variables
                icon_name: Optional[str] = None
                icon_size: int = 32
                icon_color: Optional[str] = None

                if isinstance(self._icon, str):
                    icon_name = self._icon
                elif isinstance(self._icon, dict):
                    icon_name = self._icon.get("name")
                    icon_size = self._icon.get("size", 32)
                    icon_color = self._icon.get("color")
                else:
                    logger.warning("Invalid icon specification: %s", self._icon)

                # Generate icon image
                if icon_name:
                    if icon_color:
                        icon_image = BootstrapIcon(icon_name, icon_size, icon_color).image
                    else:
                        icon_image = BootstrapIcon(icon_name, icon_size).image

                    self._img = icon_image
                    icon_lbl = ttk.Label(container, image=self._img)
                    icon_lbl.pack(side=LEFT, anchor=N, padx=(0, 10))

            except Exception as e:
                logger.warning("Failed to create icon: %s", e)

        if self._message:
            for msg in self._message.split("\n"):
                message = "\n".join(textwrap.wrap(msg, width=self._width))
                message_label = ttk.Label(container, text=message)
                message_label.pack(pady=(0, 3), fill=X, anchor=N)
        container.pack(fill=X, expand=True)

    def _parse_buttons(self, button_labels: List[str], default: Optional[str]) -> List[DialogButton]:
        """Parse button label strings into DialogButton specifications."""
        button_specs: List[DialogButton] = []

        for i, button in enumerate(button_labels):
            # Parse "text:bootstyle" format
            cnf = button.split(":")
            text = cnf[0]

            # Apply localization if enabled
            if self._localize:
                text = MessageCatalog.translate(text)

            # Determine if this is the default button
            is_default = (text == default) if default else (i == len(button_labels) - 1)

            # Parse or infer bootstyle
            if len(cnf) == 2:
                bootstyle = cnf[1]
            elif is_default:
                bootstyle = "primary"
            else:
                bootstyle = "secondary"

            # Determine button role
            role: ButtonRole
            if bootstyle == "primary":
                role = "primary"
            elif i == 0 and "cancel" in text.lower():
                role = "cancel"
            else:
                role = "secondary"

            # Create button specification
            button_specs.append(
                DialogButton(
                    text=text,
                    role=role,
                    result=text,
                    bootstyle=bootstyle if bootstyle != role else None,
                    default=is_default,
                    command=self._make_command_callback() if self._command else None,
                )
            )

        return button_specs

    def _make_command_callback(self) -> Callable[[Dialog], None]:
        """Create a callback wrapper for the custom command."""

        def callback(dialog: Dialog) -> None:
            if self._command:
                self._command()

        return callback

    def show(self, position: Optional[tuple[int, int]] = None) -> None:
        """Show the dialog.

        Args:
            position: x and y coordinates to position the dialog. If None, centers on parent.
        """
        self._dialog.show(position=position, modal=True)
        target = self._dialog.toplevel or self._master
        if target:
            payload = {"result": self._dialog.result, "confirmed": self._dialog.result is not None}
            try:
                target.event_generate("<<DialogResult>>", data=payload)
            except Exception:
                try:
                    target.event_generate("<<DialogResult>>")
                except Exception:
                    pass

    @property
    def result(self) -> Any:
        """The dialog result value (the text of the button pressed)."""
        return self._dialog.result

    def on_dialog_result(self, callback: Callable[[Any], None]) -> Optional[str]:
        """Bind a callback fired when the dialog produces a result.

        The callback receives ``event.data["result"]`` when available.

        Args:
            callback: Callable that receives the result payload.

        Returns:
            Binding identifier for use with ``off_dialog_result``.
        """
        target = self._dialog.toplevel or self._master
        if target is None:
            return None

        def handler(event):
            callback(getattr(event, "data", None))

        return target.bind("<<DialogResult>>", handler, add="+")

    def off_dialog_result(self, funcid: str) -> None:
        """Unbind a previously bound dialog result callback."""
        target = self._dialog.toplevel or self._master
        if target is None:
            return
        target.unbind("<<DialogResult>>", funcid)


class MessageBox:
    """Static methods for displaying standard message dialogs."""

    @staticmethod
    def _show(
            message: str,
            title: str = " ",
            master: Optional[tkinter.Misc] = None,
            alert: bool = False,
            buttons: Optional[List[str]] = None,
            icon: Optional[str] = None,
            on_result: Optional[Callable[[Any], None]] = None,
            **kwargs: Any,
    ) -> Optional[str]:
        """Internal helper to show a message dialog.

        Args:
            message: The message text to display.
            title: The dialog window title.
            master: Parent widget for the dialog.
            alert: If True, rings the system bell.
            buttons: List of button labels.
            icon: Optional icon to display.
            on_result: Optional callback receiving the dialog result payload.
            **kwargs: Additional arguments including 'position'.

        Returns:
            The text of the button pressed, or None.
        """
        position = kwargs.pop("position", None)
        dialog = MessageDialog(
            message=message,
            title=title,
            master=master,
            alert=alert,
            buttons=buttons,
            icon=icon,
            localize=True,
            **kwargs,
        )
        if on_result:
            dialog.on_dialog_result(on_result)
        dialog.show(position)
        return dialog.result

    @staticmethod
    def show_info(
            message: str,
            title: str = " ",
            master: Optional[tkinter.Misc] = None,
            alert: bool = False,
            **kwargs: Any,
    ) -> Optional[str]:
        """Display an info dialog with OK button and info icon.

        Args:
            message: The message text to display.
            title: The dialog window title.
            master: Parent widget for the dialog.
            alert: If True, rings the system bell.
            **kwargs: Additional arguments including 'position'.

        Returns:
            The text of the button pressed.
        """
        return MessageBox._show(message, title, master, alert, ["OK:primary"], "info-circle-fill", **kwargs)

    @staticmethod
    def show_warning(
            message: str,
            title: str = " ",
            master: Optional[tkinter.Misc] = None,
            alert: bool = True,
            **kwargs: Any,
    ) -> Optional[str]:
        """Display a warning dialog with OK button and warning icon.

        Args:
            message: The message text to display.
            title: The dialog window title.
            master: Parent widget for the dialog.
            alert: If True, rings the system bell.
            **kwargs: Additional arguments including 'position'.

        Returns:
            The text of the button pressed.
        """
        return MessageBox._show(message, title, master, alert, ["OK:primary"], "exclamation-triangle-fill", **kwargs)

    @staticmethod
    def show_error(
            message: str,
            title: str = " ",
            master: Optional[tkinter.Misc] = None,
            alert: bool = True,
            **kwargs: Any,
    ) -> Optional[str]:
        """Display an error dialog with OK button and error icon.

        Args:
            message: The message text to display.
            title: The dialog window title.
            master: Parent widget for the dialog.
            alert: If True, rings the system bell.
            **kwargs: Additional arguments including 'position'.

        Returns:
            The text of the button pressed.
        """
        return MessageBox._show(message, title, master, alert, ["OK:primary"], "x-circle-fill", **kwargs)

    @staticmethod
    def show_question(
            message: str,
            title: str = " ",
            master: Optional[tkinter.Misc] = None,
            alert: bool = False,
            **kwargs: Any,
    ) -> Optional[str]:
        """Display a question dialog with OK button and question icon.

        Args:
            message: The message text to display.
            title: The dialog window title.
            master: Parent widget for the dialog.
            alert: If True, rings the system bell.
            **kwargs: Additional arguments including 'position'.

        Returns:
            The text of the button pressed.
        """
        return MessageBox._show(message, title, master, alert, ["OK:primary"], "question-circle-fill", **kwargs)

    @staticmethod
    def ok(
            message: str,
            title: str = " ",
            master: Optional[tkinter.Misc] = None,
            alert: bool = False,
            **kwargs: Any,
    ) -> Optional[str]:
        """Display a dialog with an OK button.

        Args:
            message: The message text to display.
            title: The dialog window title.
            master: Parent widget for the dialog.
            alert: If True, rings the system bell.
            **kwargs: Additional arguments including 'position'.

        Returns:
            The text of the button pressed.
        """
        return MessageBox._show(message, title, master, alert, ["OK:primary"], None, **kwargs)

    @staticmethod
    def okcancel(
            message: str,
            title: str = " ",
            master: Optional[tkinter.Misc] = None,
            alert: bool = False,
            **kwargs: Any,
    ) -> Optional[str]:
        """Display a dialog with OK and Cancel buttons.

        Args:
            message: The message text to display.
            title: The dialog window title.
            master: Parent widget for the dialog.
            alert: If True, rings the system bell.
            **kwargs: Additional arguments including 'position'.

        Returns:
            The text of the button pressed.
        """
        return MessageBox._show(message, title, master, alert, ["Cancel", "OK"], None, **kwargs)

    @staticmethod
    def yesno(
            message: str,
            title: str = " ",
            master: Optional[tkinter.Misc] = None,
            alert: bool = False,
            **kwargs: Any,
    ) -> Optional[str]:
        """Display a dialog with Yes and No buttons.

        Args:
            message: The message text to display.
            title: The dialog window title.
            master: Parent widget for the dialog.
            alert: If True, rings the system bell.
            **kwargs: Additional arguments including 'position'.

        Returns:
            The text of the button pressed.
        """
        return MessageBox._show(message, title, master, alert, ["No", "Yes"], None, **kwargs)

    @staticmethod
    def yesnocancel(
            message: str,
            title: str = " ",
            master: Optional[tkinter.Misc] = None,
            alert: bool = False,
            **kwargs: Any,
    ) -> Optional[str]:
        """Display a dialog with Yes, No, and Cancel buttons.

        Args:
            message: The message text to display.
            title: The dialog window title.
            master: Parent widget for the dialog.
            alert: If True, rings the system bell.
            **kwargs: Additional arguments including 'position'.

        Returns:
            The text of the button pressed.
        """
        return MessageBox._show(message, title, master, alert, ["Cancel", "No", "Yes"], None, **kwargs)

    @staticmethod
    def retrycancel(
            message: str,
            title: str = " ",
            master: Optional[tkinter.Misc] = None,
            alert: bool = False,
            **kwargs: Any,
    ) -> Optional[str]:
        """Display a dialog with Retry and Cancel buttons.

        Args:
            message: The message text to display.
            title: The dialog window title.
            master: Parent widget for the dialog.
            alert: If True, rings the system bell.
            **kwargs: Additional arguments including 'position'.

        Returns:
            The text of the button pressed.
        """
        return MessageBox._show(message, title, master, alert, ["Cancel", "Retry"], None, **kwargs)
