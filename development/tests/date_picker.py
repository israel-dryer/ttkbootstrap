import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.dialogs.calendar import ask_date

root = tk.Tk()

def get_the_age(parent=None):
    date = ask_date(parent, bootstyle='success')
    print(date)
    

btn = ttk.Button(root, text="Hello")
btn.configure(command=lambda b=btn: get_the_age(b))
btn.pack(padx=10, pady=10)

root.mainloop()
