import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap import utility
utility.enable_high_dpi_awareness()

root = tk.Tk()
style = ttk.Style()


frame = ttk.Frame(padding=10)
frame.pack(padx=10, pady=10, expand=tk.YES, fill=tk.BOTH)

top_frame = ttk.Frame(frame)
top_frame.pack(fill=tk.BOTH, expand=tk.YES)

bot_frame = ttk.Frame(frame)
bot_frame.pack(fill=tk.BOTH, expand=tk.YES)

for i, color in enumerate(['default', *style.colors]):
    if i < 5:
        p = ttk.Floodgauge(
            master=top_frame,
            bootstyle=color,
            text=color,
            value=65,
        )
    else:
        p = ttk.Floodgauge(
            master=bot_frame,
            bootstyle=color,
            text=color,
            value=65,
        )
    p.pack(padx=5, pady=5, fill=tk.BOTH, side=tk.LEFT)
    p.start()

root.mainloop()
