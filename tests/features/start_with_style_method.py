import tkinter as tk
import ttkbootstrap as ttk
from random import choice

"""
    Expected Results
    - background is dark
    - only one instance of `BootStyle` or `Tk`
"""

style = ttk.Style(theme="darkly")

root = style.master

root.mainloop()