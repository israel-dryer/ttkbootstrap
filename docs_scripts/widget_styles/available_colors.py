import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.style import utility

root = tk.Tk()
utility.enable_high_dpi_awareness(root)
style = ttk.Style()

frame = ttk.Frame(root, padding=10)
frame.pack(fill=tk.BOTH, expand=tk.YES)
row_one = ttk.Frame(frame)
row_two = ttk.Frame(frame)

for i, color in enumerate(style.colors):
    if i < 4:
        lbl = ttk.Button(row_one, text=color, bootstyle=color, width=10)
    else:
        lbl = ttk.Button(row_two, text=color, bootstyle=color, width=10)

    lbl.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)

row_one.pack(fill=tk.BOTH, expand=tk.YES, pady=(5, 0), padx=5)
row_two.pack(fill=tk.BOTH, expand=tk.YES, pady=(0, 5), padx=5)

root.mainloop()



