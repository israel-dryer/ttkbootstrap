import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.style import utility

root = tk.Tk()
utility.enable_high_dpi_awareness(root)
style = ttk.Style()

# # normal label
# frame = ttk.Frame(padding=5)
# frame.pack(padx=5, pady=5, fill=tk.X)

# top_frame = ttk.Frame(frame)
# bot_frame = ttk.Frame(frame)
# top_frame.pack(fill=tk.X)
# bot_frame.pack(fill=tk.X)

# for i, color in enumerate(['default', *style.colors]):
#     if i < 5:
#         a = ttk.Label(top_frame, text=color, bootstyle=color, width=10)
#     else:
#         a = ttk.Label(bot_frame, text=color, bootstyle=color, width=10)
    
#     a.pack(side=tk.LEFT, padx=3, pady=10)    


# inverse label
frame = ttk.Frame(padding=5)
frame.pack(padx=5, pady=5, fill=tk.X)

top_frame = ttk.Frame(frame)
bot_frame = ttk.Frame(frame)
top_frame.pack(fill=tk.X)
bot_frame.pack(fill=tk.X)

for i, color in enumerate(['default', *style.colors]):
    if i < 5:
        a = ttk.Label(top_frame, text=color, bootstyle=color + "inverse", width=10)
    else:
        a = ttk.Label(bot_frame, text=color, bootstyle=color + "inverse", width=10)
    
    a.pack(side=tk.LEFT, padx=3, pady=10)    

root.mainloop()