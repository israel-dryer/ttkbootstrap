import tkinter as tk
import ttkbootstrap as ttk
from random import choice
from ttkbootstrap import utility
utility.enable_high_dpi_awareness()

DARK = 'superhero'
LIGHT = 'flatly'

def create_scrollbar_frame(style, orient, bootstyle=''):
    frame = ttk.Frame(root, padding=5)
    
    # title
    title = ttk.Label(frame, text=bootstyle.title() + ' Scrollbar', anchor=tk.CENTER)
    title.pack(padx=5, pady=2, fill=tk.BOTH)
    ttk.Separator(frame).pack(padx=5, pady=5, fill=tk.X)

    # default
    ttk.Label(frame, text='default').pack(fill=tk.X)
    sb = ttk.Scrollbar(frame, orient=orient, bootstyle=bootstyle)
    sb.set(0.1, 0.9)
    if orient == tk.HORIZONTAL:
        sb.pack(padx=5, pady=5, fill=tk.X)
    else:
        sb.pack(padx=5, pady=5, fill=tk.Y, side=tk.LEFT)

    # colored
    for _, color in enumerate(style.colors):
        ttk.Label(frame, text=color).pack(fill=tk.X)
        sb = ttk.Scrollbar(frame, bootstyle=(color, bootstyle), orient=orient)
        sb.set(0.1, 0.3)
        if orient == tk.HORIZONTAL:
            sb.pack(padx=5, pady=5, fill=tk.X, expand=tk.YES)
        else:
            sb.pack(padx=5, pady=5, fill=tk.Y, side=tk.LEFT, 
                    expand=tk.YES)

    return frame

def change_style():
    theme = choice(style.theme_names())
    style.theme_use(theme)    


if __name__ == '__main__':
    # create visual widget style tests
    root = tk.Tk()
    root.geometry('1000x500')
    style = ttk.Style()

    ttk.Button(text="Change Theme", command=change_style).pack(padx=10, pady=10)
    test1 = create_scrollbar_frame(
        style=style, 
        orient=tk.HORIZONTAL
    )
    test1.pack(side=tk.LEFT, anchor=tk.N, fill=tk.BOTH, expand=tk.YES)
    
    test2 = create_scrollbar_frame(
        style=style, 
        orient=tk.VERTICAL
    )
    test2.pack(side=tk.LEFT, anchor=tk.N, fill=tk.BOTH, expand=tk.YES)

    test3 = create_scrollbar_frame(
        style=style, 
        orient=tk.HORIZONTAL,
        bootstyle='round'
    )
    test3.pack(side=tk.LEFT, anchor=tk.N, fill=tk.BOTH, expand=tk.YES)
    
    test4 = create_scrollbar_frame(
        style=style, 
        orient=tk.VERTICAL,
        bootstyle='round'
    )
    test4.pack(side=tk.LEFT, anchor=tk.N, fill=tk.BOTH, expand=tk.YES)


    root.mainloop()