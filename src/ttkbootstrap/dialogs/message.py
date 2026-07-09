"""Message dialogs and messagebox facade for ttkbootstrap."""

import textwrap
import tkinter
from typing import Any, Callable, List, Optional, Tuple

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.localization import MessageCatalog
from ttkbootstrap.style._compat import warn_deprecated
from .base import Dialog


# The default alert glyphs for the four Messagebox.show_* dialogs, rendered from
# the built-in Bootstrap-Icons font (theme-matched and recolorable). Replaces the
# base64 PNG constants from the removed ``ttkbootstrap.icons`` module (2.0).
_ALERT_ICON_SIZE = 30
_ALERT_ICONS = {
    "info": ("info-circle-fill", "info"),
    "warning": ("exclamation-triangle-fill", "warning"),
    "error": ("x-circle-fill", "danger"),
    "question": ("question-circle-fill", "info"),
}


def _alert_icon(kind: str) -> str:
    """Render one alert glyph to a cached Tk image name (see ``_ALERT_ICONS``)."""
    name, color = _ALERT_ICONS[kind]
    return ttk.Icon(name, _ALERT_ICON_SIZE, color)


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
            command: Optional[Callable[[], Any]] = None,
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
                Optional zero-argument callback to run when a button is
                pressed. The legacy ``(callable, label)`` tuple form is
                deprecated (the label was never used) and will be removed in
                3.0; pass the callable directly.

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
                Optional icon to display. Can be an already-rendered Tk image
                name (e.g. from ``ttk.Icon(...)``), base64 image data, or a
                file path.

            **kwargs (Dict):
                Additional keyword arguments. Supports 'localize' (bool)
                to enable message translation.
        """
        super().__init__(parent, title, alert)
        self._message = message
        # Accept a plain zero-arg callable. The legacy (callable, label) tuple
        # is normalized to the callable with a deprecation warning (2.0).
        if isinstance(command, tuple):
            warn_deprecated(
                "passing a (callable, label) tuple as MessageDialog command",
                "a plain zero-argument callable",
            )
            command = command[0] if command else None
        self._command: Optional[Callable[[], Any]] = command
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
            icon_lbl = self._create_icon_label(container)
            if icon_lbl is not None:
                icon_lbl.pack(side=LEFT, anchor=N, padx=(0, 5))

        if self._message:
            for msg in self._message.split("\n"):
                message = "\n".join(textwrap.wrap(msg, width=self._width))
                ttk.Label(container, text=message).pack(pady=(0, 3), fill=X, anchor=N)
        container.pack(fill=X, expand=True)

    def _create_icon_label(self, container: tkinter.Misc) -> "Optional[ttk.Label]":
        """Build the icon Label from ``self._icon``, or None if it is unusable.

        ``self._icon`` may be, in order of preference, an already-rendered Tk
        image name (e.g. from ``ttk.Icon(...)`` -- the four default alert icons),
        base64 image data, or a file path. Setting ``image=`` to a string that
        is not an existing image raises ``TclError``, so an image name and base64
        data disambiguate cleanly with no string sniffing.
        """
        # Each candidate yields the image to hand to ``image=``. A rendered
        # ttk.Icon is a Tk image name (a str, pinned alive by the engine cache);
        # the data/file forms build a PhotoImage that must be retained on the
        # dialog (bound below) so it is not garbage-collected.
        candidates = (
            lambda: self._icon,
            lambda: ttk.PhotoImage(data=self._icon),
            lambda: ttk.PhotoImage(file=self._icon),
        )
        for make_image in candidates:
            try:
                image = make_image()
                label = ttk.Label(container, image=image)
            except Exception:
                continue
            self._img = image
            return label
        print("MessageDialog icon is invalid")
        return None

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
    """Static methods that pop up a message with various button arrangements
    and alert options, and return the label of the button the user pressed
    (or ``None`` if the dialog was dismissed via Escape / the window close).

    2.0 signature normalization: every method takes ``(message, title, *,
    parent, alert, position, buttons, icon, localize)``. ``parent``/``alert``
    are now **keyword-only** and in a uniform order (previously some methods
    ordered them ``parent, alert`` and others ``alert, parent`` positionally,
    so a positional third argument was ambiguous). The formerly hidden
    ``**kwargs`` options -- ``position``, ``buttons``, ``icon``, ``localize`` --
    are now discoverable named parameters.
    """

    @staticmethod
    def show_info(
            message: str,
            title: str = " ",
            *,
            parent: Optional[tkinter.Misc] = None,
            alert: bool = False,
            position: Optional[Tuple[int, int]] = None,
            buttons: Optional[List[str]] = None,
            icon: Optional[str] = None,
            localize: bool = True,
            **kwargs: Any,
    ) -> Optional[str]:
        """Display a modal dialog box with an OK button and an INFO icon."""
        dialog = MessageDialog(
            message=message,
            title=title,
            parent=parent,
            alert=alert,
            buttons=buttons or ["OK:primary"],
            icon=icon or _alert_icon("info"),
            localize=localize,
            **kwargs,
        )
        dialog.show(position)
        return dialog.result

    @staticmethod
    def show_warning(
            message: str,
            title: str = " ",
            *,
            parent: Optional[tkinter.Misc] = None,
            alert: bool = True,
            position: Optional[Tuple[int, int]] = None,
            buttons: Optional[List[str]] = None,
            icon: Optional[str] = None,
            localize: bool = True,
            **kwargs: Any,
    ) -> Optional[str]:
        """Display a modal dialog box with an OK button and a warning icon."""
        dialog = MessageDialog(
            message=message,
            title=title,
            parent=parent,
            alert=alert,
            buttons=buttons or ["OK:primary"],
            icon=icon or _alert_icon("warning"),
            localize=localize,
            **kwargs,
        )
        dialog.show(position)
        return dialog.result

    @staticmethod
    def show_error(
            message: str,
            title: str = " ",
            *,
            parent: Optional[tkinter.Misc] = None,
            alert: bool = True,
            position: Optional[Tuple[int, int]] = None,
            buttons: Optional[List[str]] = None,
            icon: Optional[str] = None,
            localize: bool = True,
            **kwargs: Any,
    ) -> Optional[str]:
        """Display a modal dialog box with an OK button and an error icon."""
        dialog = MessageDialog(
            message=message,
            title=title,
            parent=parent,
            alert=alert,
            buttons=buttons or ["OK:primary"],
            icon=icon or _alert_icon("error"),
            localize=localize,
            **kwargs,
        )
        dialog.show(position)
        return dialog.result

    @staticmethod
    def show_question(
            message: str,
            title: str = " ",
            *,
            parent: Optional[tkinter.Misc] = None,
            alert: bool = False,
            position: Optional[Tuple[int, int]] = None,
            buttons: Optional[List[str]] = None,
            icon: Optional[str] = None,
            localize: bool = True,
            **kwargs: Any,
    ) -> Optional[str]:
        """Display a modal dialog box with an OK button and a question icon."""
        dialog = MessageDialog(
            message=message,
            title=title,
            parent=parent,
            alert=alert,
            buttons=buttons or ["OK:primary"],
            icon=icon or _alert_icon("question"),
            localize=localize,
            **kwargs,
        )
        dialog.show(position)
        return dialog.result

    @staticmethod
    def ok(
            message: str,
            title: str = " ",
            *,
            parent: Optional[tkinter.Misc] = None,
            alert: bool = False,
            position: Optional[Tuple[int, int]] = None,
            buttons: Optional[List[str]] = None,
            icon: Optional[str] = None,
            localize: bool = True,
            **kwargs: Any,
    ) -> Optional[str]:
        """Display a modal dialog box with a single OK button."""
        dialog = MessageDialog(
            message=message,
            title=title,
            parent=parent,
            alert=alert,
            buttons=buttons or ["OK:primary"],
            icon=icon,
            localize=localize,
            **kwargs,
        )
        dialog.show(position)
        return dialog.result

    @staticmethod
    def okcancel(
            message: str,
            title: str = " ",
            *,
            parent: Optional[tkinter.Misc] = None,
            alert: bool = False,
            position: Optional[Tuple[int, int]] = None,
            buttons: Optional[List[str]] = None,
            icon: Optional[str] = None,
            localize: bool = True,
            **kwargs: Any,
    ) -> Optional[str]:
        """Display a modal dialog box with OK and Cancel buttons."""
        dialog = MessageDialog(
            message=message,
            title=title,
            parent=parent,
            alert=alert,
            buttons=buttons,
            icon=icon,
            localize=localize,
            **kwargs,
        )
        dialog.show(position)
        return dialog.result

    @staticmethod
    def yesno(
            message: str,
            title: str = " ",
            *,
            parent: Optional[tkinter.Misc] = None,
            alert: bool = False,
            position: Optional[Tuple[int, int]] = None,
            buttons: Optional[List[str]] = None,
            icon: Optional[str] = None,
            localize: bool = True,
            **kwargs: Any,
    ) -> Optional[str]:
        """Display a modal dialog box with Yes and No buttons."""
        dialog = MessageDialog(
            message=message,
            title=title,
            parent=parent,
            alert=alert,
            buttons=buttons or ["No", "Yes"],
            icon=icon,
            localize=localize,
            **kwargs,
        )
        dialog.show(position)
        return dialog.result

    @staticmethod
    def yesnocancel(
            message: str,
            title: str = " ",
            *,
            parent: Optional[tkinter.Misc] = None,
            alert: bool = False,
            position: Optional[Tuple[int, int]] = None,
            buttons: Optional[List[str]] = None,
            icon: Optional[str] = None,
            localize: bool = True,
            **kwargs: Any,
    ) -> Optional[str]:
        """Display a modal dialog box with Yes, No, and Cancel buttons."""
        dialog = MessageDialog(
            message=message,
            title=title,
            parent=parent,
            alert=alert,
            buttons=buttons or ["Cancel", "No", "Yes"],
            icon=icon,
            localize=localize,
            **kwargs,
        )
        dialog.show(position)
        return dialog.result

    @staticmethod
    def retrycancel(
            message: str,
            title: str = " ",
            *,
            parent: Optional[tkinter.Misc] = None,
            alert: bool = False,
            position: Optional[Tuple[int, int]] = None,
            buttons: Optional[List[str]] = None,
            icon: Optional[str] = None,
            localize: bool = True,
            **kwargs: Any,
    ) -> Optional[str]:
        """Display a modal dialog box with Retry and Cancel buttons."""
        dialog = MessageDialog(
            message=message,
            title=title,
            parent=parent,
            alert=alert,
            buttons=buttons or ["Cancel", "Retry"],
            icon=icon,
            localize=localize,
            **kwargs,
        )
        dialog.show(position)
        return dialog.result
