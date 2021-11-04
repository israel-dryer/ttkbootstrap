import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style

DARK = 'superhero'
LIGHT = 'flatly'

if __name__ == '__main__':
    # create visual widget style tests
    root = tk.Tk()
    style = Style(theme=LIGHT)

    lb = tk.Listbox(root)
    lb.pack(padx=10, pady=10)
    lb.insert('end', *list(range(5)))
    print(lb.exists)

    root.mainloop()