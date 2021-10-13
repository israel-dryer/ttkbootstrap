import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style

DARK = 'superhero'
LIGHT = 'flatly'

def create_label_style(widget_style, style):
    frame = ttk.Frame(root, padding=5)
    
    # title
    title = ttk.Label(frame, text=widget_style, anchor=tk.CENTER)
    title.pack(padx=5, pady=2, fill=tk.BOTH)
    ttk.Separator(frame).pack(padx=5, pady=5, fill=tk.X)

    # default button
    lbl = ttk.Label(frame, text=widget_style, style=widget_style)
    lbl.pack(padx=5, pady=5, fill=tk.BOTH)

    # colored buttons
    for color in style.colors:
        label_style = f'{color}.{widget_style}'
        lbl = ttk.Label(frame, text=label_style, style=label_style)
        lbl.pack(padx=5, pady=5, fill=tk.BOTH)

    return frame

if __name__ == '__main__':
    # create visual widget style tests
    root = tk.Tk()
    style = Style(theme=LIGHT)

    create_label_style('TLabel', style).pack(side=tk.LEFT)
    create_label_style('Inverse.TLabel', style).pack(side=tk.LEFT)

    root.mainloop()