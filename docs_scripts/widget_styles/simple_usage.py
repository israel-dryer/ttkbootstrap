import tkinter as tk
import ttkbootstrap as ttk

root = tk.Tk()
style = ttk.Style()  # use default style 'flatly'

b1 = ttk.Button(root, text="Solid Button", bootstyle="success")
b1.pack(side=tk.LEFT, padx=5, pady=10)

b2 = ttk.Button(root, text="Outline Button", bootstyle="success-outline")
b2.pack(side=tk.LEFT, padx=5, pady=10)

root.mainloop()
