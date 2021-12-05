import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap import dialogs

root = tk.Tk()
dialogs.ask_question("Do you want to continue?")
dialogs.ask_retrycancel("Should I retry?")
dialogs.ask_okcancel("A message here")
