import ttkbootstrap as ttk
from ttkbootstrap.constants import *

root = ttk.Window()

frame = ttk.Frame(root, padding=10)
frame.pack(padx=10, pady=10)

de = ttk.DateEntry(frame)
de.pack(fill=X)

root.mainloop()