import ttkbootstrap as ttk
from ttkbootstrap.constants import *


def create_separator_frame(orient):
    frame = ttk.Frame(root, padding=5)

    # title
    title = ttk.Label(
        master=frame,
        text=orient.title() + ' Separator',
        anchor=CENTER
    )
    title.pack(padx=5, pady=2, fill=BOTH)
    ttk.Separator(frame).pack(padx=5, pady=5, fill=X)

    # default
    sep = ttk.Separator(frame, orient=orient)
    if orient == HORIZONTAL:
        sep.pack(padx=5, pady=5, fill=BOTH)
    else:
        sep.pack(padx=5, pady=5, fill=BOTH, side=LEFT)

    # colored
    for i, color in enumerate(['primary', 'secondary', 'success', 'info', 'warning', 'danger']):
        ttk.Label(frame, text=color).pack(fill=X)
        sep = ttk.Separator(
            master=frame,
            color=color,
            orient=orient
        )
        if orient == HORIZONTAL:
            sep.pack(padx=5, pady=5, fill=BOTH)
        else:
            sep.pack(padx=5, pady=5, fill=BOTH, side=LEFT)

    return frame


def change_style():
    if style.theme_use() == 'light':
        style.theme_use('dark')
    else:
        style.theme_use('light')


if __name__ == '__main__':
    # create visual widget style tests
    root = ttk.Window()
    style = ttk.Style()

    ttk.Button(text="Change Theme", command=change_style).pack(padx=10, pady=10)

    test1 = create_separator_frame(HORIZONTAL)
    test1.pack(side=LEFT, anchor=N)

    test1 = create_separator_frame(VERTICAL)
    test1.pack(side=LEFT, anchor=N)

    root.mainloop()
