"""Message dialogs and messagebox facade for ttkbootstrap."""

import textwrap
import tkinter
from typing import Any, Callable, List, Optional, Tuple

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.icons import Icon
from ttkbootstrap.localization import MessageCatalog
from .base import Dialog


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
            command: Optional[Tuple[Callable[..., Any], str]] = None,
            width: int = 50,
            parent: Optional[tkinter.Misc] = None,
            alert: bool = False,
            default: Optional[str] = None,
            padding: "tuple[int, int] | int" = (20, 20),
            icon: Optional[str] = None,
            **kwargs: Any,
    ) -> None:
        """Create a message dialog.

        Parameters:

            message (str):
                The message text to display. Supports multiline strings
                (separated by \\n).

            title (str):
                The dialog window title (default=' ').

            buttons (List[str]):
                List of button labels. Each button can optionally specify
                a bootstyle using "label:bootstyle" format (e.g., "OK:primary").
                If None, defaults to ["Cancel", "OK"]. The buttons are
                displayed in reverse order (rightmost first).

            command (Callable):
                Optional callback function to execute when a button is pressed.

            width (int):
                Maximum width in characters for text wrapping (default=50).

            parent (Widget):
                Parent widget. The dialog will be centered on this widget.

            alert (bool):
                If True, rings the system bell when the dialog is shown
                (default=False).

            default (str):
                The button label to use as the default (receives primary
                bootstyle and initial focus). If None, the rightmost button
                becomes the default.

            padding (int | tuple):
                Padding around the message content. Can be a single int or
                tuple (horizontal, vertical) (default=(20, 20)).

            icon (str):
                Optional icon to display. Can be image data, file path,
                or Icon constant (e.g., Icon.info).

            **kwargs (Dict):
                Additional keyword arguments. Supports 'localize' (bool)
                to enable message translation.
        """
        super().__init__(parent, title, alert)
        self._message = message
        self._command: Optional[Tuple[Callable[..., Any], str]] = command
        self._width = width
        self._alert = alert
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
        """Overrides the parent method; adds the message section."""
        container = ttk.Frame(master, padding=self._padding)
        if self._icon:
            try:
                # assume this is image data
                self._img = ttk.PhotoImage(data=self._icon)
                icon_lbl = ttk.Label(container, image=self._img)
                icon_lbl.pack(side=LEFT, anchor=N, padx=(0, 5))
            except Exception:
                try:
                    # assume this is a file path
                    self._img = ttk.PhotoImage(file=self._icon)
                    icon_lbl = ttk.Label(container, image=self._img)
                    icon_lbl.pack(side=LEFT, anchor=N, padx=(0, 5))
                except Exception:
                    # icon is neither data nor a valid file path
                    print("MessageDialog icon is invalid")

        if self._message:
            for msg in self._message.split("\n"):
                message = "\n".join(textwrap.wrap(msg, width=self._width))
                message_label = ttk.Label(container, text=message)
                message_label.pack(pady=(0, 3), fill=X, anchor=N)
        container.pack(fill=X, expand=True)

    def create_buttonbox(self, master: tkinter.Misc) -> None:
        """Overrides the parent method; adds the message buttonbox"""
        frame = ttk.Frame(master, padding=(5, 5))

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

            btn = ttk.Button(frame, bootstyle=bootstyle, text=text)
            btn.configure(command=lambda b=btn: self.on_button_press(b))
            btn.pack(padx=2, side=RIGHT)
            btn.lower()  # set focus traversal left-to-right
            button_list.append(btn)

            if is_default:
                self._initial_focus = btn

            # bind default button to return key press and set focus
            btn.bind("<Return>", lambda _, b=btn: b.invoke())
            btn.bind("<KP_Enter>", lambda _, b=btn: b.invoke())

        for index, btn in enumerate(button_list):
            if index > 0:
                nbtn = button_list[index - 1]
                btn.bind("<Right>", lambda _, b=nbtn: b.focus_set())
            if index < len(button_list) - 1:
                nbtn = button_list[index + 1]
                btn.bind("<Left>", lambda _, b=nbtn: b.focus_set())

        ttk.Separator(self._toplevel).pack(fill=X)
        frame.pack(side=BOTTOM, fill=X, anchor=S)

        if not self._initial_focus:
            self._initial_focus = button_list[0]

    def on_button_press(self, button: ttk.Button) -> None:
        """Save result, destroy the toplevel, and execute command."""
        self._result = button["text"]
        command = self._command
        if command is not None:
            command()
        self._toplevel.after_idle(self._toplevel.destroy)

    def show(self, position: Optional[Tuple[int, int]] = None, wait_for_result: bool = True) -> None:
        """Create and display the popup messagebox."""
        super().show(position, wait_for_result=wait_for_result)


