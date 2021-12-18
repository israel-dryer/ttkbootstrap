import ttkbootstrap as ttk
from ttkbootstrap.constants import *

app = ttk.Window()

frame = ttk.Frame(padding=5)
frame.pack(padx=10, pady=10)

b1 = ttk.Button(frame, text="Button 1", bootstyle="success")
b1.pack(side=LEFT, padx=5, pady=10)

b2 = ttk.Button(frame, text="Button 2", bootstyle="info-outline")
b2.pack(side=LEFT, padx=5, pady=10)

app.mainloop()