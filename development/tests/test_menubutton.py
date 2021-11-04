import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style

DARK = 'superhero'
LIGHT = 'flatly'


def create_menubutton_frame(bootstyle, style, testname):
    frame = ttk.Frame(root, padding=5)

    title = ttk.Label(
        master=frame,
        text=testname,
        anchor=tk.CENTER
    )
    title.pack(padx=5, pady=2, fill=tk.BOTH)

    ttk.Separator(frame).pack(padx=5, pady=5, fill=tk.X)

    btn = ttk.Menubutton(
        master=frame,
        text='default',
        bootstyle=bootstyle
    )
    btn.pack(padx=5, pady=5, fill=tk.BOTH)

    for color in style.colors:
        btn = ttk.Menubutton(
            master=frame,
            text=color,
            bootstyle=(color, bootstyle)
        )
        btn.pack(padx=5, pady=5, fill=tk.BOTH)

    btn = ttk.Menubutton(
        master=frame,
        text='disabled',
        state=tk.DISABLED,
        bootstyle=bootstyle
    )
    btn.pack(padx=5, pady=5, fill=tk.BOTH)

    return frame


if __name__ == '__main__':
    root = tk.Tk()
    style = Style(theme=DARK)

    create_menubutton_frame(
        '', style, 'Solid Menubutton'
    ).pack(side=tk.LEFT)
    
    create_menubutton_frame(
        'outline', style, 'Outline Menubutton'
    ).pack(side=tk.LEFT)

    root.mainloop()
