import ttkbootstrap as ttk
from ttkbootstrap.constants import *


def create_menubutton_frame(bootstyle, testname):
    frame = ttk.Frame(root, padding=5)

    title = ttk.Label(
        master=frame,
        text=testname,
        anchor=CENTER
    )
    title.pack(padx=5, pady=2, fill=BOTH)

    ttk.Separator(frame).pack(padx=5, pady=5, fill=X)

    btn = ttk.MenuButton(
        master=frame,
        bootstyle=bootstyle,
        text='default',
    )
    btn.pack(padx=5, pady=5, fill=BOTH)

    for color in ['primary', 'secondary', 'success', 'info', 'warning', 'danger']:
        btn = ttk.MenuButton(
            master=frame,
            text=color,
            bootstyle=f"{color}-{bootstyle}"
        )
        btn.pack(padx=5, pady=5, fill=BOTH)

    btn = ttk.MenuButton(
        master=frame,
        text='disabled',
        state=DISABLED,
        bootstyle=bootstyle,
    )
    btn.pack(padx=5, pady=5, fill=BOTH)

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

    create_menubutton_frame("default", 'Solid Menubutton').pack(side=LEFT)
    create_menubutton_frame('outline', 'Outline Menubutton').pack(side=LEFT)
    create_menubutton_frame('ghost', 'Ghost Menubutton').pack(side=LEFT)
    create_menubutton_frame('text', 'Text Menubutton').pack(side=LEFT)

    root.mainloop()
