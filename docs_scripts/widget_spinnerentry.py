import ttkbootstrap as ttk

app = ttk.App(theme="docs-light")

r1 = ttk.Frame(app, padding=16)
r1.pack(side='top')

r2 = ttk.Frame(app, padding=16)
r2.pack(side='top')

# entry states
ttk.SpinnerEntry(r1, value='Active', label='Label', show_message=True).pack(side='left', padx=10)
ttk.SpinnerEntry(r1, value='Normal', label='Label', required=True, message='This field is required', show_message=True).pack(side='left', padx=10)
ttk.SpinnerEntry(r1, value='Readonly', state='readonly', label='Label', show_message=True).pack(side='left', padx=10)
ttk.SpinnerEntry(r1, value='Disabled', state='disabled', label='Label', show_message=True).pack(side='left', padx=10)


# colors
r3 = ttk.Frame(app, padding=16)
r3.pack(side='top')

for color in ['primary', 'secondary', 'success']:
    te = ttk.SpinnerEntry(r3, value=123456, color=color)
    te.pack(side='left', padx=10)

r5 = ttk.Frame(app, padding=16)
r5.pack(side='top')

for color in ['info', 'warning', 'danger']:
    te = ttk.SpinnerEntry(r5, value=123456, color=color)
    te.pack(side='left', padx=10)

# prefix example

r2 = ttk.Frame(app, padding=16)
r2.pack(side='top')

salary = ttk.SpinnerEntry(r2, label="Salary")
salary.insert_addon(ttk.Label, position='before', icon='currency-euro')
salary.pack(side='left', padx=10, anchor='s')

size = ttk.SpinnerEntry(r2, label="Size", values=['Small', 'Med', 'Large'], value='Small')
size.insert_addon(ttk.Button, position='before', icon='rulers')
size.pack(side='left', padx=10, anchor='s')


# localization and value format
r7 = ttk.Frame(app, padding=16)
r7.pack(side='top')


ttk.SpinnerEntry(
    r7,
    label="Currency",
    value=9.99,
    increment=0.01,
    value_format="currency",
).pack(side="left", padx=10)

ttk.SpinnerEntry(
    r7,
    label="Fixed Point",
    value=1500,
    increment=10,
    value_format="fixedPoint",
).pack(side="left", padx=10)

ttk.SpinnerEntry(
    r7,
    label="Percent",
    value=0.25,
    increment=0.05,
    value_format="percent",
).pack(side="left", padx=10)

app.mainloop()