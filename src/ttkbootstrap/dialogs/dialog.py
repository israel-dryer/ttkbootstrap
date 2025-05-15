"""
    This module contains various base dialog base classes that can be
    used to create custom dialogs for the end user.

    These classes serve as the basis for the pre-defined static helper
    methods in the `Messagebox`, and `Querybox` container classes.
"""

import ttkbootstrap as ttk
from tkinter import BaseWidget


class Dialog(BaseWidget):
    """A simple dialog base class."""

    def __init__(self, parent=None, title="", alert=False):
        """
        Parameters:

            parent (Widget):
                Makes the window the logical parent of the message box.
                The messagebox is displayed on top of its parent window.

            title (str):
                The string displayed as the title of the message box.
                This option is ignored on Mac OS X, where platform
                guidelines forbid the use of a title on this kind of
                dialog.

            alert (bool):
                Ring the display's bell when the dialog is shown.
        """
        BaseWidget._setup(self, parent, {})
        self._winsys = self.master.tk.call("tk", "windowingsystem")
        self._parent = parent
        self._toplevel = None
        self._title = title or " "
        self._result = None
        self._alert = alert
        self._initial_focus = None

    def _locate(self):
        toplevel = self._toplevel
        if self._parent is None:
            master = toplevel.master
        else:
            master = self._parent
        x = master.winfo_rootx()
        y = master.winfo_rooty()
        toplevel.geometry(f"+{x}+{y}")

    def show(self, position=None, wait_for_result=True):
        """Show the popup dialog
        Parameters:

            position: Tuple[int, int]
                The x and y coordinates used to position the dialog. By
                default the dialog will anchor at the NW corner of the
                parent window.
        """
        self._result = None
        self.build()

        if position is None:
            self._locate()
        else:
            try:
                x, y = position
                self._toplevel.geometry(f'+{x}+{y}')
            except:
                self._locate()

        self._toplevel.deiconify()
        if self._alert:
            self._toplevel.bell()

        if self._initial_focus:
            self._initial_focus.focus_force()

        if wait_for_result:
            self._toplevel.wait_window()

    def create_body(self, master):
        """Create the dialog body.

        This method should be overridden and is called by the `build`
        method. Set the `self._initial_focus` for the widget that
        should receive the initial focus.

        Parameters:

            master (Widget):
                The parent widget.
        """
        raise NotImplementedError

    def create_buttonbox(self, master):
        """Create the dialog button box.

        This method should be overridden and is called by the `build`
        method. Set the `self._initial_focus` for the button that
        should receive the intial focus.

        Parameters:

            master (Widget):
                The parent widget.
        """
        raise NotImplementedError

    def build(self):
        """Build the dialog from settings"""

        # setup toplevel based on widowing system
        if self._winsys == "win32":
            self._toplevel = ttk.Toplevel(
                transient=self.master,
                title=self._title,
                resizable=(0, 0),
                minsize=(250, 15),
                iconify=True,
            )
        else:
            self._toplevel = ttk.Toplevel(
                transient=self.master,
                title=self._title,
                resizable=(0, 0),
                windowtype="dialog",
                iconify=True,
            )

        self._toplevel.withdraw()  # reset the iconify state

        # bind <Escape> event to window close
        self._toplevel.bind("<Escape>", lambda _: self._toplevel.destroy())

        # set position of popup from parent window
        # self._locate()

        # create widgets
        self.create_body(self._toplevel)
        self.create_buttonbox(self._toplevel)

        # update the window before showing
        self._toplevel.update_idletasks()

    @property
    def result(self):
        """Returns the result of the dialog."""
        return self._result
