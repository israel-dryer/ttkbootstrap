import ttkbootstrap as ttk
from ttkbootstrap.constants import *


def create_labelframe_style():
    frame = ttk.Frame(root, padding=5)

    # title
    title = ttk.Label(frame, text='Labelframe', anchor=CENTER)
    title.pack(padx=5, pady=2, fill=BOTH)
    ttk.Separator(frame).pack(padx=5, pady=5, fill=X)

    # default
    lbl = ttk.LabelFrame(
        master=frame,
        text='default',
        width=150,
        height=75
    )
    lbl.pack(padx=5, pady=5, fill=BOTH)

    # colored
    for color in ['primary', 'secondary', 'success', 'info', 'warning', 'danger']:
        lbl = ttk.LabelFrame(
            master=frame,
            text=color,
            color=color,
            width=150,
            height=75
        )
        lbl.pack(padx=5, pady=5, fill=BOTH)

    return frame


if __name__ == '__main__':
    # create visual widget style tests
    root = ttk.Window()

    ttk.Button(text="Change Theme", command=ttk.toggle_theme).pack(padx=10, pady=10)

    create_labelframe_style().pack(side=LEFT)

    root.mainloop()
