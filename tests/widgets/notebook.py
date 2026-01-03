import ttkbootstrap as ttk

app = ttk.Window()

colors = ['default', 'primary', 'secondary', 'success', 'info', 'warning', 'danger']

nb = ttk.Notebook(app)
nb.pack(padx=20, pady=20)

for c in colors:
    nb.insert('end', ttk.Frame(nb, width=100, height=100), text=c)

nb = ttk.Notebook(app, bootstyle="success-underline")
nb.pack(padx=20, pady=20)

for c in colors:
    nb.insert('end', ttk.Frame(nb, width=100, height=100), text=c)

nb = ttk.Notebook(app, bootstyle="danger-underline")
nb.pack(padx=20, pady=20)

for c in colors:
    nb.insert('end', ttk.Frame(nb, width=100, height=100), text=c)

app.mainloop()
