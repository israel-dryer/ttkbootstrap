import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style

DARK = 'superhero'
LIGHT = 'flatly'

def create_sizegrip_style(widget_style, style):
    frame = ttk.Frame(root, padding=5)
    
    # title
    title = ttk.Label(frame, text=widget_style, anchor=tk.CENTER)
    title.pack(padx=5, pady=2, fill=tk.BOTH)
    ttk.Separator(frame).pack(padx=5, pady=5, fill=tk.X)

    # default
    ttk.Label(frame, text=widget_style).pack(fill=tk.X)
    sg = ttk.Sizegrip(frame, style=widget_style)
    sg.pack(padx=5, pady=5, fill=tk.BOTH)

    # colored 
    for color in style.colors:
        sg_style = f'{color}.{widget_style}'
        ttk.Label(frame, text=sg_style).pack(fill=tk.X)
        sg = ttk.Sizegrip(frame, style=sg_style)
        sg.pack(padx=5, pady=5, fill=tk.BOTH)

    return frame

if __name__ == '__main__':
    # create visual widget style tests
    root = tk.Tk()
    style = Style(theme=DARK)

    create_sizegrip_style('TSizegrip', style).pack(side=tk.LEFT)

    root.mainloop()