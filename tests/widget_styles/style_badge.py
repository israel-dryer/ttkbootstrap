import ttkbootstrap as ttk
from ttkbootstrap.constants import *


def create_badge_style(variant, test_name):
    frame = ttk.Frame(root, padding=5)

    # title
    title = ttk.Label(frame, text=test_name, anchor=CENTER)
    title.pack(padx=5, pady=2, fill=BOTH)
    ttk.Separator(frame).pack(padx=5, pady=5, fill=X)

    # default
    badge = ttk.Badge(frame, text='default', variant=variant)
    badge.pack(padx=5, pady=5)

    # colored
    for color in ['primary', 'secondary', 'success', 'info', 'warning', 'danger']:
        lbl = ttk.Badge(frame, text=color, accent=color, variant=variant, anchor='center')
        lbl.pack(padx=5, pady=5)

    return frame


if __name__ == '__main__':
    # create visual widget style tests
    root = ttk.Window()
    style = ttk.Style()

    ttk.Button(text="Change Theme", command=ttk.toggle_theme).pack(padx=10, pady=10)

    create_badge_style('square', 'Square').pack(side=LEFT)
    create_badge_style('pill', 'Pill').pack(side=LEFT)

    root.mainloop()
