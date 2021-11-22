import tkinter as tk
import ttkbootstrap as ttk
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)

root = tk.Tk()
style = ttk.Style()

frame = ttk.Frame(padding=10)
frame.pack(padx=10, pady=10)

top_frame = ttk.Frame(frame)
top_frame.pack(fill=tk.BOTH)

bot_frame = ttk.Frame(frame)
bot_frame.pack(fill=tk.BOTH)

for i, color in enumerate(['default', *style.colors]):
    
    if i < 5:
        f = ttk.Labelframe(top_frame, text=color, bootstyle=color, width=125, height=40)
    else:
        f = ttk.Labelframe(bot_frame, text=color, bootstyle=color, width=125, height=40)

    f.pack(padx=5, pady=5, side=tk.LEFT)

root.mainloop()