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
        f = ttk.Frame(top_frame)
    else:
        f = ttk.Frame(bot_frame)

    ttk.Label(f, text=color, width=10, anchor=tk.CENTER).pack(padx=15, pady=15)
    sg = ttk.Sizegrip(f, bootstyle=color)
    sg.pack(fill=tk.BOTH, expand=tk.YES)
    f.pack(side=tk.LEFT, padx=3, pady=10, fill=tk.X)

root.mainloop()



