import ttkbootstrap as ttk
from ttkbootstrap.constants import *

root = ttk.Window()

frame = ttk.Frame(root, padding=10)
frame.pack(padx=10, pady=10, expand=True, fill="both")

de = ttk.DateEntry(frame, bootstyle="secondary", button_icon="cake")

de.pack(fill=X, expand=True)

root.mainloop()

