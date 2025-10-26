from random import choice

import ttkbootstrap as ttk
from ttkbootstrap import Tk, utility
from ttkbootstrap.constants import *

utility.enable_high_dpi_awareness()

root = Tk()
style = ttk.Style()


def change_style():
    theme = choice(style.theme_names())
    style.theme_use(theme)


frame = ttk.Frame(padding=10)
frame.pack(padx=10, pady=10)

ttk.Meter(
    master=frame,
    metersize=180,
    padding=5,
    amountused=25,
    amountformat="{:0.1f}",
    metertype='semi',

    subtext='miles per hour',
    interactive=True
).pack(side=LEFT)

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
).pack(side=LEFT)

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
).pack(side=LEFT)

ttk.Meter(
    master=frame,
    metersize=180,
    padding=5,
    amounttotal=280,
    meterthickness=50,
    arcrange=180,
    arcoffset=-180,
    amountused=75,
    textright='°',
    subtext='heat temperature',
    wedgesize=2,
    bootstyle='danger',
    interactive=True
).pack(side='left')

meter = ttk.Meter(
    metersize=100,
    padding=10,
    amountused=10,
    metertype="semi",
    subtext="Miles per hour",
    interactive=True,
    amounttotal=100
)
meter.step(-50)
meter.pack(side=LEFT)
# btn = ttk.Button(text="Change Theme", command=change_style)
# btn.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()
