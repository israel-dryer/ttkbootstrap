import ttkbootstrap as ttk
from ttkbootstrap.constants import *

def create_checkbutton_test(bootstyle, name):
    frame = ttk.Frame(padding=10)

    # title
    title = ttk.Label(frame, text=name, anchor=CENTER)
    title.pack(padx=5, pady=2, fill=BOTH)
    ttk.Separator(frame).pack(padx=5, pady=5, fill=X)

    # default style
    cb = ttk.Checkbutton(frame, text='default', bootstyle=bootstyle)
    cb.pack(padx=5, pady=5, fill=BOTH)
    cb.invoke()

    # color styles
    for color in ['primary', 'secondary', 'success', 'info', 'warning', 'danger']:
        cb = ttk.Checkbutton(
            master=frame,
            text=color,
            bootstyle=f"{color}-{bootstyle}",
            width=15
        )
        cb.pack(padx=5, pady=5, fill=BOTH)
        cb.invoke()
        print(cb.cget('style'))

    # disabled style
    cb = ttk.Checkbutton(
        master=frame,
        text='disabled',
        bootstyle=bootstyle,
        state=DISABLED
    )
    cb.pack(padx=5, pady=5, fill=BOTH)
    cb.invoke()

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

    test4 = create_checkbutton_test('toolbutton','Toolbutton')
    test4.pack(side='left', fill=BOTH)
    test5 = create_checkbutton_test('outline-toolbutton','Outline Toolbutton')
    test5.pack(side='left', fill=BOTH)
    test6 = create_checkbutton_test('ghost-toolbutton','Ghost Toolbutton')
    test6.pack(side='left', fill=BOTH)

    btn = ttk.Button(text="Change Theme", command=change_style)
    btn.pack(padx=10, pady=10)

    root.mainloop()
