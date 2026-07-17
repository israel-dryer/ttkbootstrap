"""Screenshot scenes for docs/user-guide/feature-guides/windows.rst."""

import ttkbootstrap as ttk


def centered():
    # Capture the About dialog itself (a Toplevel positioned with
    # place_window_center). A tight parent+child composite isn't reliable here --
    # the child sits at screen center, far from the harness-offset parent -- so
    # the shot shows the centered dialog window on its own.
    app = ttk.App(title="Editor")
    ttk.Label(app, text="Editor", padding=20).pack()

    win = ttk.Toplevel(master=app, title="About")
    win.minsize(280, 1)   # comfortable width; height auto-sizes -> OK sits at the bottom
    frm = ttk.Frame(win, padding=20)
    frm.pack(fill="both", expand=True)
    ttk.Label(frm, text="About Editor", font="TkHeadingFont").pack(anchor="w")
    ttk.Label(frm, text="A tiny text editor.\nVersion 2.0").pack(anchor="w", pady=(4, 14))
    ttk.Button(frm, text="OK", bootstyle="primary").pack(anchor="e")
    win.place_window_center()

    def _raise():
        win.attributes("-topmost", True)
        win.lift()

    app.after(200, _raise)
    app._capture_target = win     # capture the centered dialog window
    app.mainloop()


SCENES = {
    "centered": centered,
}
