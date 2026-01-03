import ttkbootstrap as ttk
from ttkbootstrap.constants import *

root = ttk.Window()

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
    accent='info',
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
    accent='success',
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
    accent='danger',
    interactive=True
).pack(side='left', padx=10)

ttk.Button(root, text='Change style', command=ttk.toggle_theme).pack(padx=10, pady=10)

root.mainloop()
