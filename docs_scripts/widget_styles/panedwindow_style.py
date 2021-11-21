import tkinter as tk
import ttkbootstrap as ttk
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)

root = tk.Tk()
root.geometry('800x200')
style = ttk.Style("lumen")

frame = ttk.Frame()
frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=tk.YES)

pw = ttk.Panedwindow(frame)
pw.pack(padx=10, pady=10, fill=tk.BOTH, expand=tk.YES)

f1 = ttk.Frame(pw, bootstyle="primary")
f2 = ttk.Frame(pw, bootstyle="success")

pw.add(f1)
pw.add(f2)

root.mainloop()