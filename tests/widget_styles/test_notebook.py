import tkinter as tk
import ttkbootstrap as ttk
from random import choice
from ttkbootstrap import utility
utility.enable_high_dpi_awareness()

DARK = 'superhero'
LIGHT = 'flatly'

def create_notebook_frame(widget_style, style):
    frame = ttk.Frame(root, padding=5)
    
    # title
    title = ttk.Label(frame, text=widget_style, anchor=tk.CENTER)
    title.pack(padx=5, pady=2, fill=tk.BOTH)
    ttk.Separator(frame).pack(padx=5, pady=5, fill=tk.X)

    # default
    nb = ttk.Notebook(frame, height=50, width=100)
    nb.pack(padx=5, pady=5, fill=tk.BOTH)
    for i, _ in enumerate(style.colors):
        nb.add(ttk.Frame(nb), text=f'Tab {i+1}')

    # other colors
    for color in style.colors:
        nb = ttk.Notebook(frame, bootstyle=color, height=50, width=100)
        nb.pack(padx=5, pady=5, fill=tk.BOTH)
        for i, _ in enumerate(style.colors):
            nb.add(ttk.Frame(nb), text=f'Tab {i+1}')
    return frame

def change_style():
    theme = choice(style.theme_names())
    style.theme_use(theme)    


if __name__ == '__main__':
    # create visual widget style tests
    root = tk.Tk()
    style = ttk.Style()

    ttk.Button(text="Change Theme", command=change_style).pack(padx=10, pady=10)

    create_notebook_frame('TNotebook', style).pack(side=tk.LEFT)

    root.mainloop()