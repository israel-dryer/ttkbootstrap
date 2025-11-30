import ttkbootstrap as ttk
from ttkbootstrap.constants import *


def create_label_style(bootstyle, test_name):
    frame = ttk.Frame(root, padding=5)

    # title
    title = ttk.Label(frame, text=test_name, anchor=CENTER)
    title.pack(padx=5, pady=2, fill=BOTH)
    ttk.Separator(frame).pack(padx=5, pady=5, fill=X)

    # default
    lbl = ttk.Label(frame, text='de', bootstyle=bootstyle)
    lbl.pack(padx=5, pady=5, fill=BOTH)

    # colored
    for color in ['primary', 'secondary', 'success', 'info', 'warning', 'danger']:
        lbl = ttk.Label(frame, text=color, bootstyle=f'{color}-{bootstyle}')
        lbl.pack(padx=5, pady=5, fill=BOTH)

    return frame


def change_style():
    if style.theme_use() == 'dark':
        style.theme_use('light')
    else:
        style.theme_use('dark')


if __name__ == '__main__':
    # create visual widget style tests
    root = ttk.Window()
    style = ttk.Style()

    ttk.Button(text="Change Theme", command=change_style).pack(padx=10, pady=10)

    create_label_style('badge', 'Default').pack(side=LEFT)
    create_label_style('pill-badge', 'Pill').pack(side=LEFT)

    root.mainloop()
