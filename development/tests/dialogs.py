import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.dialogs import message

root = tk.Tk()
message.ok("Do you want to continue?")
message.retrycancel("Should I retry?")
message.okcancel("A message here")
