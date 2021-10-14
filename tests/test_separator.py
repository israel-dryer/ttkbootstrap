import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style

DARK = 'superhero'
LIGHT = 'flatly'

def create_separator_frame(widget_style, style, orient):
    frame = ttk.Frame(root, padding=5)
    
    # title
    title = ttk.Label(frame, text=widget_style, anchor=tk.CENTER)
    title.pack(padx=5, pady=2, fill=tk.BOTH)
    ttk.Separator(frame).pack(padx=5, pady=5, fill=tk.X)

    # default
    sep = ttk.Separator(frame, style=widget_style, orient=orient)
    if orient == 'h':
        sep.pack(padx=5, pady=5, fill=tk.BOTH)
    else:
        sep.pack(padx=5, pady=5, fill=tk.BOTH, side=tk.LEFT)

    # colored
    for i, color in enumerate(style.colors):
        sep_style = f'{color}.{widget_style}'
        ttk.Label(frame, text=sep_style).pack(fill=tk.X)
        sep = ttk.Separator(frame, style=sep_style, orient=orient)
        if orient == 'h':
            sep.pack(padx=5, pady=5, fill=tk.BOTH)
        else:
            sep.pack(padx=5, pady=5, fill=tk.BOTH, side=tk.LEFT)


    return frame

if __name__ == '__main__':
    # create visual widget style tests
    root = tk.Tk()
    style = Style(theme=LIGHT)

    test1 = create_separator_frame('Horizontal.TSeparator', style, 'h')
    test1.pack(side=tk.LEFT, anchor=tk.N)
    test2 = create_separator_frame('Vertical.TSeparator', style, 'v')
    test2.pack(side=tk.LEFT, anchor=tk.N)

    root.mainloop()