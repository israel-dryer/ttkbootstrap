import ttkbootstrap as ttk
from ttkbootstrap.constants import *


def create_notebook_frame(bootstyle, test_name):
    frame = ttk.Frame(root, padding=5)

    # title
    title = ttk.Label(frame, text=test_name, anchor=CENTER)
    title.pack(padx=5, pady=2, fill=BOTH)
    colors = ['primary', 'secondary', 'success', 'info', 'warning', 'danger']

    # default
    nb = ttk.Notebook(frame, height=50, width=100, variant=bootstyle)
    nb.pack(padx=5, pady=5, fill=BOTH)
    for i, _ in enumerate(colors):
        if i % 2 == 0:
            nb.add(ttk.Frame(nb), text=f'Tab {i + 1}')

    # other colors
    for color in colors:
        nb = ttk.Notebook(frame, color=color, variant=bootstyle, height=50, width=100)
        nb.pack(padx=5, pady=5, fill=BOTH)
        for i, _ in enumerate(colors):
            nb.add(ttk.Frame(nb), text=f'Tab {i + 1}')
    return frame


if __name__ == '__main__':
    # create visual widget style tests
    root = ttk.Window()

    ttk.Button(text="Change Theme", command=ttk.toggle_theme).pack(padx=10, pady=10)

    create_notebook_frame('default', 'Default Notebook').pack(side=LEFT)
    create_notebook_frame('pill', 'Pill Notebook').pack(side=LEFT)
    create_notebook_frame('underline', 'Underline Notebook').pack(side=LEFT)

    root.mainloop()
