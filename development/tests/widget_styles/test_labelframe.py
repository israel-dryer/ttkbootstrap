import tkinter as tk
import ttkbootstrap as ttk
from random import choice
from ttkbootstrap import utility
utility.enable_high_dpi_awareness()

DARK = 'superhero'
LIGHT = 'flatly'


def create_labelframe_style(bootstyle, style):
    frame = ttk.Frame(root, padding=5)

    # title
    title = ttk.Label(frame, text='Labelframe', anchor=tk.CENTER)
    title.pack(padx=5, pady=2, fill=tk.BOTH)
    ttk.Separator(frame).pack(padx=5, pady=5, fill=tk.X)

    # default
    lbl = ttk.Labelframe(
        master=frame,
        text='default',
        bootstyle=bootstyle,
        width=150,
        height=75
    )
    lbl.pack(padx=5, pady=5, fill=tk.BOTH)

    # colored
    for color in style.colors:
        lbl = ttk.Labelframe(
            master=frame,
            text=color,
            bootstyle=color,
            width=150,
            height=75
        )
        lbl.pack(padx=5, pady=5, fill=tk.BOTH)

    return frame


def change_style():
    theme = choice(style.theme_names())
    style.theme_use(theme)    


if __name__ == '__main__':
    # create visual widget style tests
    root = tk.Tk()
    style = ttk.Style()

    ttk.Button(text="Change Theme", command=change_style).pack(padx=10, pady=10)

    create_labelframe_style('', style).pack(side=tk.LEFT)

    root.mainloop()
