import tkinter as tk
import ttkbootstrap as ttk
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)

root = tk.Tk()
style = ttk.Style("lumen")

frame = ttk.Frame(padding=5)
frame.pack(padx=5, pady=5, fill=tk.X)

top_frame = ttk.Frame(frame)
bot_frame = ttk.Frame(frame)
top_frame.pack(fill=tk.X)
bot_frame.pack(fill=tk.X)

for i, color in enumerate(['default', *style.colors]):
    if i < 5:
        a = ttk.Entry(top_frame, bootstyle=color)
    else:
        a = ttk.Entry(bot_frame, bootstyle=color)
    a.insert('end', color)
    a.pack(side=tk.LEFT, padx=3, pady=10)

root.mainloop()
