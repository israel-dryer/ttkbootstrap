import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap import utility
utility.enable_high_dpi_awareness()

root = tk.Tk()
style = ttk.Style()

frame = ttk.Frame(padding=10)
frame.pack(padx=10, pady=10)

top_frame = ttk.Frame(frame)
top_frame.pack(fill=tk.BOTH)

bot_frame = ttk.Frame(frame)
bot_frame.pack(fill=tk.BOTH)

for i, color in enumerate(['default', *style.colors]):
    if color == 'default':
        text_style = 'default'
    else:
        text_style = color + 'inverse'
    
    if i < 5:
        f = ttk.Frame(top_frame, bootstyle=color)
    else:
        f = ttk.Frame(bot_frame, bootstyle=color)

    f.pack(padx=5, pady=5, side=tk.LEFT)
    ttk.Label(f, text=color, anchor=tk.CENTER, bootstyle=text_style, 
            width=10).pack(fill=tk.Y, expand=tk.YES, padx=15, pady=10)


root.mainloop()