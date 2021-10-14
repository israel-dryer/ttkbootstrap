import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style

DARK = 'superhero'
LIGHT = 'flatly'

def create_spinbox_test(widget_style, style):
    frame = ttk.Frame(padding=10)

    # title
    title = ttk.Label(frame, text=widget_style, anchor=tk.CENTER)
    title.pack(padx=5, pady=2, fill=tk.BOTH)
    ttk.Separator(frame).pack(padx=5, pady=5, fill=tk.X)

    # default
    spinbox = ttk.Spinbox(frame, style=widget_style)
    spinbox.pack(padx=5, pady=5, fill=tk.BOTH)
    spinbox.insert('end', widget_style)

    # color
    for color in style.theme.colors:
        cbo_style = f'{color}.{widget_style}'
        spinbox = ttk.Spinbox(frame, style=cbo_style)
        spinbox.pack(padx=5, pady=5, fill=tk.BOTH)
        spinbox.insert('end', cbo_style)

    # disabled 
    spinbox = ttk.Spinbox(frame, style=widget_style)
    spinbox.insert('end', widget_style)
    spinbox.configure(state=tk.DISABLED)
    spinbox.pack(padx=5, pady=5, fill=tk.BOTH)

    return frame


if __name__ == '__main__':
    # create visual widget style tests
    root = tk.Tk()
    style = Style(theme=DARK)

    test1 = create_spinbox_test('TSpinbox', style)
    test1.pack(side=tk.LEFT, fill=tk.BOTH)

    root.mainloop()