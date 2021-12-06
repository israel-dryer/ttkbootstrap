import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Querybox
from ttkbootstrap import utility

utility.enable_high_dpi_awareness()

root = tk.Tk()
result = Querybox.get_float("How much to charge?", initialvalue=5.4)
print(result)

result = Querybox.get_string("What is your name?")
print(result)


result = Querybox.get_integer("What is your age?")
print(result)
