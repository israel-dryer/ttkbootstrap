"""Screenshot scenes for docs/widgets/optionmenu.rst."""

import ttkbootstrap as ttk


def open():
    # tall enough that the posted list drops within the window
    app = ttk.App(title="OptionMenu", size=(220, 175))
    frm = ttk.Frame(app, padding=20).pack()
    size = ttk.StringVar()
    om = ttk.OptionMenu(frm, size, "Medium", "Small", "Medium", "Large")
    om.pack()

    def post():
        # a native menu blocks the event loop while open — hand the capture
        # to the harness parent, then post
        app.capture_via_parent()
        menu = app.nametowidget(om.cget("menu"))
        x = om.winfo_rootx()
        y = om.winfo_rooty() + om.winfo_height()
        menu.post(x, y)

    app.after(600, post)
    app.mainloop()


SCENES = {
    "open": open,
}
