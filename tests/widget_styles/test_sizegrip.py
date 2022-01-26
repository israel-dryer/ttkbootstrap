import tkinter as tk
import ttkbootstrap as ttk
from random import choice
from ttkbootstrap import utility
utility.enable_high_dpi_awareness()

DARK = 'superhero'
LIGHT = 'flatly'


def create_sizegrip_style(bootstyle, style):
    frame = ttk.Frame(root, padding=5)

    # title
    title = ttk.Label(
        master=frame,
        text='Sizegrip',
        anchor=tk.CENTER
    )
    title.pack(padx=5, pady=2, fill=tk.BOTH)
    ttk.Separator(frame).pack(padx=5, pady=5, fill=tk.X)

    # default
    ttk.Label(frame, text=bootstyle).pack(fill=tk.X)
    sg = ttk.Sizegrip(frame)
    sg.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

    # colored
    for color in style.colors:
        ttk.Label(frame, text=color).pack(fill=tk.X)
        sg = ttk.Sizegrip(frame, bootstyle=(color, bootstyle))
        sg.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

    return frame


def change_style():
    theme = choice(style.theme_names())
    style.theme_use(theme)    


if __name__ == '__main__':
    # create visual widget style tests
    root = tk.Tk()
    style = ttk.Style()

    ttk.Button(text="Change Theme", command=change_style).pack(padx=10, pady=10)

    create_sizegrip_style('', style).pack(
        side=tk.LEFT, fill=tk.BOTH, expand=True
    )

    root.mainloop()
