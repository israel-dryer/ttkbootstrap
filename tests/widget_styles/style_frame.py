import ttkbootstrap as ttk
from ttkbootstrap.constants import *


def create_frame_test():
    frame = ttk.Frame(padding=10)

    # title
    title = ttk.Label(frame, text='Frame', anchor=CENTER)
    title.pack(padx=5, pady=2, fill=BOTH)
    ttk.Separator(frame).pack(padx=5, pady=5, fill=X)

    # color
    for color in ['primary', 'secondary', 'success', 'info', 'warning', 'danger']:
        frm = ttk.Frame(frame, accent=color, width=150, height=100)
        frm.pack(padx=5, pady=5)
        frm.pack_propagate(False)
        ttk.Label(master=frm, text=color).pack(fill=BOTH)

    return frame


if __name__ == '__main__':
    root = ttk.Window()

    ttk.Button(text="Change Theme", command=ttk.toggle_theme).pack(padx=10, pady=10)

    test1 = create_frame_test()
    test1.pack(side=LEFT, fill=BOTH)

    root.mainloop()
