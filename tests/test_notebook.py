import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style

DARK = 'superhero'
LIGHT = 'flatly'

def create_notebook_frame(widget_style, style):
    frame = ttk.Frame(root, padding=5)
    
    # title
    title = ttk.Label(frame, text=widget_style, anchor=tk.CENTER)
    title.pack(padx=5, pady=2, fill=tk.BOTH)
    ttk.Separator(frame).pack(padx=5, pady=5, fill=tk.X)

    # default button
    nb = ttk.Notebook(frame, style=widget_style, height=50, width=100)
    nb.pack(padx=5, pady=5, fill=tk.BOTH)
    for i, _ in enumerate(style.colors):
        nb.add(ttk.Frame(nb), text=f'Tab {i+1}')

    return frame

if __name__ == '__main__':
    # create visual widget style tests
    root = tk.Tk()
    style = Style(theme=DARK)

    create_notebook_frame('TNotebook', style).pack(side=tk.LEFT)

    root.mainloop()