import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from random import choice

DARK = 'superhero'
LIGHT = 'flatly'


def create_entry_test(bootstyle, style):
    frame = ttk.Frame(padding=10)

    # title
    title = ttk.Label(frame, text='Entry', anchor=tk.CENTER)
    title.pack(padx=5, pady=2, fill=tk.BOTH)
    ttk.Separator(frame).pack(padx=5, pady=5, fill=tk.X)

    # default
    entry = ttk.Entry(frame, bootstyle=bootstyle)
    entry.pack(padx=5, pady=5, fill=tk.BOTH)
    entry.insert(tk.END, 'default')

    # color
    for color in style.theme.colors:
        entry = ttk.Entry(frame, bootstyle=color)
        entry.pack(padx=5, pady=5, fill=tk.BOTH)
        entry.insert(tk.END, color)

    # readonly
    entry = ttk.Entry(frame, bootstyle=bootstyle)
    entry.insert(tk.END, 'readonly')
    entry.configure(state=READONLY)
    entry.pack(padx=5, pady=5, fill=tk.BOTH)        

    # disabled
    entry = ttk.Entry(frame, bootstyle=bootstyle)
    entry.insert(tk.END, 'disabled')
    entry.configure(state=DISABLED)
    entry.pack(padx=5, pady=5, fill=tk.BOTH)

    return frame


def change_style():
    theme = choice(root.style.theme_names())
    root.style.theme_use(theme)    


if __name__ == '__main__':
    # create visual widget style tests
    root = ttk.Window(themename='sandstone')

    ttk.Button(text="Change Theme", command=change_style).pack(padx=10, pady=10)

    test1 = create_entry_test('TEntry', root.style)
    test1.pack(side=tk.LEFT, fill=tk.BOTH)

    root.mainloop()
