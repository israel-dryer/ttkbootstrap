import tkinter as tk
import ttkbootstrap as ttk
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)

root = tk.Tk()
style = ttk.Style()

frame = ttk.Frame(padding=5)
frame.pack(padx=5, pady=5, fill=tk.X)

top_frame = ttk.Frame(frame)
bot_frame = ttk.Frame(frame)
top_frame.pack(fill=tk.X)
bot_frame.pack(fill=tk.X)

# --- Testing below ---

# # solid button
# for i, color in enumerate(['default', *style.colors]):
#     if i < 5:
#         a = ttk.Button(top_frame, text=color, bootstyle=color, width=10)
#     else:
#         a = ttk.Button(bot_frame, text=color, bootstyle=color, width=10)
#     a.pack(side=tk.LEFT, padx=3, pady=10)
# a = ttk.Button(bot_frame, text='disabled', width=10, state=tk.DISABLED)
# a.pack(side=tk.LEFT, padx=3, pady=10)

# # outline button
# for i, color in enumerate(['default', *style.colors]):
#     if i < 5:
#         a = ttk.Button(top_frame, text=color, bootstyle=color + "outline", width=10)
#     else:
#         a = ttk.Button(bot_frame, text=color, bootstyle=color + "outline", width=10)
#     a.pack(side=tk.LEFT, padx=3, pady=10)
# a = ttk.Button(bot_frame, text='disabled', width=10, bootstyle="outline", state=tk.DISABLED)
# a.pack(side=tk.LEFT, padx=3, pady=10)

# link button
for i, color in enumerate(['default', *style.colors]):
    if i < 5:
        a = ttk.Button(top_frame, text=color, bootstyle=color + "link", width=10)
    else:
        a = ttk.Button(bot_frame, text=color, bootstyle=color + "link", width=10)
    
    a.pack(side=tk.LEFT, padx=3, pady=10)    
a = ttk.Button(bot_frame, text='disabled', width=10, bootstyle="link", state=tk.DISABLED)
a.pack(side=tk.LEFT, padx=3, pady=10)


root.mainloop()