import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap import utility
utility.enable_high_dpi_awareness()

root = tk.Tk()
style = ttk.Style()  # use default style 'flatly'

frame = ttk.Frame(padding=5)
frame.pack(padx=10, pady=10)

b1 = ttk.Button(frame, text="Button 1", bootstyle="success")
b1.pack(side=tk.LEFT, padx=5, pady=10)

b2 = ttk.Button(frame, text="Button 2", bootstyle="info-outline")
b2.pack(side=tk.LEFT, padx=5, pady=10)

root.mainloop()