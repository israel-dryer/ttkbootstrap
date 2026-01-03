import ttkbootstrap as ttk
from ttkbootstrap.constants import *


def create_label_style(test_name):
    frame = ttk.Frame(root, padding=5)

    # title
    title = ttk.Label(frame, text=test_name, anchor=CENTER)
    title.pack(padx=5, pady=2, fill=BOTH)
    ttk.Separator(frame).pack(padx=5, pady=5, fill=X)

    # default
    lbl = ttk.Label(frame, text='default')
    lbl.pack(padx=5, pady=5, fill=X)

    # colored
    for color in ['primary', 'secondary', 'success', 'info', 'warning', 'danger']:
        lbl = ttk.Label(frame, text=color, accent=color)
        lbl.pack(padx=5, pady=5, fill=X)

    return frame


if __name__ == '__main__':
    # create visual widget style tests
    root = ttk.Window()

    ttk.Button(text="Change Theme", command=ttk.toggle_theme).pack(padx=10, pady=10)

    create_label_style('Label').pack(side=LEFT, fill=X)

    root.mainloop()
