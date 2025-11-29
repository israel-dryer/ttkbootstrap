import ttkbootstrap as ttk
from ttkbootstrap.constants import *

root = ttk.Window()

frame = ttk.Frame(root, padding=10)
frame.pack(padx=10, pady=10)

inner_frame = ttk.Frame(frame, padding=10)
inner_frame.pack(padx=10, pady=10)

de = ttk.DateEntry(inner_frame, show_picker_button=True)


de.pack(fill=X)

root.mainloop()
