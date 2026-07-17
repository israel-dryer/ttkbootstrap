"""Screenshot scenes for docs/user-guide/foundations/layout-with-pack.rst."""

import ttkbootstrap as ttk


def toolbar():
    # Step 3 state: a toolbar frame spanning the top, a content area below it
    # taking the leftover space.
    app = ttk.App(title="Pack", size=(360, 220))

    bar = ttk.Frame(app, bootstyle="secondary")
    bar.pack(side="top", fill="x")
    ttk.Button(bar, text="New").pack(side="left", padx=2, pady=2)
    ttk.Button(bar, text="Open").pack(side="left", padx=2, pady=2)

    content = ttk.Frame(app, padding=20)
    content.pack(side="top", fill="both", expand=True)
    ttk.Label(content, text="Content goes here").pack()
    app.mainloop()


def shell():
    # Step 4 state: the full app shell — header, status bar, sidebar, content.
    app = ttk.App(title="App shell", size=(600, 400))

    ttk.Label(app, text="  My App", bootstyle="inverse-primary").pack(
        side="top", fill="x", ipady=8)
    ttk.Label(app, text="  Ready", bootstyle="inverse-secondary").pack(
        side="bottom", fill="x", ipady=4)

    middle = ttk.Frame(app)
    middle.pack(side="top", fill="both", expand=True)

    sidebar = ttk.Frame(middle, width=160, bootstyle="secondary")
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)

    content = ttk.Frame(middle, padding=20)
    content.pack(side="left", fill="both", expand=True)
    ttk.Label(content, text="Content goes here").pack()
    app.mainloop()


SCENES = {
    "toolbar": toolbar,
    "shell": shell,
}
