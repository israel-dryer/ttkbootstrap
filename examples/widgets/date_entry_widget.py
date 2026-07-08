import ttkbootstrap as ttk
from ttkbootstrap.constants import *

root = ttk.Window()

frame = ttk.Frame(root, padding=10)
frame.pack(padx=10, pady=10)

de = ttk.DateEntry(frame)

ttk.Button(frame, text="TtkBootstrap", icon="house", icon_size=14).pack()

de.pack(fill=X)

root.mainloop()

