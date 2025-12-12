import ttkbootstrap as ttk

app = ttk.App()

ttk.MessageCatalog.locale("zh")

lf = ttk.LabelFrame(app, text='Close', padding=8)
lf.pack(padx=20, pady=20)

# disabling localization on this field
ttk.Label(lf, text='Cancel', localize=False).pack(padx=20, pady=20)

# allow default localization
ttk.Label(lf, text='Cancel').pack(padx=20, pady=20)

# use a specific value format in the current locale
ttk.Label(lf, text=12456, value_format='currency').pack(padx=20, pady=20)

ttk.Button(lf, text='Submit', command=lambda: ttk.MessageCatalog.locale('fr')).pack(padx=20, pady=20)

ttk.CheckButton(lf, text='Close').pack(padx=20, pady=20)

ttk.TextEntry(lf, label="Submit").pack(padx=20, pady=20)

ttk.NumericEntry(lf, label="Cancel", value_format="currency").pack(padx=20, pady=20)

ttk.DateEntry(lf, label="Birthday", value="March 14, 1981").pack(padx=20, pady=20)



app.mainloop()
