import tkinter as tk
from tkinter import ttk


root = tk.Tk()

style = ttk.Style()
style.theme_use('default')

layout = style.layout('TSpinbox')

print(layout)

root.mainloop()

