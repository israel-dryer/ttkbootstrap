import ttkbootstrap as ttk

app = ttk.App(theme="docs-dark")

r1 = ttk.Frame(app, padding=16)
r1.pack(side='top')

r2 = ttk.Frame(app, padding=16)
r2.pack(side='top')

# entry states
ttk.NumericEntry(r1, value=123456, label='Active', show_message=True).pack(side='left', padx=10)
ttk.NumericEntry(r1, value=123456, label='Normal', required=True, message='This field is required', show_message=True).pack(side='left', padx=10)
ttk.NumericEntry(r2, value=123456, state='readonly', label='Readonly', show_message=True).pack(side='left', padx=10)
ttk.NumericEntry(r2, value=123456, state='disabled', label='Disabled', show_message=True).pack(side='left', padx=10)


# colors
r3 = ttk.Frame(app, padding=16)
r3.pack(side='top')

for color in ['primary', 'secondary', 'success']:
    te = ttk.NumericEntry(r3, value=123456, bootstyle=color)
    te.pack(side='left', padx=10)

r5 = ttk.Frame(app, padding=16)
r5.pack(side='top')

for color in ['info', 'warning', 'danger']:
    te = ttk.NumericEntry(r5, value=123456, bootstyle=color)
    te.pack(side='left', padx=10)

# prefix example

r2 = ttk.Frame(app, padding=16)
r2.pack(side='top')

salary = ttk.NumericEntry(r2, label="Salary")
salary.insert_addon(ttk.Label, position='before', icon='currency-euro')
salary.pack(side='left', padx=10, anchor='s')

size = ttk.NumericEntry(r2, label="Size", show_spin_buttons=False)
size.insert_addon(ttk.Button, position='before', icon='rulers')
size.insert_addon(ttk.Label, position='after', text='cm', font='label[9]')
size.pack(side='left', padx=10, anchor='s')


# localization and value format
r7 = ttk.Frame(app, padding=16)
r7.pack(side='top')


ttk.NumericEntry(
    r7,
    label="Currency",
    value=1234.56,
    value_format="currency",
).pack(side="left", padx=10)

ttk.NumericEntry(
    r7,
    label="Fixed Point",
    value=15422354,
    value_format="fixedPoint",
).pack(side="left", padx=10)

ttk.NumericEntry(
    r7,
    label="Percent",
    value=0.35,
    value_format="percent",
).pack(side="left", padx=10)

app.mainloop()