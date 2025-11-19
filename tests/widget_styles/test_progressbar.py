import ttkbootstrap as ttk
from ttkbootstrap.constants import *


def create_progressbar_frame(bootstyle, orient, testname):
    frame = ttk.Frame(root, padding=5)

    # title
    title = ttk.Label(frame, text=testname, anchor=CENTER)
    title.pack(padx=5, pady=2, fill=BOTH)
    ttk.Separator(frame).pack(padx=5, pady=5, fill=X)

    for i, color in enumerate(['primary', 'secondary', 'success', 'info', 'warning', 'danger']):
        ttk.Label(frame, text=color).pack(fill=X)
        pb = ttk.Progressbar(
            master=frame,
            value=25 + ((i - 1) * 10),
            bootstyle=f'{color}-{bootstyle}',
            orient=orient
        )
        if orient == 'h':
            pb.pack(padx=5, pady=5, fill=X)
        else:
            pb.pack(padx=5, pady=5, fill=Y)
        pb.start()

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

    test1 = create_progressbar_frame('default', 'horizontal', 'Solid Progressbar')
    test1.pack(side=LEFT)

    test2 = create_progressbar_frame('striped', 'horizontal', 'Striped Progressbar')
    test2.pack(side=LEFT)

    test3 = create_progressbar_frame('default', 'vertical', 'Solid Progressbar')
    test3.pack(side=LEFT)

    test4 = create_progressbar_frame('striped', 'vertical', 'Striped Progressbar')
    test4.pack(side=LEFT)

    root.mainloop()
