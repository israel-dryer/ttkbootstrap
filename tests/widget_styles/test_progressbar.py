import tkinter as tk
import ttkbootstrap as ttk
from random import choice
from ttkbootstrap import utility
utility.enable_high_dpi_awareness()

DARK = 'superhero'
LIGHT = 'flatly'


def create_progressbar_frame(bootstyle, style, orient, testname):
    frame = ttk.Frame(root, padding=5)

    # title
    title = ttk.Label(frame, text=testname, anchor=tk.CENTER)
    title.pack(padx=5, pady=2, fill=tk.BOTH)
    ttk.Separator(frame).pack(padx=5, pady=5, fill=tk.X)

    # colored
    for i, color in enumerate(style.colors):
        ttk.Label(frame, text=color).pack(fill=tk.X)
        pb = ttk.Progressbar(
            master=frame,
            value=25 + ((i-1)*10),
            bootstyle=(color, bootstyle),
            orient=orient
        )
        if orient == 'h':
            pb.pack(padx=5, pady=5, fill=tk.X)
        else:
            pb.pack(padx=5, pady=5, fill=tk.Y)
        pb.start()

    return frame


def change_style():
    theme = choice(style.theme_names())
    style.theme_use(theme)    


if __name__ == '__main__':
    # create visual widget style tests
    root = tk.Tk()
    style = ttk.Style()

    ttk.Button(text="Change Theme", command=change_style).pack(padx=10, pady=10)

    test1 = create_progressbar_frame(
        '', style, 'horizontal', 'Solid Progressbar')
    test1.pack(side=tk.LEFT)

    test2 = create_progressbar_frame(
        'striped', style, 'horizontal', 'Striped Progressbar')
    test2.pack(side=tk.LEFT)

    test3 = create_progressbar_frame(
        '', style, 'vertical', 'Solid Progressbar')
    test3.pack(side=tk.LEFT)

    test4 = create_progressbar_frame(
        'striped', style, 'vertical', 'Striped Progressbar')
    test4.pack(side=tk.LEFT)

    root.mainloop()
