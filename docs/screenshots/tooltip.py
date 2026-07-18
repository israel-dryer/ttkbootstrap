"""Screenshot scenes for docs/widgets/tooltip.rst."""

import ttkbootstrap as ttk
from ttkbootstrap.widgets import ToolTip


def hero():
    # The tip is a separate top-level that dismisses on focus move, so use the
    # parent-capture: announce the (tall) window rect, show the anchored tip (it
    # drops within the window), and the harness parent grabs the region.
    app = ttk.App(title="ToolTip", size=(300, 150))
    save = ttk.Button(app, text="Save", bootstyle="primary")
    save.pack(padx=20, pady=(28, 20), anchor="n")

    tip = ToolTip(save, text="Save the current file (Ctrl+S)", position="bottom")

    def show():
        app.capture_via_parent()
        tip.show_tip()

    app.after(500, show)
    app.mainloop()


SCENES = {
    "hero": hero,
}
