import ttkbootstrap as ttk
from ttkbootstrap.constants import *

root = ttk.Window()

frame = ttk.Frame(padding=5)
frame.pack(padx=10, pady=10)

b1 = ttk.Button(frame, text="Solid Button", bootstyle="success")
b1.pack(side=LEFT, padx=5, pady=10)

b2 = ttk.Button(frame, text="Outline Button", bootstyle="success-outline")
b2.pack(side=LEFT, padx=5, pady=10)

root.mainloop()