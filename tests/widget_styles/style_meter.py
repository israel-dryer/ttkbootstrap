import ttkbootstrap as ttk
from ttkbootstrap import use_style
from ttkbootstrap.constants import *

root = ttk.Window()
style = use_style()


def change_style():
    if style.theme_use() == 'dark':
        style.theme_use('light')
    else:
        style.theme_use('dark')


frame = ttk.Frame(padding=10)
frame.pack(padx=10, pady=10)

m = ttk.Meter(
    master=frame,
    size=180,
    padding=5,
    value=25,
    value_format="{:0.1f}",
    meter_type='semi',
    subtitle='miles per hour',
    interactive=True
)
m.pack(side=LEFT, padx=10)
m.on_changed(print)

ttk.Meter(
    master=frame,
    size=180,
    padding=5,
    value=1800,
    maxvalue=2600,
    subtitle='storage used',
    value_suffix='gb',
    bootstyle='info',
    segment_width=10,
    interactive=True
).pack(side=LEFT, padx=10)

ttk.Meter(
    master=frame,
    size=180,
    padding=5,
    segment_width=2,
    value=40,
    subtitle='project capacity',
    value_suffix='%',
    bootstyle='success',
    interactive=True
).pack(side=LEFT, padx=10)

ttk.Meter(
    master=frame,
    size=180,
    padding=5,
    value=75,
    maxvalue=280,
    arc_range=180,
    arc_offset=-180,
    value_suffix='°',
    subtitle='heat temperature',
    indicator_width=2,
    bootstyle='danger',
    interactive=True
).pack(side='left', padx=10)

ttk.Button(root, text='Change style', command=change_style).pack(padx=10, pady=10)

root.mainloop()
