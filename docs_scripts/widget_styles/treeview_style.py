import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap import utility
utility.enable_high_dpi_awareness()

root = tk.Tk()
style = ttk.Style()

frame = ttk.Frame(padding=10)
frame.pack(padx=10, pady=10)

top_frame = ttk.Frame(frame)
top_frame.pack(fill=tk.BOTH, expand=tk.YES)

bot_frame = ttk.Frame(frame)
bot_frame.pack(fill=tk.BOTH, expand=tk.YES)

for i, color in enumerate(['default', *style.colors]):
    if color == 'default':
        text_style = 'default'
    else:
        text_style = color + 'inverse'
    
    if i < 5:
        tv = ttk.Treeview(
            master=top_frame, 
            bootstyle=color,
            height=5,
        )
    else:
        tv = ttk.Treeview(
            master=bot_frame, 
            bootstyle=color,
            height=5,
        )

    tv.column('#0')
    tv.heading('#0', text=color, anchor=tk.W)

    iid = tv.insert('', tk.END, text='parent 1')
    tv.insert(iid, tk.END, text='child 1')
    tv.insert(iid, tk.END, text='child 2')
    tv.insert(iid, tk.END, text='child 2')
    tv.insert('', tk.END, text='parent 2')
    tv.pack(padx=5, pady=5)
    tv.selection_add(iid)

    tv.pack(padx=5, pady=5, side=tk.LEFT)

root.mainloop()