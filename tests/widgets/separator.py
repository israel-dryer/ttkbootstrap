import ttkbootstrap as ttk

app = ttk.Window()

colors = ['border', 'primary', 'secondary', 'success', 'info', 'warning', 'danger']

for color in colors:
    ttk.Separator(app, orient="horizontal", bootstyle=color).pack(fill='x', padx=20, pady=20)

app.mainloop()