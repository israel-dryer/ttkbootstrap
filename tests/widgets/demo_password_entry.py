import ttkbootstrap as ttk

app = ttk.App()


pe = ttk.PasswordEntry(color='info')
pe.pack(padx=10, pady=10, fill='x')


app.mainloop()