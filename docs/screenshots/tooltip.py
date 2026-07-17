"""Screenshot scenes for docs/widgets/tooltip.rst."""

import ttkbootstrap as ttk
from ttkbootstrap.widgets import ToolTip


def hero():
    # tall enough that the anchored tip fits within the window
    app = ttk.App(title="ToolTip", size=(280, 130))
    save = ttk.Button(app, text="Save", bootstyle="primary")
    save.pack(padx=20, pady=20)

    tip = ToolTip(save, text="Save the current file (Ctrl+S)",
                  position="bottom")

    def show():
        tip.show_tip()
        app._capture_extra = [tip.toplevel]

    app.after(400, show)
    app.mainloop()


SCENES = {
    "hero": hero,
}