class Messagebox:
    """This class contains various static methods that show popups with
    a message to the end user with various arrangments of buttons
    and alert options."""

    @staticmethod
    def show_info(
            message: str,
            title: str = " ",
            parent: Optional[tkinter.Misc] = None,
            alert: bool = False,
            **kwargs: Any,
    ) -> Optional[str]:
        """Display a modal dialog box with an OK button and an INFO icon."""
        position = kwargs.pop("position", None)
        buttons = kwargs.pop("buttons", ["OK:primary"])
        icon = kwargs.pop("icon", Icon.info)
        localize = kwargs.pop("localize", True)
        dialog = MessageDialog(
            message=message,
            title=title,
            alert=alert,
            parent=parent,
            buttons=buttons,
            icon=icon,
            localize=localize,
            **kwargs,
        )
        dialog.show(position)
        return dialog.result

    @staticmethod
    def show_warning(
            message: str,
            title: str = " ",
            parent: Optional[tkinter.Misc] = None,
            alert: bool = True,
            **kwargs: Any,
    ) -> Optional[str]:
        """Display a modal dialog box with an OK button and a warning icon."""
        position = kwargs.pop("position", None)
        buttons = kwargs.pop("buttons", ["OK:primary"])
        icon = kwargs.pop("icon", Icon.warning)
        localize = kwargs.pop("localize", True)
        dialog = MessageDialog(
            message=message,
            title=title,
            parent=parent,
            buttons=buttons,
            icon=icon,
            alert=alert,
            localize=localize,
            **kwargs,
        )
        dialog.show(position)
        return dialog.result

    @staticmethod
    def show_error(
            message: str,
            title: str = " ",
            parent: Optional[tkinter.Misc] = None,
            alert: bool = True,
            **kwargs: Any,
    ) -> Optional[str]:
        """Display a modal dialog box with an OK button and an error icon."""
        position = kwargs.pop("position", None)
        buttons = kwargs.pop("buttons", ["OK:primary"])
        icon = kwargs.pop("icon", Icon.error)
        localize = kwargs.pop("localize", True)
        dialog = MessageDialog(
            message=message,
            title=title,
            parent=parent,
            buttons=buttons,
            icon=icon,
            alert=alert,
            localize=localize,
            **kwargs,
        )
        dialog.show(position)
        return dialog.result

    @staticmethod
    def show_question(
            message: str,
            title: str = " ",
            parent: Optional[tkinter.Misc] = None,
            alert: bool = False,
            **kwargs: Any,
    ) -> Optional[str]:
        """Display a modal dialog box with an OK button and a question icon."""
        position = kwargs.pop("position", None)
        buttons = kwargs.pop("buttons", ["OK:primary"])
        icon = kwargs.pop("icon", Icon.question)
        localize = kwargs.pop("localize", True)
        dialog = MessageDialog(
            message=message,
            title=title,
            parent=parent,
            buttons=buttons,
            icon=icon,
            alert=alert,
            localize=localize,
            **kwargs,
        )
        dialog.show(position)
        return dialog.result

    @staticmethod
    def ok(
            message: str,
            title: str = " ",
            parent: Optional[tkinter.Misc] = None,
            alert: bool = False,
            **kwargs: Any,
    ) -> Optional[str]:
        position = kwargs.pop("position", None)
        buttons = kwargs.pop("buttons", ["OK:primary"])
        localize = kwargs.pop("localize", True)
        dialog = MessageDialog(
            title=title,
            message=message,
            parent=parent,
            alert=alert,
            buttons=buttons,
            localize=localize,
            **kwargs,
        )
        dialog.show(position)
        return dialog.result

    @staticmethod
    def okcancel(
            message: str,
            title: str = " ",
            alert: bool = False,
            parent: Optional[tkinter.Misc] = None,
            **kwargs: Any,
    ) -> Optional[str]:
        position = kwargs.pop("position", None)
        localize = kwargs.pop("localize", True)
        dialog = MessageDialog(
            title=title,
            message=message,
            parent=parent,
            alert=alert,
            localize=localize,
            **kwargs,
        )
        dialog.show(position)
        return dialog.result

    @staticmethod
    def yesno(
            message: str,
            title: str = " ",
            alert: bool = False,
            parent: Optional[tkinter.Misc] = None,
            **kwargs: Any,
    ) -> Optional[str]:
        position = kwargs.pop("position", None)
        buttons = kwargs.pop("buttons", ["No", "Yes"])
        localize = kwargs.pop("localize", True)
        dialog = MessageDialog(
            title=title,
            message=message,
            parent=parent,
            buttons=buttons,
            alert=alert,
            localize=localize,
            **kwargs,
        )
        dialog.show(position)
        return dialog.result

    @staticmethod
    def yesnocancel(
            message: str,
            title: str = " ",
            alert: bool = False,
            parent: Optional[tkinter.Misc] = None,
            **kwargs: Any,
    ) -> Optional[str]:
        position = kwargs.pop("position", None)
        buttons = kwargs.pop("buttons", ["Cancel", "No", "Yes"])
        localize = kwargs.pop("localize", True)
        dialog = MessageDialog(
            title=title,
            message=message,
            parent=parent,
            alert=alert,
            buttons=buttons,
            localize=localize,
            **kwargs,
        )
        dialog.show(position)
        return dialog.result

    @staticmethod
    def retrycancel(
            message: str,
            title: str = " ",
            alert: bool = False,
            parent: Optional[tkinter.Misc] = None,
            **kwargs: Any,
    ) -> Optional[str]:
        position = kwargs.pop("position", None)
        buttons = kwargs.pop("buttons", ["Cancel", "Retry"])
        localize = kwargs.pop("localize", True)
        dialog = MessageDialog(
            title=title,
            message=message,
            parent=parent,
            alert=alert,
            buttons=buttons,
            localize=localize,
            **kwargs,
        )
        dialog.show(position)
        return dialog.result
