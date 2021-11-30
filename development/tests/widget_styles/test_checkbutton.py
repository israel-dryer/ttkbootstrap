import tkinter as tk
import ttkbootstrap as ttk
from random import choice
from ttkbootstrap import utility
utility.enable_high_dpi_awareness()

DARK = 'superhero'
LIGHT = 'flatly'

def create_checkbutton_test(bootstyle, style, name):
    frame = ttk.Frame(padding=10)

    # title
    title = ttk.Label(frame, text=name, anchor=tk.CENTER)
    title.pack(padx=5, pady=2, fill=tk.BOTH)
    ttk.Separator(frame).pack(padx=5, pady=5, fill=tk.X)

    # default style
    cb = ttk.Checkbutton(frame, text='default', bootstyle=bootstyle)
    cb.pack(padx=5, pady=5, fill=tk.BOTH)
    cb.invoke()

    # color styles
    for color in style.theme.colors:
        cb = ttk.Checkbutton(
            master=frame, 
            text=color, 
            bootstyle=color + bootstyle,
            width=15
        )
        cb.pack(padx=5, pady=5, fill=tk.BOTH)
        cb.invoke()

    # disabled style
    cb = ttk.Checkbutton(
        master=frame, 
        text='disabled', 
        bootstyle=bootstyle,
        state=tk.DISABLED
    )
    cb.pack(padx=5, pady=5, fill=tk.BOTH)
    cb.invoke()

    return frame

def change_style():
    theme = choice(style.theme_names())
    style.theme_use(theme)


if __name__ == '__main__':
    # create visual widget style tests
    root = tk.Tk()
    style = ttk.Style(theme=LIGHT)

    test1 = create_checkbutton_test('', style, 'Checkbutton')
    test1.pack(side=tk.LEFT, fill=tk.BOTH)
    test2 = create_checkbutton_test('round-toggle', style, 'Roundtoggle')
    test2.pack(side=tk.LEFT, fill=tk.BOTH)
    test3 = create_checkbutton_test('square-toggle', style, 'Squaretoggle')
    test3.pack(side=tk.LEFT, fill=tk.BOTH)
    test4 = create_checkbutton_test('toolbutton', style, 'Toolbutton')
    test4.pack(side=tk.LEFT, fill=tk.BOTH)
    test5 = create_checkbutton_test('outline-toolbutton', style, 'Outline Toolbutton')
    test5.pack(side=tk.LEFT, fill=tk.BOTH)

    btn = ttk.Button(text="Change Theme", command=change_style)
    btn.pack(padx=10, pady=10)    

    root.mainloop()