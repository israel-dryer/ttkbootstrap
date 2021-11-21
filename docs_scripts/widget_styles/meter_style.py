import tkinter as tk
import ttkbootstrap as ttk
from random import choice
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)

root = tk.Tk()
style = ttk.Style()

def change_style():
    theme = choice(style.theme_names())
    style.theme_use(theme)

frame = ttk.Frame(root, padding=10)
frame.pack(padx=10, pady=10)

ttk.Meter(
    master=frame,
    metersize=180,
    padding=5,
    amountused=25,
    metertype='semi',
    subtext='miles per hour',
    interactive=True
).grid(row=0, column=0)

ttk.Meter(
    master=frame,
    metersize=180,
    padding=5,
    amountused=1800,
    amounttotal=2600,
    subtext='storage used',
    textright='gb',
    bootstyle='info',
    stripethickness=10,
    interactive=True
).grid(row=0, column=1)

ttk.Meter(
    master=frame,
    metersize=180,
    padding=5,
    stripethickness=2,
    amountused=40,
    subtext='project capacity',
    textright='%',
    bootstyle='success',
    interactive=True
).grid(row=0, column=2)

ttk.Meter(
    master=frame,
    metersize=180,
    padding=5,
    amounttotal=280,
    arcrange=180,
    arcoffset=-180,
    amountused=75,
    textright='°',
    subtext='heat temperature',
    wedgesize=5,
    bootstyle='danger',
    interactive=True
).grid(row=0, column=3)

# btn = ttk.Button(text="Change Theme", command=change_style)
# btn.pack()

root.mainloop()