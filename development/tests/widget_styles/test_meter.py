import tkinter as tk
import ttkbootstrap as ttk
from random import choice

root = tk.Tk()
style = ttk.Style()

def change_style():
    theme = choice(style.theme_names())
    style.theme_use(theme)

ttk.Meter(
    master=root,
    metersize=180,
    padding=20,
    amountused=25,
    metertype='semi',
    subtext='miles per hour',
    interactive=True
).grid(row=0, column=0)

ttk.Meter(
    metersize=180,
    padding=20,
    amountused=1800,
    amounttotal=2600,
    subtext='storage used',
    textright='gb',
    bootstyle='info',
    stripethickness=10,
    interactive=True
).grid(row=0, column=1)

ttk.Meter(
    metersize=180,
    padding=20,
    stripethickness=2,
    amountused=40,
    subtext='project capacity',
    textright='%',
    bootstyle='success',
    interactive=True
).grid(row=1, column=0)

ttk.Meter(
    metersize=180,
    padding=20,
    amounttotal=280,
    arcrange=180,
    arcoffset=-180,
    amountused=75,
    textright='°',
    subtext='heat temperature',
    wedgesize=5,
    bootstyle='danger',
    interactive=True
).grid(row=1, column=1)

btn = ttk.Button(text="Change Theme", command=change_style)
btn.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()