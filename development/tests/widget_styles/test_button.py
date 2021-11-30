import tkinter as tk
import ttkbootstrap as ttk
from random import choice
from ttkbootstrap import utility
utility.enable_high_dpi_awareness()

DARK = 'superhero'
LIGHT = 'flatly'


def button_style_frame(bootstyle, style, widget_name):
    frame = ttk.Frame(root, padding=5)

    title = ttk.Label(
        master=frame,
        text=widget_name,
        anchor=tk.CENTER
    )
    title.pack(padx=5, pady=2, fill=tk.BOTH)

    ttk.Separator(frame).pack(padx=5, pady=5, fill=tk.X)

    ttk.Button(
        master=frame,
        text='default',
        bootstyle=bootstyle
    ).pack(padx=5, pady=5, fill=tk.BOTH)

    for color in style.colors:
        ttk.Button(
            master=frame,
            text=color,
            bootstyle=f'{color}-{bootstyle}'
        ).pack(padx=5, pady=5, fill=tk.BOTH)

    ttk.Button(
        master=frame,
        text='disabled',
        state=tk.DISABLED,
        bootstyle=bootstyle
    ).pack(padx=5, pady=5, fill=tk.BOTH)

    return frame

def change_style():
    theme = choice(style.theme_names())
    style.theme_use(theme)
    print(theme)



if __name__ == '__main__':
    # create visual widget style tests
    root = tk.Tk()
    style = ttk.Style(theme='minty')

    button_style_frame('outline', style, 'Outline Button').pack(side=tk.LEFT)
    button_style_frame('', style, 'Solid Button').pack(side=tk.LEFT)
    button_style_frame('link', style, 'Link Button').pack(side=tk.LEFT)
    ttk.Button(text="Change Theme", command=change_style).pack(padx=10, pady=10)

    root.mainloop()
