import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style

DARK = 'superhero'
LIGHT = 'flatly'

def create_entry_test(widget_style, style):
    frame = ttk.Frame(padding=10)

    # title
    title = ttk.Label(frame, text=widget_style, anchor=tk.CENTER)
    title.pack(padx=5, pady=2, fill=tk.BOTH)
    ttk.Separator(frame).pack(padx=5, pady=5, fill=tk.X)

    # default
    entry = ttk.Entry(frame, style=widget_style)
    entry.pack(padx=5, pady=5, fill=tk.BOTH)
    entry.insert('end', widget_style)

    # color
    for color in style.theme.colors:
        cbo_style = f'{color}.{widget_style}'
        entry = ttk.Entry(frame, style=cbo_style)
        entry.pack(padx=5, pady=5, fill=tk.BOTH)
        entry.insert('end', cbo_style)

    # disabled 
    entry = ttk.Entry(frame, style=widget_style)
    entry.insert('end', widget_style)
    entry.configure(state=tk.DISABLED)
    entry.pack(padx=5, pady=5, fill=tk.BOTH)

    return frame


if __name__ == '__main__':
    # create visual widget style tests
    root = tk.Tk()
    style = Style(theme=DARK)

    test1 = create_entry_test('TEntry', style)
    test1.pack(side=tk.LEFT, fill=tk.BOTH)

    root.mainloop()