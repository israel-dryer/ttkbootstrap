import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style

DARK = 'superhero'
LIGHT = 'flatly'

def create_progressbar_frame(widget_style, style, orient):
    frame = ttk.Frame(root, padding=5)
    
    # title
    title = ttk.Label(frame, text=widget_style, anchor=tk.CENTER)
    title.pack(padx=5, pady=2, fill=tk.BOTH)
    ttk.Separator(frame).pack(padx=5, pady=5, fill=tk.X)

    # default
    pb = ttk.Progressbar(frame, value=10, style=widget_style, orient=orient)
    if orient == 'h':
        pb.pack(padx=5, pady=5, fill=tk.X)
    else:
        pb.pack(padx=5, pady=5, fill=tk.Y)

    # colored
    for i, color in enumerate(style.colors):
        pb_style = f'{color}.{widget_style}'
        ttk.Label(frame, text=pb_style).pack(fill=tk.X)
        pb = ttk.Progressbar(frame, value=25 + ((i-1)*10), style=pb_style,
                             orient=orient)
        if orient == 'h':
            pb.pack(padx=5, pady=5, fill=tk.X)
        else:
            pb.pack(padx=5, pady=5, fill=tk.Y)
        pb.start()

    return frame

if __name__ == '__main__':
    # create visual widget style tests
    root = tk.Tk()
    style = Style(theme=DARK)

    test1 = create_progressbar_frame('Horizontal.TProgressbar', style, 'h')
    test1.pack(side=tk.LEFT)
    test2 = create_progressbar_frame('Striped.Horizontal.TProgressbar', style, 'h')
    test2.pack(side=tk.LEFT)
    test3 = create_progressbar_frame('Vertical.TProgressbar', style, 'v')
    test3.pack(side=tk.LEFT)
    test4 = create_progressbar_frame('Striped.Vertical.TProgressbar', style, 'v')
    test4.pack(side=tk.LEFT)    

    root.mainloop()