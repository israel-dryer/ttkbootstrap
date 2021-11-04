import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style

DARK = 'superhero'
LIGHT = 'flatly'


def button_style_frame(bootstyle, style, widget_name):
    frame = ttk.Frame(root, padding=5)

    title = ttk.Label(
        master=frame,
        text=widget_name,
        anchor=tk.CENTER
    )
    title.pack(padx=5, pady=2, fill=tk.BOTH)

    ttk.Separator(frame).pack(padx=5, pady=5, fill=tk.X)

    btn = ttk.Button(
        master=frame,
        text='default',
        bootstyle=bootstyle
    )
    btn.pack(padx=5, pady=5, fill=tk.BOTH)

    for color in style.colors:
        btn = ttk.Button(
            master=frame,
            text=color,
            bootstyle=(color, bootstyle)
        )
        btn.pack(padx=5, pady=5, fill=tk.BOTH)

    btn = ttk.Button(
        master=frame,
        text='disabled',
        state=tk.DISABLED,
        bootstyle=bootstyle
    )
    btn.pack(padx=5, pady=5, fill=tk.BOTH)

    return frame


if __name__ == '__main__':
    # create visual widget style tests
    root = tk.Tk()
    style = Style(theme='flatly')

    button_style_frame('', style, 'Solid Button').pack(side=tk.LEFT)
    button_style_frame('outline', style, 'Outline Button').pack(side=tk.LEFT)
    button_style_frame('link', style, 'Link Button').pack(side=tk.LEFT)

    root.mainloop()
