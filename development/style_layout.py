import tkinter as tk
from tkinter import ttk


root = tk.Tk()

style = ttk.Style()
style.theme_use('default')

print(style.layout('TNotebook'))

root.mainloop()

