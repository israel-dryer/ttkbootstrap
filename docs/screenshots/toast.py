"""Screenshot scenes for docs/widgets/toast.rst."""

import ttkbootstrap as ttk
from ttkbootstrap.widgets import ToastNotification


def hero():
    app = ttk.App(title="Toast")
    ttk.Frame(app, padding=40).pack()

    def show():
        toast = ToastNotification(
            title="Saved",
            message="Your file was saved.",
            bootstyle="success",
        )
        toast.show_toast()
        app._capture_target = toast.toplevel  # capture the toast window itself

    app.after(400, show)
    app.mainloop()


SCENES = {
    "hero": hero,
}
