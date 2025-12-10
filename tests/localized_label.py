import ttkbootstrap as ttk

app = ttk.App()

ttk.MessageCatalog.locale("ja")

# disabling localization on this field
ttk.Label(app, text='Cancel', localize=False).pack(padx=20, pady=20)

# allow default localization
ttk.Label(app, text='Cancel').pack(padx=20, pady=20)

# use a specific value format in the current locale
ttk.Label(app, text=12456, value_format='currency').pack(padx=20, pady=20)


app.mainloop()