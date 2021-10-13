import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style

DARK = 'superhero'
LIGHT = 'flatly'

def create_combobox_test(widget_style, style):
    frame = ttk.Frame(padding=10)

    # title
    title = ttk.Label(frame, text=widget_style, anchor=tk.CENTER)
    title.pack(padx=5, pady=2, fill=tk.BOTH)
    ttk.Separator(frame).pack(padx=5, pady=5, fill=tk.X)

    # default style
    cbo = ttk.Combobox(frame, values=[widget_style, 'other'], 
                       style=widget_style)
    cbo.pack(padx=5, pady=5, fill=tk.BOTH)
    cbo.current(0)

    # color styles
    for color in style.theme.colors:
        cbo_style = f'{color}.{widget_style}'
        cbo = ttk.Combobox(frame, values=[cbo_style, 'other'], 
                           style=cbo_style)
        cbo.pack(padx=5, pady=5, fill=tk.BOTH)
        cbo.current(0)

    # disabled style
    cbo = ttk.Combobox(frame, values=[widget_style,'other'], 
                       style=widget_style, state=tk.DISABLED)
    cbo.pack(padx=5, pady=5, fill=tk.BOTH)
    cbo.current(0)

    return frame


if __name__ == '__main__':
    # create visual widget style tests
    root = tk.Tk()
    style = Style(theme=LIGHT)

    test1 = create_combobox_test('TCombobox', style)
    test1.pack(side=tk.LEFT, fill=tk.BOTH)

    root.mainloop()