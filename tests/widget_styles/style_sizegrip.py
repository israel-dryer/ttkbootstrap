import ttkbootstrap as ttk
from ttkbootstrap.constants import *


def create_sizegrip_style(bootstyle):
    frame = ttk.Frame(root, padding=5)

    # title
    title = ttk.Label(
        master=frame,
        text='Sizegrip',
        anchor=CENTER
    )
    title.pack(padx=5, pady=2, fill=BOTH)
    ttk.Separator(frame).pack(padx=5, pady=5, fill=X)

    # default
    ttk.Label(frame, text=bootstyle).pack(fill=X)
    sg = ttk.SizeGrip(frame)
    sg.pack(padx=5, pady=5, fill=BOTH, expand=True)

    return frame


if __name__ == '__main__':
    # create visual widget style tests
    root = ttk.Window()

    ttk.Button(text="Change Theme", command=ttk.toggle_theme).pack(padx=10, pady=10)

    create_sizegrip_style('default').pack(
        side=LEFT, fill=BOTH, expand=True
    )

    root.mainloop()
