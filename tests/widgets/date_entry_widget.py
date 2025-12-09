import ttkbootstrap as ttk
from ttkbootstrap.constants import *

root = ttk.Window(theme="dark")

frame = ttk.Frame(root, padding=10)
frame.pack(padx=10, pady=10)

inner_frame = ttk.Frame(frame, padding=10)
inner_frame.pack(padx=10, pady=10)

de = ttk.DateEntry(inner_frame, label="Registration Date", show_picker_button=True, value_format="longDate", message="Enter the registration date")


de.pack(fill=X)

root.mainloop()
