import ttkbootstrap as ttk
from ttkbootstrap.constants import *

app = ttk.Window()

frame = ttk.Frame(padding=10)
frame.pack(padx=10, pady=10)

for color in app.style.colors:
    b = ttk.Button(frame, text=color, bootstyle=color)
    b.pack(side=LEFT, padx=5, pady=5)

app.mainloop()