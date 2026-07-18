"""Screenshot scenes for docs/user-guide/how-to/multiple-windows.rst."""

import ttkbootstrap as ttk


def dialog():
    # The modal ask_name dialog. Captured without grab_set/wait_window (which
    # would block) -- the harness targets the dialog window directly.
    app = ttk.App(title="Main", size=(320, 200))
    ttk.Label(app, text="Main window", padding=20).pack()

    win = ttk.Toplevel(master=app, title="Your name")
    win.minsize(240, 1)
    name = ttk.StringVar(value="Ada Lovelace")
    entry = ttk.Entry(win, textvariable=name)
    entry.pack(padx=10, pady=10, fill="x")
    ttk.Button(win, text="OK", bootstyle="primary").pack(pady=(0, 10))
    win.place_window_center()      # screen-centered, clear of the offset main window

    def target():
        win.attributes("-topmost", True)
        win.lift()
        app._capture_target = win

    app.after(200, target)
    app.mainloop()


SCENES = {
    "dialog": dialog,
}
