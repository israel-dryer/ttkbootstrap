import tkinter as tk
import ttkbootstrap as ttk

DARK = 'superhero'
LIGHT = 'flatly'

def create_separator_frame(widget_style, style, orient):
    frame = ttk.Frame(root, padding=5)
    
    # title
    title = ttk.Label(
        master=frame, 
        text=orient.title() + ' Separator', 
        anchor=tk.CENTER
    )
    title.pack(padx=5, pady=2, fill=tk.BOTH)
    ttk.Separator(frame).pack(padx=5, pady=5, fill=tk.X)

    # default
    sep = ttk.Separator(frame, orient=orient)
    if orient == tk.HORIZONTAL:
        sep.pack(padx=5, pady=5, fill=tk.BOTH)
    else:
        sep.pack(padx=5, pady=5, fill=tk.BOTH, side=tk.LEFT)

    # colored
    for i, color in enumerate(style.colors):
        ttk.Label(frame, text=color).pack(fill=tk.X)
        sep = ttk.Separator(
            master=frame, 
            bootstyle=color, 
            orient=orient
        )
        if orient == tk.HORIZONTAL:
            sep.pack(padx=5, pady=5, fill=tk.BOTH)
        else:
            sep.pack(padx=5, pady=5, fill=tk.BOTH, side=tk.LEFT)


    return frame

if __name__ == '__main__':
    # create visual widget style tests
    root = tk.Tk()
    style = ttk.Style(theme=DARK)

    test1 = create_separator_frame('', style, tk.HORIZONTAL)
    test1.pack(side=tk.LEFT, anchor=tk.N)
    test2 = create_separator_frame('', style, tk.VERTICAL)
    test2.pack(side=tk.LEFT, anchor=tk.N)

    root.mainloop()