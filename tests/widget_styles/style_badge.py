import ttkbootstrap as ttk
from ttkbootstrap.constants import *


def create_label_style(bootstyle, test_name):
    frame = ttk.Frame(root, padding=5)

    # title
    title = ttk.Label(frame, text=test_name, anchor=CENTER)
    title.pack(padx=5, pady=2, fill=BOTH)
    ttk.Separator(frame).pack(padx=5, pady=5, fill=X)

    # default
    badge = ttk.Badge(frame, text='de', variant=bootstyle)
    badge.pack(padx=5, pady=5, fill=BOTH)

    # colored
    for color in ['primary', 'secondary', 'success', 'info', 'warning', 'danger']:
        lbl = ttk.Badge(frame, text=color, color=color)
        lbl.pack(padx=5, pady=5, fill=BOTH)

    return frame


if __name__ == '__main__':
    # create visual widget style tests
    root = ttk.Window()
    style = ttk.Style()

    ttk.Button(text="Change Theme", command=ttk.toggle_theme).pack(padx=10, pady=10)

    create_label_style('default', 'Default').pack(side=LEFT)
    create_label_style('pill', 'Pill').pack(side=LEFT)

    root.mainloop()
