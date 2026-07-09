"""Core dialog base class for ttkbootstrap dialogs.

This module provides the minimal base `Dialog` class used by other
dialog implementations in this package.
"""

import tkinter
from tkinter import BaseWidget
from typing import Any, Optional, Tuple

import ttkbootstrap as ttk
from ttkbootstrap.internal.utility import center_on_parent
from ttkbootstrap.internal.positioning import ensure_on_screen
from ttkbootstrap.utility import windowing_system


class Dialog(BaseWidget):
    """A simple dialog base class."""

    def __init__(self, parent: Optional[tkinter.Misc] = None, title: str = "", alert: bool = False) -> None:
        """
        Parameters:

            parent (Widget):
                Makes the window the logical parent of the dialog.
                The dialog is displayed on top of its parent window.

            title (str):
                The string displayed as the title of the dialog.
                This option is ignored on Mac OS X, where platform
                guidelines forbid the use of a title on this kind of
                dialog.

            alert (bool):
                Ring the display's bell when the dialog is shown.
        """
        BaseWidget._setup(self, parent, {})
        self._winsys = windowing_system(self.master)
        self._parent = parent
        self._toplevel = None
        self._title = title or " "
        self._result = None
        self._alert = alert
        self._initial_focus = None

    def _locate(self) -> None:
        toplevel = self._toplevel
        center_on_parent(toplevel, self._parent)

    def show(self, position: Optional[Tuple[int, int]] = None, wait_for_result: bool = True) -> None:
        """Show the popup dialog.

        Parameters:

            position (tuple[int, int], optional):
                The x and y coordinates used to position the dialog. If not
                given, the dialog is centered on the parent window.

            wait_for_result (bool):
                Grab input focus and block until the dialog is closed.
        """
        self.update_idletasks()
        self._result = None
        self.build()

        if position is None:
            self._locate()
        else:
            try:
                x, y = position
                # Clamp so an explicit position near a screen edge doesn't push
                # the dialog partly (or fully) off-screen.
                x, y = ensure_on_screen(self._toplevel, x, y)
                self._toplevel.geometry(f'+{x}+{y}')
            except Exception:
                self._locate()

        self._toplevel.deiconify()
        if self._alert:
            self._toplevel.bell()

        if self._initial_focus:
            self._initial_focus.focus_force()

        if wait_for_result:
            self._toplevel.grab_set()
            self._toplevel.wait_window()

    def create_body(self, master: tkinter.Misc) -> None:
        """Create the dialog body.

        This method should be overridden and is called by the `build`
        method. Set the `self._initial_focus` for the widget that
        should receive the initial focus.

        Parameters:

            master (Widget):
                The parent widget.
        """
        raise NotImplementedError

    def create_buttonbox(self, master: tkinter.Misc) -> None:
        """Create the dialog button box.

        This method should be overridden and is called by the `build`
        method. Set the `self._initial_focus` for the button that
        should receive the initial focus.

        Parameters:

            master (Widget):
                The parent widget.
        """
        raise NotImplementedError

    def build(self) -> None:
        """Build the dialog from settings"""

        # setup toplevel based on widowing system
        if self._winsys == "win32":
            self._toplevel = ttk.Toplevel(
                transient=self.master,
                title=self._title,
                resizable=(False, False),
                minsize=(250, 15),
                iconify=True,
            )
        else:
            self._toplevel = ttk.Toplevel(
                transient=self.master,
                title=self._title,
                resizable=(False, False),
                minsize=(250, 15),
                window_type="dialog",
                iconify=True,
            )

        self._toplevel.withdraw()  # reset the iconify state

        # bind <Escape> event to window close
        self._toplevel.bind("<Escape>", lambda _: self._toplevel.destroy())

        # create widgets
        self.create_body(self._toplevel)
        self.create_buttonbox(self._toplevel)

        # update the window before showing
        self._toplevel.update_idletasks()

        # Explicitly set geometry to ensure proper sizing on all platforms
        width = self._toplevel.winfo_reqwidth()
        height = self._toplevel.winfo_reqheight()
        if width > 0 and height > 0:
            self._toplevel.geometry(f"{width}x{height}")        

    @property
    def result(self) -> Any:
        """Returns the result of the dialog.

        Safe to read whether the toplevel is already destroyed (e.g.
        ``QueryDialog`` destroys it synchronously on submit) or only queued for
        destruction (``MessageDialog`` uses ``after_idle``); the grab is released
        only if the window still exists.
        """
        toplevel = self._toplevel
        if toplevel is not None:
            try:
                if toplevel.winfo_exists():
                    toplevel.grab_release()
            except tkinter.TclError:
                pass
        return self._result
