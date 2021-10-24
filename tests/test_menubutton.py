import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style

DARK = 'superhero'
LIGHT = 'flatly'


def create_menubutton_frame(widget_style, style):
    frame = ttk.Frame(root, padding=5)

    title = ttk.Label(
        master=frame,
        text=widget_style,
        anchor=tk.CENTER
    )
    title.pack(padx=5, pady=2, fill=tk.BOTH)

    ttk.Separator(frame).pack(padx=5, pady=5, fill=tk.X)

    btn = ttk.Menubutton(
        master=frame,
        text=widget_style,
        style=widget_style
    )
    btn.pack(padx=5, pady=5, fill=tk.BOTH)

    for color in style.colors:
        button_style = f'{color}.{widget_style}'
        btn = ttk.Menubutton(
            master=frame,
            text=button_style,
            style=button_style
        )
        btn.pack(padx=5, pady=5, fill=tk.BOTH)

    disabled_style = f'{widget_style} (disabled)'

    btn = ttk.Menubutton(
        master=frame,
        text=disabled_style,
        state=tk.DISABLED,
        style=widget_style
    )
    btn.pack(padx=5, pady=5, fill=tk.BOTH)

    return frame


if __name__ == '__main__':
    root = tk.Tk()
    style = Style(theme=DARK)

    create_menubutton_frame(
        widget_style='TMenubutton',
        style=style
    ).pack(side=tk.LEFT)

    create_menubutton_frame(
        widget_style='Outline.TMenubutton',
        style=style
    ).pack(side=tk.LEFT)

    root.mainloop()
