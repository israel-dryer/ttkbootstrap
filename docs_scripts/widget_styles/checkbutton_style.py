import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap import utility
utility.enable_high_dpi_awareness()

root = tk.Tk()
style = ttk.Style(theme='darkly')

frame = ttk.Frame(padding=5)
frame.pack(padx=5, pady=5, fill=tk.X)

top_frame = ttk.Frame(frame)
bot_frame = ttk.Frame(frame)
top_frame.pack(fill=tk.X)
bot_frame.pack(fill=tk.X)

# --- Testing below ---

# checkbutton
for i, color in enumerate(['default', *style.colors]):
    if i < 5:
        a = ttk.Checkbutton(top_frame, text=color, bootstyle=color, width=12)
    else:
        a = ttk.Checkbutton(bot_frame, text=color, bootstyle=color, width=12)
    
    a.pack(side=tk.LEFT, padx=3, pady=10)
    a.invoke()
a = ttk.Checkbutton(bot_frame, text='disabled', width=12, state=tk.DISABLED)
a.pack(side=tk.LEFT, padx=3, pady=10)

# solid toolbutton
for i, color in enumerate(['default', *style.colors]):
    if i < 5:
        a = ttk.Checkbutton(top_frame, text=color, bootstyle=color + 'toolbutton', width=12)
    else:
        a = ttk.Checkbutton(bot_frame, text=color, bootstyle=color + 'toolbutton', width=12)
    
    a.pack(side=tk.LEFT, padx=3, pady=10)
    a.invoke()
a = ttk.Checkbutton(bot_frame, text='disabled', width=12, bootstyle="toolbutton", state=tk.DISABLED)
a.pack(side=tk.LEFT, padx=3, pady=10)

# outline toolbutton
for i, color in enumerate(['default', *style.colors]):
    if i < 5:
        a = ttk.Checkbutton(top_frame, text=color, bootstyle=color + 'outline-toolbutton', width=12)
    else:
        a = ttk.Checkbutton(bot_frame, text=color, bootstyle=color + 'outline-toolbutton', width=12)
    
    a.pack(side=tk.LEFT, padx=3, pady=10)
    a.invoke()
a = ttk.Checkbutton(bot_frame, text='disabled', width=12, bootstyle="outline-toolbutton", state=tk.DISABLED)
a.pack(side=tk.LEFT, padx=3, pady=10)

# round toggles
for i, color in enumerate(['default', *style.colors]):
    if i < 5:
        a = ttk.Checkbutton(top_frame, text=color, bootstyle=color + 'round-toggle', width=12)
    else:
        a = ttk.Checkbutton(bot_frame, text=color, bootstyle=color + 'round-toggle', width=12)
    a.pack(side=tk.LEFT, padx=3, pady=10)
    a.invoke()
a = ttk.Checkbutton(bot_frame, text='disabled', width=12, bootstyle="round-toggle", state=tk.DISABLED)
a.pack(side=tk.LEFT, padx=3, pady=10)

# square toggle
for i, color in enumerate(['default', *style.colors]):
    if i < 5:
        a = ttk.Checkbutton(top_frame, text=color, bootstyle=color + 'square-toggle', width=12)
    else:
        a = ttk.Checkbutton(bot_frame, text=color, bootstyle=color + 'square-toggle', width=12)
    a.pack(side=tk.LEFT, padx=3, pady=10)
    a.invoke()
a = ttk.Checkbutton(bot_frame, text='disabled', width=12, bootstyle="square-toggle", state=tk.DISABLED)
a.pack(side=tk.LEFT, padx=3, pady=10)

root.mainloop()