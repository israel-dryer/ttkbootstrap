import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.dialogs import QueryBox
from ttkbootstrap import utility

utility.enable_high_dpi_awareness()

root = tk.Tk()
result = QueryBox.get_float("How much to charge?", value=5.4)
print(result)

result = QueryBox.get_string("What is your name?")
print(result)


result = QueryBox.get_integer("What is your age?")
print(result)
