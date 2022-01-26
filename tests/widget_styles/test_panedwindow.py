import tkinter as tk
import ttkbootstrap as ttk
from random import choice
from ttkbootstrap import utility
utility.enable_high_dpi_awareness()

DARK = 'superhero'
LIGHT = 'flatly'


def create_panedwindow_frame(widget_style, style):
    frame = ttk.Frame(root, padding=5)

    # title
    title = ttk.Label(frame, text=widget_style, anchor=tk.CENTER)
    title.pack(padx=5, pady=2, fill=tk.BOTH)
    ttk.Separator(frame).pack(padx=5, pady=5, fill=tk.X)

    # default
    pw = ttk.Panedwindow(frame)
    pw.pack(padx=5, pady=5, fill=tk.BOTH)
    pw.add(ttk.Frame(pw, width=100, height=50, bootstyle='info'))
    pw.add(ttk.Frame(pw, width=100, height=50, bootstyle='success'))

    for color in style.colors:
    # default
        pw = ttk.Panedwindow(frame, bootstyle=color)
        pw.pack(padx=5, pady=5, fill=tk.BOTH)
        pw.add(ttk.Frame(pw, width=100, height=50))
        pw.add(ttk.Frame(pw, width=100, height=50))        

    return frame


def change_style():
    theme = choice(style.theme_names())
    style.theme_use(theme)    


if __name__ == '__main__':
    # create visual widget style tests
    root = tk.Tk()
    style = ttk.Style()

    ttk.Button(text="Change Theme", command=change_style).pack(padx=10, pady=10)

    create_panedwindow_frame('TPanedwindow', style).pack(side=tk.LEFT)

    root.mainloop()
