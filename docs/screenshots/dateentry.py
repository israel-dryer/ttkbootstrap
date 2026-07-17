"""Screenshot scenes for docs/widgets/dateentry.rst."""

import tkinter
from datetime import datetime

import ttkbootstrap as ttk
from ttkbootstrap.widgets import DateEntry


def open():
    # tall enough that the pop-up calendar drops within the window
    app = ttk.App(title="DateEntry", size=(300, 315))
    frm = ttk.Frame(app, padding=20).pack()
    picker = DateEntry(frm)
    picker.pack()
    picker.set_date(datetime(2026, 7, 16))

    # The calendar button opens a modal dialog; Tk's modal wait still pumps
    # after() callbacks, so the popup can be wired into the capture afterwards.
    app.after(300, picker.button.invoke)

    def wire():
        tops = [w for w in app.winfo_children() if isinstance(w, tkinter.Toplevel)]
        app._capture_extra = tops

    app.after(700, wire)
    app.mainloop()


SCENES = {
    "open": open,
}
