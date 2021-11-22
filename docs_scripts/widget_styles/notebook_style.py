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

width = 150

for i, color in enumerate(['default', *style.colors]):
    
    if i < 5:
        nb = ttk.Notebook(top_frame, bootstyle=color)
        nb.add(ttk.Frame(nb, width=width, height=40), text=color)
        nb.add(ttk.Frame(nb, width=width, height=40), text=color)
    else:
        nb = ttk.Notebook(bot_frame, bootstyle=color)
        nb.add(ttk.Frame(nb, width=width, height=40), text=color)
        nb.add(ttk.Frame(nb, width=width, height=40), text=color)

    nb.pack(padx=5, pady=5, side=tk.LEFT)
    
root.mainloop()