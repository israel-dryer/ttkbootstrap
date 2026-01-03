import ttkbootstrap as ttk

app = ttk.App()


pe = ttk.PasswordEntry(accent='info')
pe.pack(padx=10, pady=10, fill='x')


app.mainloop()