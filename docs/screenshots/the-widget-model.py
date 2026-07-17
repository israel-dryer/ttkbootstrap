"""Screenshot scenes for docs/user-guide/foundations/the-widget-model.rst."""

import ttkbootstrap as ttk


def _panel(app, text, disabled):
    panel = ttk.Frame(app, padding=10)
    panel.pack()
    name = ttk.Entry(panel, width=24)
    name.pack(pady=(0, 8))
    if text:
        name.insert(0, text)
    save = ttk.Button(panel, text="Save", bootstyle="success")
    save.pack()
    save.state(["disabled"] if disabled else ["!disabled"])
    app.mainloop()


def disabled():
    _panel(ttk.App(title="Widget model"), "", True)


def enabled():
    _panel(ttk.App(title="Widget model"), "Ada Lovelace", False)


SCENES = {
    "disabled": disabled,
    "enabled": enabled,
}
