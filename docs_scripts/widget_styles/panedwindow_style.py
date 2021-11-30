import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap import utility
utility.enable_high_dpi_awareness()

root = tk.Tk()
style = ttk.Style()

frame = ttk.Frame(padding=5)
frame.pack(padx=5, pady=5, fill=tk.X)

top_frame = ttk.Frame(frame)
bot_frame = ttk.Frame(frame)

top_frame.pack(fill=tk.X)
bot_frame.pack(fill=tk.X)

for i, color in enumerate(['default', *style.colors]):
    if i < 5:
        pw = ttk.Panedwindow(top_frame, bootstyle=color)
    else:
        pw = ttk.Panedwindow(bot_frame, bootstyle=color)

    f = ttk.Frame(pw)
    f.pack(fill=tk.BOTH, expand=tk.YES)
    ttk.Label(f, text=color).pack(side=tk.TOP)
    pw.add(f)
    pw.add(ttk.Frame(width=120, height=30))
    pw.pack(side=tk.LEFT, padx=3, pady=10, fill=tk.X)

root.mainloop()
