import ttkbootstrap as ttk

app = ttk.App(theme="docs-light")

r1 = ttk.Frame(app, padding=16)
r1.pack(side='top')

r2 = ttk.Frame(app, padding=16)
r2.pack(side='top')

# entry states
ttk.DateEntry(r1, value='2030-12-31', label='Active', show_message=True, width=16).pack(side='left', padx=10)
ttk.DateEntry(r1, value='2030-12-31', label='Normal', required=True, message='This field is required', show_message=True, width=16).pack(side='left', padx=10)
ttk.DateEntry(r1, value='2030-12-31', state='readonly', label='Readonly', show_message=True, width=16).pack(side='left', padx=10)
ttk.DateEntry(r1, value='2030-12-31', state='disabled', label='Disabled', show_message=True, width=16).pack(side='left', padx=10)


# colors
r3 = ttk.Frame(app, padding=16)
r3.pack(side='top')

for color in ['primary', 'secondary', 'success']:
    te = ttk.DateEntry(r3, value='2030-12-31', bootstyle=color)
    te.pack(side='left', padx=10)

r5 = ttk.Frame(app, padding=16)
r5.pack(side='top')

for color in ['info', 'warning', 'danger']:
    te = ttk.DateEntry(r5, value='2030-12-31', bootstyle=color)
    te.pack(side='left', padx=10)

# prefix example

r2 = ttk.Frame(app, padding=16)
r2.pack(side='top')

birthday = ttk.DateEntry(r2, label="Birthday")
birthday.insert_addon(ttk.Label, position='before', icon='cake-fill')
birthday.pack(side='left', padx=10, anchor='s')


# localization and value format
r7 = ttk.Frame(app, padding=16)
r7.pack(side='top')


ttk.DateEntry(
    r7,
    label="Short Date",
    value="March 14, 1981",
    value_format="shortDate",
).pack(side="left", padx=10)

ttk.DateEntry(
    r7,
    label="Long Date",
    value="1981-03-14",
    value_format="longDate",
).pack(side="left", padx=10)



ttk.DateEntry(app, label='Due Date', value='2025-12-31', message='Pick a date or type one').pack(padx=10, pady=20)




app.mainloop()
