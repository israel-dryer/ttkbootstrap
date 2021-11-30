import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap import utility
utility.enable_high_dpi_awareness()

root = tk.Tk()
style = ttk.Style()

frame = ttk.Frame(padding=5)
frame.pack(padx=5, pady=5, fill=tk.X)
frame1 = ttk.Frame(frame)
frame2 = ttk.Frame(frame)
frame3 = ttk.Frame(frame)
frame1.pack(fill=tk.X)
frame2.pack(fill=tk.X)
frame3.pack(fill=tk.X)

for i, color in enumerate(['default', *style.colors]):
    if i < 5:
        a = ttk.Spinbox(frame1, bootstyle=color, width=12)
    else:
        a = ttk.Spinbox(frame2, bootstyle=color, width=12)
    a.insert('end', color)
    a.pack(side=tk.LEFT, padx=3, pady=10)

# disabled
a = ttk.Spinbox(frame3, width=12)
a.insert(tk.END, 'disabled')
a.pack(side=tk.LEFT, padx=3, pady=10)
a.configure(state=tk.DISABLED)

# readonly
a = ttk.Spinbox(frame3, width=12)
a.insert(tk.END, 'readonly')
a.pack(side=tk.LEFT, padx=3, pady=10)
a.configure(state='readonly')


root.mainloop()
