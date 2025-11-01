from random import choice

import ttkbootstrap as ttk
from ttkbootstrap import utility
from ttkbootstrap.constants import *

utility.enable_high_dpi_awareness()


def create_label_style(bootstyle, style, test_name):
    frame = ttk.Frame(root, padding=5)

    # title
    title = ttk.Label(frame, text=test_name, anchor=CENTER)
    title.pack(padx=5, pady=2, fill=BOTH)
    ttk.Separator(frame).pack(padx=5, pady=5, fill=X)

    # default
    lbl = ttk.Label(frame, text='default', bootstyle=bootstyle)
    lbl.pack(padx=5, pady=5, fill=BOTH)

    # colored
    for color in style.colors:
        lbl = ttk.Label(frame, text=color, bootstyle=(color, bootstyle))
        lbl.pack(padx=5, pady=5, fill=BOTH)

    return frame


def change_style():
    theme = choice(style.theme_names())
    style.theme_use(theme)


if __name__ == '__main__':
    # create visual widget style tests
    root = ttk.Window()
    style = ttk.Style()

    ttk.Button(text="Change Theme", command=change_style).pack(padx=10, pady=10)

    create_label_style('', style, 'Label').pack(side=LEFT)
    create_label_style('inverse', style, 'Inverse Label').pack(side=LEFT)

    root.mainloop()
