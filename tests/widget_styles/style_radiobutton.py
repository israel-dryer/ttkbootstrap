import ttkbootstrap as ttk
from ttkbootstrap.constants import *


def create_radiobutton_test(bootstyle, testname):
    frame = ttk.Frame(padding=10)

    var = ttk.Variable()

    # title
    title = ttk.Label(frame, text=testname, anchor=CENTER)
    title.pack(padx=5, pady=2, fill=BOTH)
    ttk.Separator(frame).pack(padx=5, pady=5, fill=X)

    # default style
    cb = ttk.Radiobutton(frame, text='default', bootstyle=bootstyle, value=0)
    cb.configure(variable=var)
    cb.pack(padx=5, pady=5, fill=BOTH)
    cb.invoke()

    # color styles
    for i, color in enumerate(['primary', 'secondary', 'success', 'info', 'warning', 'danger']):
        cb = ttk.Radiobutton(frame, text=color, bootstyle=f'{color}-{bootstyle}')
        cb.configure(variable=var, value=i + 1)
        cb.pack(padx=5, pady=5, fill=BOTH)
        cb.invoke()

    # disabled style
    cb = ttk.Radiobutton(
        master=frame,
        text='disabled',
        bootstyle=bootstyle,
        state=DISABLED,
        variable=var,
        value=i + 1
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

    ttk.Button(text="Change Theme", command=change_style).pack(padx=10, pady=10)

    test1 = create_radiobutton_test('default', 'Radiobutton')
    test1.pack(side=LEFT, fill=BOTH)
    test4 = create_radiobutton_test('toolbutton', 'Toolbutton')
    test4.pack(side=LEFT, fill=BOTH)
    test5 = create_radiobutton_test('outline-toolbutton', 'Outline Toolbutton')
    test5.pack(side=LEFT, fill=BOTH)
    create_radiobutton_test('ghost-toolbutton', 'Ghost Toolbutton').pack(side=LEFT, fill=BOTH)

    root.mainloop()
