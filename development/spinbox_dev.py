import tkinter as tk
from tkinter import ttk


root = tk.Tk()


sb = ttk.Spinbox(root)
sb.pack(padx=10, pady=10)

en = ttk.Entry(root, style='TSpinbox')
en.pack(padx=10, pady=10)


root.mainloop()