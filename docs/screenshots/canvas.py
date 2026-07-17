"""Screenshot scenes for docs/widgets/canvas.rst."""

import ttkbootstrap as ttk


def hero():
    app = ttk.App(title="Canvas")
    frm = ttk.Frame(app, padding=10).pack()

    canvas = ttk.Canvas(frm, width=300, height=200)
    canvas.pack()

    colors = ttk.Style.get_instance().colors
    canvas.create_rectangle(20, 20, 120, 90, fill=colors.primary, outline="")
    canvas.create_oval(160, 20, 260, 120, fill=colors.success, outline="")
    canvas.create_line(20, 150, 280, 150, width=3, fill=colors.fg)
    canvas.create_text(150, 180, text="Hello, canvas", fill=colors.fg)

    app.mainloop()


SCENES = {
    "hero": hero,
}
