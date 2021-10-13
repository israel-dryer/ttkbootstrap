import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style

DARK = 'superhero'
LIGHT = 'flatly'

def create_frame_test(widget_style, style):
    frame = ttk.Frame(padding=10)

    # title
    title = ttk.Label(frame, text=widget_style, anchor=tk.CENTER)
    title.pack(padx=5, pady=2, fill=tk.BOTH)
    ttk.Separator(frame).pack(padx=5, pady=5, fill=tk.X)

    # default
    frm = ttk.Frame(frame, style=widget_style, width=200, height=100)
    frm.pack(padx=5, pady=5)
    frm.pack_propagate(0)
    ttk.Label(frm, text=widget_style).pack(fill=tk.BOTH)

    # color
    for color in style.theme.colors:
        frm_style = f'{color}.{widget_style}'
        frm = ttk.Frame(frame, style=frm_style, width=150, height=100)
        frm.pack(padx=5, pady=5)
        frm.pack_propagate(0)
        lbl_style = f'{color}.Inverse.TLabel'
        ttk.Label(frm, text=frm_style, style=lbl_style).pack(fill=tk.BOTH)

    return frame


if __name__ == '__main__':
    # create visual widget style tests
    root = tk.Tk()
    style = Style(theme=LIGHT)

    test1 = create_frame_test('TFrame', style)
    test1.pack(side=tk.LEFT, fill=tk.BOTH)
    
    root.mainloop()