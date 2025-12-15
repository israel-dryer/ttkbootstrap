import ttkbootstrap as ttk

app = ttk.App(theme="docs-dark")

r1 = ttk.Frame(app, padding=16)
r1.pack(side='top')

# entry states
ttk.TextEntry(r1, value='Active', label='Label', show_message=True).pack(side='left', padx=10)
ttk.TextEntry(r1, value='Normal', label='Label', required=True, message='This field is required', show_message=True).pack(side='left', padx=10)
ttk.TextEntry(r1, value='Readonly', state='readonly', label='Label', show_message=True).pack(side='left', padx=10)
ttk.TextEntry(r1, value='Disabled', state='disabled', label='Label', show_message=True).pack(side='left', padx=10)


# prefix example

r2 = ttk.Frame(app, padding=16)
r2.pack(side='top')

email = ttk.TextEntry(r2, label="Email")
email.insert_addon(ttk.Label, position='before', icon='envelope')
email.pack(side='left', padx=10, anchor='s')

def handle_search():
    ...

search = ttk.TextEntry(r2)
search.insert_addon(ttk.Button, position='after', icon='search', command=handle_search)
search.pack(side='left', padx=10, anchor='s')

# localization and value format
r3 = ttk.Frame(app, padding=16)
r3.pack(side='top')

ttk.TextEntry(r3, label="Currency", value=1234.56, value_format="currency").pack(side='left', padx=10)
ttk.TextEntry(r3, label="Short Date", value='March 14, 1981', value_format='shortDate').pack(side='left', padx=10)
ttk.TextEntry(r3, label="Fixed Point", value=15422354, value_format="fixedPoint").pack(side='left', padx=10)


# colors
r4 = ttk.Frame(app, padding=16)
r4.pack(side='top')

for color in ['primary', 'secondary', 'success']:
    te = ttk.TextEntry(r4, value=color, bootstyle=color)
    te.pack(side='left', padx=10)

r5 = ttk.Frame(app, padding=16)
r5.pack(side='top')

for color in ['info', 'warning', 'danger']:
    te = ttk.TextEntry(r5, value=color, bootstyle=color)
    te.pack(side='left', padx=10)

app.mainloop()