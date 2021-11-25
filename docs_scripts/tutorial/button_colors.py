import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.style import utility

root = tk.Tk()
utility.enable_high_dpi_awareness(root)
style = ttk.Style()

frame = ttk.Frame(padding=10)
frame.pack(padx=10, pady=10)

for color in style.colors:
    b = ttk.Button(frame, text=color, bootstyle=color)
    b.pack(side=tk.LEFT, padx=5, pady=5)

root.mainloop()