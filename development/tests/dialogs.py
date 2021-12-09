import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.dialogs import Querybox, Messagebox

root = tk.Tk()
Messagebox.ok("Do you want to continue?")
Messagebox.retrycancel("Should I retry?")
Messagebox.okcancel("A message here")
Querybox.get_date()
Querybox.get_font()
