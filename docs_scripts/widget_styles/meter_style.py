import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap import utility
utility.enable_high_dpi_awareness()

root = tk.Tk()
style = ttk.Style()

frame = ttk.Frame(root, padding=10)
frame.pack(padx=10, pady=10)

top_frame = ttk.Frame(frame)
bot_frame = ttk.Frame(frame)
top_frame.pack(fill=tk.X)
bot_frame.pack()

for i, color in enumerate(['default', *style.colors]):
    if i < 5:
        m = ttk.Meter(
            master=top_frame,
            metersize=150,
            amountused=100,
            subtext=color,
            bootstyle=color,
            interactive=True
        )

    else:
        m = ttk.Meter(
            master=bot_frame,
            metersize=150,
            padding=5,
            amountused=100,
            subtext=color,
            bootstyle=color,
            interactive=True
        )

    m.pack(side=tk.LEFT, padx=3)

    
root.mainloop()