"""Screenshot scenes for docs/widgets/combobox.rst."""

import ttkbootstrap as ttk


def closed():
    app = ttk.App(title="Combobox")
    frm = ttk.Frame(app, padding=20).pack()
    color = ttk.StringVar(value="Green")
    ttk.Combobox(frm, textvariable=color, values=["Red", "Green", "Blue"],
                 width=16).pack()
    app.mainloop()


def open():
    # tall enough that the popdown drops within the window
    app = ttk.App(title="Combobox", size=(230, 125))
    frm = ttk.Frame(app, padding=20).pack()
    color = ttk.StringVar(value="Green")
    combo = ttk.Combobox(frm, textvariable=color, values=["Red", "Green", "Blue"],
                         width=16)
    combo.pack()

    def drop():
        app.tk.call("ttk::combobox::Post", combo)
        # the popdown exists only on the Tcl side — pass its window path
        app._capture_extra = [app.tk.eval(f"ttk::combobox::PopdownWindow {combo}")]

    app.after(400, drop)
    app.mainloop()


SCENES = {
    "closed": closed,
    "open": open,
}
