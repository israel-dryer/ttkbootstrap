import tkinter as tk
from tkinter import ttk

root = tk.Tk()

style = ttk.Style()
style.theme_use('clam')

cb = ttk.Checkbutton(root, text="Toolbutton", style='Toolbutton')
cb.pack()

style.configure('Toolbutton', relief='flat')
style.map('Toolbutton', background=[('selected', 'red')])
print(style.configure('Toolbutton'))


root.mainloop()