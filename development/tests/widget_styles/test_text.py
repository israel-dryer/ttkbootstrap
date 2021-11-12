import tkinter as tk
import ttkbootstrap as ttk
from random import choice

DARK = 'superhero'
LIGHT = 'flatly'

def change_style():
    theme = choice(style.theme_names())
    style.theme_use(theme)    


if __name__ == '__main__':
    # create visual widget style tests
    root = tk.Tk()
    style = ttk.Style()

    ttk.Button(text="Change Theme", command=change_style).pack(padx=10, pady=10)

    tk.Text(root).pack(padx=10, pady=10)

    root.mainloop()