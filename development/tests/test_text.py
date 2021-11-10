import tkinter as tk
import ttkbootstrap as ttk

DARK = 'superhero'
LIGHT = 'flatly'

if __name__ == '__main__':
    # create visual widget style tests
    root = tk.Tk()
    style = ttk.Style(theme=DARK)

    tk.Text(root).pack(padx=10, pady=10)

    root.mainloop()