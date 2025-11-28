"""Core dialog base class for ttkbootstrap dialogs.

This module provides the minimal base `Dialog` class used by other
dialog implementations in this package.
"""

import tkinter
from abc import ABC, abstractmethod
from typing import Any, Optional, Tuple

import ttkbootstrap as ttk
from ttkbootstrap.utility import center_on_parent


class Dialog(ABC):
    """Base class for creating modal dialogs using composition pattern.

    This class creates and manages a Toplevel window internally and provides
    a consistent API for modal dialogs. Subclasses must implement
    `create_body` and `create_buttonbox` methods.
    """

    def __init__(self, master: Optional[tkinter.Misc] = None, title: str = "", alert: bool = False) -> None:
        """Initialize the dialog.

        Args:
            master: Parent widget for the dialog. If None, uses the default root window.
            title: Dialog window title. Ignored on macOS per platform guidelines.
            alert: If True, rings the system bell when the dialog is shown.
        """
        self._master = master if master else tkinter._default_root
        self._winsys = self._master.tk.call("tk", "windowingsystem")
        self._toplevel: Optional[ttk.Toplevel] = None
        self._title = title or " "
        self._result = None
        self._alert = alert
        self._initial_focus = None
        self._is_built = False

    def _locate(self) -> None:
        """Center the dialog on the parent window."""
        if self._toplevel:
            center_on_parent(self._toplevel, self._master)

    def show(self, position: Optional[Tuple[int, int]] = None, wait_for_result: bool = True) -> None:
        """Show the dialog.

        Args:
            position: x and y coordinates to position the dialog. If None, centers on parent.
            wait_for_result: If True, dialog is modal and blocks. If False, non-modal.
        """
        # Reset result for each show
        self._result = None

        # Build the dialog only once
        if not self._is_built:
            self._build()

        # Position the dialog
        if position is None:
            self._locate()
        else:
            try:
                x, y = position
                self._toplevel.geometry(f'+{x}+{y}')
            except (TypeError, ValueError):
                # Invalid position format, fall back to centering
                self._locate()

        # Show the dialog
        self._toplevel.deiconify()

        if self._alert:
            self._toplevel.bell()

        if self._initial_focus:
            self._initial_focus.focus_force()

        # Make modal if requested
        if wait_for_result:
            self._toplevel.grab_set()
            self._toplevel.wait_window()

    @abstractmethod
    def create_body(self, master: tkinter.Misc) -> None:
        """Create the dialog body.

        Subclasses must override this method. Set `self._initial_focus` to the widget
        that should receive initial focus.

        Args:
            master: The dialog's Toplevel window.
        """
        pass

    @abstractmethod
    def create_buttonbox(self, master: tkinter.Misc) -> None:
        """Create the dialog button box.

        Subclasses must override this method. Set `self._initial_focus` to the button
        that should receive initial focus.

        Args:
            master: The dialog's Toplevel window.
        """
        pass

    def _build(self) -> None:
        """Build the dialog window and widgets."""
        if self._is_built:
            return

        # Setup toplevel based on windowing system
        if self._winsys == "win32":
            self._toplevel = ttk.Toplevel(
                transient=self._master,
                title=self._title,
                resizable=(False, False),
                minsize=(250, 15),
                iconify=True,
            )
        else:
            self._toplevel = ttk.Toplevel(
                transient=self._master,
                title=self._title,
                resizable=(False, False),
                minsize=(250, 15),
                windowtype="dialog",
                iconify=True,
            )

        self._toplevel.withdraw()  # Reset the iconify state

        # Bind <Escape> event to proper close handler
        self._toplevel.bind("<Escape>", lambda _: self._on_escape())

        # Create widgets
        self.create_body(self._toplevel)
        self.create_buttonbox(self._toplevel)

        # Update the window before showing (platform-specific timing for Linux/macOS)
        self._toplevel.update_idletasks()

        # Explicitly set geometry to ensure proper sizing on all platforms
        width = self._toplevel.winfo_reqwidth()
        height = self._toplevel.winfo_reqheight()
        if width > 0 and height > 0:
            self._toplevel.geometry(f"{width}x{height}")

        self._is_built = True

    def _on_escape(self) -> None:
        """Cancel the dialog when Escape is pressed."""
        self._result = None
        self.destroy()

    def destroy(self) -> None:
        """Destroy the dialog and release resources."""
        if self._toplevel:
            try:
                self._toplevel.grab_release()
            except tkinter.TclError:
                # Grab might not be set or window already destroyed
                pass

            try:
                self._toplevel.destroy()
            except tkinter.TclError:
                # Window might already be destroyed
                pass

            self._toplevel = None
            self._is_built = False

    @property
    def result(self) -> Any:
        """The dialog result value."""
        return self._result
