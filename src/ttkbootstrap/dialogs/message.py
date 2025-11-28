"""Message dialogs and messagebox facade for ttkbootstrap."""

import logging
import textwrap
import tkinter
from typing import Any, Callable, List, Optional

import ttkbootstrap as ttk
from ttkbootstrap.appconfig import use_icon_provider
from ttkbootstrap.constants import *
from ttkbootstrap.localization import MessageCatalog
from .base import Dialog

logger = logging.getLogger(__name__)


class MessageDialog(Dialog):
    """A simple modal dialog class that can be used to build simple
    message dialogs.

    Displays a message and a set of buttons. Each of the buttons in the
    message window is identified by a unique symbolic name. After the
    message window is popped up, the message box awaits for the user to
    select one of the buttons. Then it returns the symbolic name of the
    selected button. Use a `Toplevel` widget for more advanced modal
    dialog designs.
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
        super().__init__(master, title, alert)
        self._message = message
        self._command = command
        self._width = width
        self._default = default
        self._padding = padding
        self._icon = icon
        self._localize = kwargs.get("localize")

        if buttons is None:
            self._buttons = [
                f"{MessageCatalog.translate('Cancel')}",
                f"{MessageCatalog.translate('OK')}",
            ]
        else:
            self._buttons = buttons

    def create_body(self, master: tkinter.Misc) -> None:
        """Create the message body with optional icon."""
        container = ttk.Frame(master, padding=self._padding)

        if self._icon:
            try:
                icon_provider = use_icon_provider()

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
                        icon_image = icon_provider(icon_name, icon_size, icon_color)
                    else:
                        icon_image = icon_provider(icon_name, icon_size)

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

    def create_buttonbox(self, master: tkinter.Misc) -> None:
        """Create the button box with configured buttons."""
        # Add separator above buttons
        ttk.Separator(master).pack(fill=X)

        # Create button frame
        frame = ttk.Frame(master, padding=(5, 5))
        frame.pack(side=BOTTOM, fill=X, anchor=S)

        button_list: list[ttk.Button] = []

        for i, button in enumerate(self._buttons[::-1]):
            cnf = button.split(":")
            text = cnf[0]

            is_default = False
            if self._default is not None and text == self._default:
                is_default = True
            elif self._default is None and i == 0:
                is_default = True

            if len(cnf) == 2:
                bootstyle = cnf[1]
            elif is_default:
                bootstyle = "primary"
            else:
                bootstyle = "secondary"

            if self._localize is True:
                text = MessageCatalog.translate(text)

            btn = ttk.Button(frame, bootstyle=bootstyle, text=text, padding=(10, 5))
            btn.configure(command=lambda b=btn: self._on_button_press(b))
            btn.pack(padx=2, side=RIGHT)
            btn.lower()  # set focus traversal left-to-right
            button_list.append(btn)

            if is_default:
                self._initial_focus = btn

            # Bind return key to button
            btn.bind("<Return>", lambda _, b=btn: b.invoke())
            btn.bind("<KP_Enter>", lambda _, b=btn: b.invoke())

        # Bind arrow keys for navigation
        for index, btn in enumerate(button_list):
            if index > 0:
                nbtn = button_list[index - 1]
                btn.bind("<Right>", lambda _, b=nbtn: b.focus_set())
            if index < len(button_list) - 1:
                nbtn = button_list[index + 1]
                btn.bind("<Left>", lambda _, b=nbtn: b.focus_set())

        if not self._initial_focus:
            self._initial_focus = button_list[0]

    def _on_button_press(self, button: ttk.Button) -> None:
        """Save result and close dialog."""
        self._result = button["text"]
        if self._command is not None:
            self._command()
        self.destroy()


class Messagebox:
    """Static methods for displaying standard message dialogs."""

    @staticmethod
    def _show(
            message: str,
            title: str = " ",
            master: Optional[tkinter.Misc] = None,
            alert: bool = False,
            buttons: Optional[List[str]] = None,
            icon: Optional[str] = None,
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
        return Messagebox._show(message, title, master, alert, ["OK:primary"], "info-circle-fill", **kwargs)

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
        return Messagebox._show(message, title, master, alert, ["OK:primary"], "exclamation-triangle-fill", **kwargs)

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
        return Messagebox._show(message, title, master, alert, ["OK:primary"], "x-circle-fill", **kwargs)

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
        return Messagebox._show(message, title, master, alert, ["OK:primary"], "question-circle-fill", **kwargs)

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
        return Messagebox._show(message, title, master, alert, ["OK:primary"], None, **kwargs)

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
        return Messagebox._show(message, title, master, alert, ["Cancel", "OK"], None, **kwargs)

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
        return Messagebox._show(message, title, master, alert, ["No", "Yes"], None, **kwargs)

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
        return Messagebox._show(message, title, master, alert, ["Cancel", "No", "Yes"], None, **kwargs)

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
        return Messagebox._show(message, title, master, alert, ["Cancel", "Retry"], None, **kwargs)
