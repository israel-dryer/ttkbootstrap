import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.api.style import get_style


def create_frame_test():
    frame = ttk.Frame(padding=10)

    # title
    title = ttk.Label(frame, text='Frame', anchor=CENTER)
    title.pack(padx=5, pady=2, fill=BOTH)
    ttk.Separator(frame).pack(padx=5, pady=5, fill=X)

    # color
    for color in ['default', 'primary', 'secondary', 'success', 'info', 'warning', 'danger']:
        frm = ttk.Frame(frame, bootstyle=color, width=150, height=100)
        frm.pack(padx=5, pady=5)
        frm.pack_propagate(False)
        ttk.Label(master=frm, text=color).pack(fill=BOTH)

    return frame


def change_style():
    if style.theme_use() == 'dark':
        style.theme_use('light')
    else:
        style.theme_use('dark')


if __name__ == '__main__':
    # create visual widget style tests
    root = ttk.Window()
    style = get_style()

    ttk.Button(text="Change Theme", command=change_style).pack(padx=10, pady=10)

    test1 = create_frame_test()
    test1.pack(side=LEFT, fill=BOTH)

    root.mainloop()
