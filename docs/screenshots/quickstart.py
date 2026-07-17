"""Screenshot scenes for docs/user-guide/getting-started/quickstart.rst."""

import ttkbootstrap as ttk


def hello():
    app = ttk.App(title="Hello")
    ttk.Label(app, text="Hello from ttkbootstrap!").pack(padx=16, pady=(16, 8))
    ttk.Button(app, text="Primary", bootstyle="primary").pack(padx=16, pady=4)
    ttk.Button(app, text="Success", bootstyle="success").pack(padx=16, pady=4)
    ttk.Button(app, text="Danger Outline", bootstyle="danger outline").pack(
        padx=16, pady=(4, 16))
    app._capture_full_window = True  # a complete first app — show the window chrome
    app.mainloop()


SCENES = {
    "hello": hello,
}
