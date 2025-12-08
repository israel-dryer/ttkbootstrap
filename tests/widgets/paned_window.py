import ttkbootstrap as ttk

app = ttk.Window()
app.style.theme_use('dark')

pw1 = ttk.PanedWindow(app, orient='horizontal', bootstyle="primary")
pw1.pack(fill='both', expand=True, padx=20, pady=20)

pw1.add(ttk.Frame(pw1, width=100, height=100))
pw1.add(ttk.Frame(pw1, width=100, height=100))


pw2 = ttk.PanedWindow(app, orient='horizontal')
pw2.pack(fill='both', expand=True, padx=20, pady=20)

pw2.add(ttk.Frame(pw2, width=100, height=100))
pw2.add(ttk.Frame(pw2, width=100, height=100))

app.update_idletasks()

app.mainloop()