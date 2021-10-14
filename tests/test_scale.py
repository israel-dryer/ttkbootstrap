import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style

DARK = 'superhero'
LIGHT = 'flatly'

def create_scale_frame(widget_style, style, orient):
    frame = ttk.Frame(root, padding=5)
    
    # title
    title = ttk.Label(frame, text=widget_style, anchor=tk.CENTER)
    title.pack(padx=5, pady=2, fill=tk.BOTH)
    ttk.Separator(frame).pack(padx=5, pady=5, fill=tk.X)

    # default
    pb = ttk.Scale(frame, style=widget_style, orient=orient, value=0.2)
    if orient == 'h':
        pb.pack(padx=5, pady=5, fill=tk.BOTH)
    else:
        pb.pack(padx=5, pady=5, fill=tk.BOTH, side='left')

    # colored
    for color in style.colors:
        pb_style = f'{color}.{widget_style}'
        ttk.Label(frame, text=pb_style).pack(fill=tk.X)
        pb = ttk.Scale(frame, value=0.2, style=pb_style, orient=orient)
        if orient == 'h':
            pb.pack(padx=5, pady=5, fill=tk.BOTH)
        else:
            pb.pack(padx=5, pady=5, fill=tk.BOTH, side='left')

    return frame

if __name__ == '__main__':
    # create visual widget style tests
    root = tk.Tk()
    style = Style(theme=DARK)

    test1 = create_scale_frame('Horizontal.TScale', style, 'h')
    test1.pack(side=tk.LEFT, anchor=tk.N)
    test2 = create_scale_frame('Vertical.TScale', style, 'v')
    test2.pack(side=tk.LEFT, anchor=tk.N)

    root.mainloop()