import tkinter as tk
import ttkbootstrap as ttk
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)

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
        f = ttk.Frame(frame1)
        ttk.Label(f, text=color, anchor=tk.CENTER).pack(fill=tk.X)
    else:
        f = ttk.Frame(frame2)
        ttk.Label(f, text=color, anchor=tk.CENTER).pack(fill=tk.X)

    a = ttk.DateEntry(f, bootstyle=color)
    a.pack(fill=tk.X)
    f.pack(side=tk.LEFT, padx=3, pady=10)

# disabled
f = ttk.Frame(frame3)
ttk.Label(f, text='disabled', anchor=tk.CENTER).pack(fill=tk.X)
a = ttk.DateEntry(f)
a.pack(fill=tk.X)
f.pack(side=tk.LEFT, padx=3, pady=10)
a.configure(state=tk.DISABLED)

# readonly
f = ttk.Frame(frame3)
ttk.Label(f, text='readonly', anchor=tk.CENTER).pack(fill=tk.X)
a = ttk.DateEntry(f)
a.pack(fill=tk.X)
f.pack(side=tk.LEFT, padx=3, pady=10)
a.configure(state='readonly')


root.mainloop()
