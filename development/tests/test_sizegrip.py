import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style

DARK = 'superhero'
LIGHT = 'flatly'


def create_sizegrip_style(bootstyle, style):
    frame = ttk.Frame(root, padding=5)

    # title
    title = ttk.Label(
        master=frame,
        text='Sizegrip',
        anchor=tk.CENTER
    )
    title.pack(padx=5, pady=2, fill=tk.BOTH)
    ttk.Separator(frame).pack(padx=5, pady=5, fill=tk.X)

    # default
    ttk.Label(frame, text=bootstyle).pack(fill=tk.X)
    sg = ttk.Sizegrip(frame)
    sg.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

    # colored
    for color in style.colors:
        ttk.Label(frame, text=color).pack(fill=tk.X)
        sg = ttk.Sizegrip(frame, bootstyle=(color, bootstyle))
        sg.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

    return frame


if __name__ == '__main__':
    # create visual widget style tests
    root = tk.Tk()
    style = Style(theme=LIGHT)

    create_sizegrip_style('', style).pack(
        side=tk.LEFT, fill=tk.BOTH, expand=True
    )

    root.mainloop()
