import tkinter as tk
import ttkbootstrap as ttk
from random import choice
from ttkbootstrap import utility
utility.enable_high_dpi_awareness()

DARK = 'superhero'
LIGHT = 'flatly'


def create_menubutton_frame(bootstyle, style, testname):
    frame = ttk.Frame(root, padding=5)

    title = ttk.Label(
        master=frame,
        text=testname,
        anchor=tk.CENTER
    )
    title.pack(padx=5, pady=2, fill=tk.BOTH)

    ttk.Separator(frame).pack(padx=5, pady=5, fill=tk.X)

    btn = ttk.Menubutton(
        master=frame,
        text='default',
        bootstyle=bootstyle
    )
    btn.pack(padx=5, pady=5, fill=tk.BOTH)

    for color in style.colors:
        btn = ttk.Menubutton(
            master=frame,
            text=color,
            bootstyle=(color, bootstyle)
        )
        btn.pack(padx=5, pady=5, fill=tk.BOTH)

    btn = ttk.Menubutton(
        master=frame,
        text='disabled',
        state=tk.DISABLED,
        bootstyle=bootstyle
    )
    btn.pack(padx=5, pady=5, fill=tk.BOTH)

    return frame


def change_style():
    theme = choice(style.theme_names())
    style.theme_use(theme)    


if __name__ == '__main__':
    # create visual widget style tests
    root = tk.Tk()
    style = ttk.Style()

    ttk.Button(text="Change Theme", command=change_style).pack(padx=10, pady=10)

    create_menubutton_frame(
        '', style, 'Solid Menubutton'
    ).pack(side=tk.LEFT)
    
    create_menubutton_frame(
        'outline', style, 'Outline Menubutton'
    ).pack(side=tk.LEFT)

    root.mainloop()
