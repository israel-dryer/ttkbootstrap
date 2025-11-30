import ttkbootstrap as ttk
from ttkbootstrap.constants import *


def create_panedwindow_frame():
    frame = ttk.Frame(root, padding=5)

    # title
    title = ttk.Label(frame, text='Paned Window', anchor=CENTER)
    title.pack(padx=5, pady=2, fill=BOTH)
    ttk.Separator(frame).pack(padx=5, pady=5, fill=X)

    # default
    pw = ttk.Panedwindow(frame)
    pw.pack(padx=5, pady=5, fill=BOTH)
    pw.add(ttk.Frame(pw, width=100, height=50, bootstyle='info'))
    pw.add(ttk.Frame(pw, width=100, height=50, bootstyle='success'))

    for color in ['primary', 'secondary', 'success', 'info', 'warning', 'danger']:
        pw = ttk.Panedwindow(frame, bootstyle=color)
        pw.pack(padx=5, pady=5, fill=BOTH)
        pw.add(ttk.Frame(pw, width=100, height=50))
        pw.add(ttk.Frame(pw, width=100, height=50))

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
    create_panedwindow_frame().pack(side=LEFT)

    root.mainloop()
