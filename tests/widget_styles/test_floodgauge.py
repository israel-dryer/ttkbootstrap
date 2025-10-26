from random import choice

import ttkbootstrap as ttk
from ttkbootstrap import utility
from ttkbootstrap.constants import *

utility.enable_high_dpi_awareness()

root = ttk.Tk()
root.geometry('500x500')
root.title('ttkbootstrap')
style = ttk.Style()


def change_style():
    theme = choice(style.theme_names())
    style.theme_use(theme)


p1 = ttk.Floodgauge(
    bootstyle='info',
    font='helvetica 24 bold',
    mask="Memory Used {}%",
    value=45
)
p1.pack(fill=BOTH, expand=YES, padx=10, pady=10)
p1.start()

btn = ttk.Button(text="Change Theme", command=change_style)
btn.pack(padx=10, pady=10)

p1['value'] = 50
assert p1['value'] == 50
assert p1.configure('value')[-1] == 50

p1['mask'] = None
assert p1.configure('mask')[-1] is None

p1['text'] = "Updating the database"
assert p1['text'] == "Updating the database"

p1['font'] = "arial 18"
assert p1['font'] == 'arial 18'

p1['mask'] = '{}% Complete'
assert p1.configure('mask')[-1] == '{}% Complete'

var = ttk.IntVar(value=30)
p1['variable'] = var
assert p1['value'] == 30
assert (str(var) == p1.cget('variable'))

root.mainloop()
