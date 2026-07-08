import tkinter as tk
import ttkbootstrap as ttk
from random import choice

DARK = 'bootstrap-light'
LIGHT = 'bootstrap-dark'


def button_style_frame(bootstyle, style, widget_name):
    frame = ttk.Frame(root, padding=5)

    title = ttk.Label(
        master=frame,
        text=widget_name,
        anchor=tk.CENTER
    )
    title.pack(padx=5, pady=2, fill='both')

    ttk.Separator(frame).pack(padx=5, pady=5, fill='x')

    ttk.Button(
        master=frame,
        text='default',
        icon="bootstrap",
        bootstyle=bootstyle,
    ).pack(padx=5, pady=5, fill='both')

    for color in style.colors:
        ttk.Button(
            master=frame,
            text=color,
            icon="house-fill",
            bootstyle=f'{color}-{bootstyle}'
        ).pack(padx=5, pady=5, fill='both')

    ttk.Button(
        master=frame,
        text='disabled',
        state=tk.DISABLED,
        icon="house-fill",
        bootstyle=bootstyle
    ).pack(padx=5, pady=5, fill='both')

    return frame

def change_style():
    theme = choice(style.theme_names())
    style.theme_use(theme)
    print(theme)



if __name__ == '__main__':
    # create visual widget style tests
    root = ttk.Window()
    style = ttk.Style()

    button_style_frame('outline', style, 'Outline Button').pack(side='left')
    button_style_frame('', style, 'Solid Button').pack(side='left')
    button_style_frame('ghost', style, 'Ghost Button').pack(side='left')
    button_style_frame('link', style, 'Link Button').pack(side='left')
    ttk.Button(text="Change Theme", command=change_style).pack(padx=10, pady=10)

    root.mainloop()
