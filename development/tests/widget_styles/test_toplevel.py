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

    ttk.Label(root, text="Root").pack(padx=10, pady=10)

    top = tk.Toplevel(root)
    ttk.Label(top, text="Toplevel").pack(padx=10, pady=10)

    btn = ttk.Button(top, text="Change Theme", command=change_style)
    btn.pack(padx=10, pady=10)

    root.mainloop()