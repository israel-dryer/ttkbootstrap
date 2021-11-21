import tkinter as tk
import ttkbootstrap as ttk
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)

root = tk.Tk()
style = ttk.Style()

for color in style.colors:
    b = ttk.Button(root, text=color, bootstyle=color)
    b.pack(side=tk.LEFT, padx=5, pady=5)

root.mainloop()