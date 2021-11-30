import tkinter as tk
import ttkbootstrap as ttk
from random import choice
from ttkbootstrap import utility
utility.enable_high_dpi_awareness()

def change_style():
    theme = choice(style.theme_names())
    style.theme_use(theme)    


if __name__ == '__main__':
    # create visual widget style tests
    root = tk.Tk()
    style = ttk.Style()

    ttk.Button(text="Change Theme", command=change_style).pack(padx=10, pady=10)
    var = tk.Variable()
    om = ttk.OptionMenu(root, var, 'default', *style.colors)
    om.pack(padx=10, pady=10, fill=tk.X)

    for i, color in enumerate(style.colors):
        var = tk.Variable()
        om = ttk.OptionMenu(root, var, color, *style.colors, bootstyle=color)
        om.pack(padx=10, pady=10, fill=tk.X)

    root.mainloop()


