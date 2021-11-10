import tkinter as tk
import ttkbootstrap as ttk


root = tk.Tk()
style = ttk.Style('superhero')

var = tk.Variable()
om = ttk.OptionMenu(root, var, 'default', *style.colors)
om.pack(padx=10, pady=10, fill=tk.X)

for i, color in enumerate(style.colors):
    var = tk.Variable()
    om = ttk.OptionMenu(root, var, color, *style.colors, bootstyle=color)
    om.pack(padx=10, pady=10, fill=tk.X)

root.mainloop()


