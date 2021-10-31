import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style

DARK = 'superhero'
LIGHT = 'flatly'


def create_label_style(bootstyle, style, test_name):
    frame = ttk.Frame(root, padding=5)

    # title
    title = ttk.Label(frame, text=test_name, anchor=tk.CENTER)
    title.pack(padx=5, pady=2, fill=tk.BOTH)
    ttk.Separator(frame).pack(padx=5, pady=5, fill=tk.X)

    # default
    lbl = ttk.Label(frame, text='default', bootstyle=bootstyle)
    lbl.pack(padx=5, pady=5, fill=tk.BOTH)

    # colored
    for color in style.colors:
        lbl = ttk.Label(frame, text=color, bootstyle=(color, bootstyle))
        lbl.pack(padx=5, pady=5, fill=tk.BOTH)

    return frame


if __name__ == '__main__':
    # create visual widget style tests
    root = tk.Tk()
    style = Style(theme=LIGHT)

    create_label_style('', style, 'Label').pack(side=tk.LEFT)
    create_label_style('inverse', style, 'Inverse Label').pack(side=tk.LEFT)

    root.mainloop()
