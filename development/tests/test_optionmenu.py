import tkinter as tkinter
from tkinter import ttk
from ttkbootstrap import Style

root = tkinter.Tk()
style = Style('superhero')

var = tkinter.Variable()
om = ttk.OptionMenu(root, var, 'default', *style.colors)
om.pack(padx=10, pady=10, fill=tkinter.X)

for i, color in enumerate(style.colors):
    var = tkinter.Variable()
    om = ttk.OptionMenu(root, var, color, *style.colors, bootstyle=color)
    om.pack(padx=10, pady=10, fill=tkinter.X)

root.mainloop()


