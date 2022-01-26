import tkinter as tk
import ttkbootstrap as ttk
from random import choice
from ttkbootstrap import utility
utility.enable_high_dpi_awareness()

DARK = 'superhero'
LIGHT = 'flatly'


def create_frame_test(bootstyle, style):
    frame = ttk.Frame(padding=10)

    # title
    title = ttk.Label(frame, text='Frame', anchor=tk.CENTER)
    title.pack(padx=5, pady=2, fill=tk.BOTH)
    ttk.Separator(frame).pack(padx=5, pady=5, fill=tk.X)

    # default
    frm = ttk.Frame(frame, style=bootstyle, width=150, height=100)
    frm.pack(padx=5, pady=5)
    frm.pack_propagate(0)
    ttk.Label(frm, text='default').pack(fill=tk.BOTH)

    # color
    for color in style.theme.colors:
        frm = ttk.Frame(frame, bootstyle=color, width=150, height=100)
        frm.pack(padx=5, pady=5)
        frm.pack_propagate(0)
        ttk.Label(
            master=frm,
            text=color,
            bootstyle=(color, 'inverse')
        ).pack(fill=tk.BOTH)

    return frame


def change_style():
    theme = choice(style.theme_names())
    style.theme_use(theme)    


if __name__ == '__main__':
    # create visual widget style tests
    root = tk.Tk()
    style = ttk.Style()

    ttk.Button(text="Change Theme", command=change_style).pack(padx=10, pady=10)

    test1 = create_frame_test('TFrame', style)
    test1.pack(side=tk.LEFT, fill=tk.BOTH)

    root.mainloop()
