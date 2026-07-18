"""Screenshot scenes for docs/widgets/combobox.rst."""

import ttkbootstrap as ttk


def open():
    # The popdown dismisses on focus move, so use the parent-capture: announce
    # the (tall) window rect, post the popdown (it drops within the window), and
    # the harness parent grabs the region.
    app = ttk.App(title="Combobox", size=(230, 150))
    frm = ttk.Frame(app, padding=20)
    frm.pack(anchor="n", fill="x")
    color = ttk.StringVar(value="Green")
    combo = ttk.Combobox(frm, textvariable=color, values=["Red", "Green", "Blue"],
                         width=16)
    combo.pack(anchor="w")

    def drop():
        app.capture_via_parent()
        app.tk.call("ttk::combobox::Post", combo)

    app.after(500, drop)
    app.mainloop()


SCENES = {
    "open": open,
}
