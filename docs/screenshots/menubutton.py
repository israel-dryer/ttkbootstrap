"""Screenshot scenes for docs/widgets/menubutton.rst."""

import ttkbootstrap as ttk


def open():
    # tall enough that the posted menu drops within the window
    app = ttk.App(title="Menubutton", size=(220, 175))
    frm = ttk.Frame(app, padding=20).pack()
    menubutton = ttk.Menubutton(frm, text="Actions", bootstyle="primary")
    menubutton.pack()

    menu = ttk.Menu(menubutton)
    menu.add_command(label="New")
    menu.add_command(label="Open")
    menu.add_separator()
    menu.add_command(label="Quit")
    menubutton["menu"] = menu

    def post():
        # a native menu blocks the event loop while open — hand the capture
        # to the harness parent, then post
        app.capture_via_parent()
        x = menubutton.winfo_rootx()
        y = menubutton.winfo_rooty() + menubutton.winfo_height()
        menu.post(x, y)

    app.after(600, post)
    app.mainloop()


SCENES = {
    "open": open,
}
