import tkinter as tk
import ttkbootstrap as ttk
from random import choice
from ttkbootstrap import utility
utility.enable_high_dpi_awareness()

DARK = 'superhero'
LIGHT = 'flatly'


def create_entry_test(style):
    frame = ttk.Frame(padding=10)

    # title
    title = ttk.Label(frame, text='DateEntry', anchor=tk.CENTER)
    title.pack(padx=5, pady=2, fill=tk.BOTH)
    ttk.Separator(frame).pack(padx=5, pady=5, fill=tk.X)

    # default
    ttk.Label(frame, text='default').pack()
    entry = ttk.DateEntry(frame)
    entry.pack(padx=5, pady=5, fill=tk.BOTH)

    # color
    for color in style.theme.colors:
        ttk.Label(frame, text=color).pack()
        entry = ttk.DateEntry(frame, bootstyle=color)
        entry.pack(padx=5, pady=5, fill=tk.BOTH)

    ttk.Label(frame, text='disabled').pack()
    entry = ttk.DateEntry(frame)
    entry.configure(state=tk.DISABLED)
    entry.pack(padx=5, pady=5, fill=tk.BOTH)

    ttk.Label(frame, text='readonly').pack()
    entry = ttk.DateEntry(frame)
    entry.configure(state='readonly')
    entry.pack(padx=5, pady=5, fill=tk.BOTH)


    return frame


def change_style():
    theme = choice(style.theme_names())
    style.theme_use(theme)    


if __name__ == '__main__':
    # create visual widget style tests
    root = tk.Tk()
    style = ttk.Style()

    ttk.Button(text="Change Theme", command=change_style).pack(padx=10, pady=10)

    test1 = create_entry_test(style)
    test1.pack(side=tk.LEFT, fill=tk.BOTH)

    root.mainloop()
