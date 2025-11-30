import ttkbootstrap as ttk
from ttkbootstrap.constants import *


def create_notebook_frame(bootstyle, test_name):
    frame = ttk.Frame(root, padding=5)

    # title
    title = ttk.Label(frame, text=test_name, anchor=CENTER)
    title.pack(padx=5, pady=2, fill=BOTH)
    colors = ['primary', 'secondary', 'success', 'info', 'warning', 'danger']

    # default
    nb = ttk.Notebook(frame, height=50, width=100, bootstyle=bootstyle)
    nb.pack(padx=5, pady=5, fill=BOTH)
    for i, _ in enumerate(colors):
        if i % 2 == 0:
            nb.add(ttk.Frame(nb), text=f'Tab {i + 1}')

    # other colors
    for color in colors:
        nb = ttk.Notebook(frame, bootstyle=f"{color}-{bootstyle}", height=50, width=100)
        nb.pack(padx=5, pady=5, fill=BOTH)
        for i, _ in enumerate(colors):
            nb.add(ttk.Frame(nb), text=f'Tab {i + 1}')
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

    create_notebook_frame('default', 'Default Notebook').pack(side=LEFT)
    create_notebook_frame('pill', 'Pill Notebook').pack(side=LEFT)
    create_notebook_frame('underline', 'Underline Notebook').pack(side=LEFT)

    root.mainloop()
