"""Screenshot scenes for docs/user-guide/how-to/scrollable.rst."""

import tkinter

import ttkbootstrap as ttk


def settings():
    # Default (auto_hide off) keeps the scrollbar visible at the right edge, which
    # is what the shot needs; a few toggles are on for colour.
    app = ttk.App(title="Settings", size=(360, 300))
    scroller = ttk.ScrolledFrame(app)
    scroller.pack(fill="both", expand=True, padx=10, pady=10)
    app._vars = []
    for i in range(40):
        var = tkinter.IntVar(value=1 if i % 3 == 0 else 0)
        app._vars.append(var)
        ttk.Checkbutton(scroller, text=f"Option {i + 1}", variable=var,
                        bootstyle="round toggle").pack(anchor="w", pady=2)
    app._capture_full_window = True
    app.mainloop()


SCENES = {
    "settings": settings,
}
