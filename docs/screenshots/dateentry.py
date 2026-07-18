"""Screenshot scenes for docs/widgets/dateentry.rst."""

from datetime import datetime

import ttkbootstrap as ttk
from ttkbootstrap.widgets import DateEntry


def open():
    # The calendar popover dismisses on focus move, so use the parent-capture:
    # announce the (tall) window rect, open the calendar (it drops within), and
    # the harness parent grabs the region while it's up.
    app = ttk.App(title="DateEntry", size=(300, 340))
    frm = ttk.Frame(app, padding=20)
    frm.pack(anchor="n", fill="x")
    picker = DateEntry(frm)
    picker.pack(anchor="w")
    picker.set_date(datetime(2026, 7, 16))

    def open_cal():
        app.capture_via_parent()
        picker.button.invoke()   # opens the modal calendar (drops below the field)

    app.after(500, open_cal)
    app.mainloop()


SCENES = {
    "open": open,
}
