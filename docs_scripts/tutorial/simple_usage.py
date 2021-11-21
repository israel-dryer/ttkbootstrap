import tkinter as tk
import ttkbootstrap as ttk
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)

root = tk.Tk()
style = ttk.Style()  # use default style 'flatly'

b1 = ttk.Button(root, text="Button 1", bootstyle="success")
b1.pack(side=tk.LEFT, padx=5, pady=10)

b2 = ttk.Button(root, text="Button 2", bootstyle="info-outline")
b2.pack(side=tk.LEFT, padx=5, pady=10)

root.mainloop()