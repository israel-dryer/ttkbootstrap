import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style

DARK = 'superhero'
LIGHT = 'flatly'

def create_checkbutton_test(widget_style, style):
    frame = ttk.Frame(padding=10)

    # title
    title = ttk.Label(frame, text=widget_style, anchor=tk.CENTER)
    title.pack(padx=5, pady=2, fill=tk.BOTH)
    ttk.Separator(frame).pack(padx=5, pady=5, fill=tk.X)

    # default style
    cb = ttk.Checkbutton(frame, text=widget_style, style=widget_style)
    cb.pack(padx=5, pady=5, fill=tk.BOTH)
    cb.invoke()

    # color styles
    for color in style.theme.colors:
        cb_style = f'{color}.{widget_style}'
        cb = ttk.Checkbutton(frame, text=cb_style, style=cb_style)
        cb.pack(padx=5, pady=5, fill=tk.BOTH)
        cb.invoke()

    # disabled style
    cb = ttk.Checkbutton(frame, text=widget_style, style=widget_style,
                         state=tk.DISABLED)
    cb.pack(padx=5, pady=5, fill=tk.BOTH)
    cb.invoke()

    return frame


if __name__ == '__main__':
    # create visual widget style tests
    root = tk.Tk()
    style = Style(theme=LIGHT)

    test1 = create_checkbutton_test('TCheckbutton', style)
    test1.pack(side=tk.LEFT, fill=tk.BOTH)
    test2 = create_checkbutton_test('Roundtoggle.Toolbutton', style)
    test2.pack(side=tk.LEFT, fill=tk.BOTH)
    test3 = create_checkbutton_test('Squaretoggle.Toolbutton', style)
    test3.pack(side=tk.LEFT, fill=tk.BOTH)
    test4 = create_checkbutton_test('Toolbutton', style)
    test4.pack(side=tk.LEFT, fill=tk.BOTH)
    test5 = create_checkbutton_test('Outline.Toolbutton', style)
    test5.pack(side=tk.LEFT, fill=tk.BOTH)

    root.mainloop()