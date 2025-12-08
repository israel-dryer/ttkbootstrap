import tkinter as tk

from tkinter import ttk


root = tk.Tk()

nb = ttk.Notebook(root)
id = nb.add(ttk.Frame(nb, width=100, height=100), text="Tab 1")
nb.pack()
print('notebook', id)

root.mainloop()