import tkinter as tk
from tkinter import ttk

root = tk.Tk()

cbo = ttk.Combobox(root, values=['one', 'two', 'three'])
cbo.pack(padx=20, pady=20)
cbo.set(0)

cbo = ttk.Combobox(root, values=['one', 'two', 'three'])
cbo.pack(padx=20, pady=20)
cbo.set(0)


root.mainloop()