import ttkbootstrap as ttk

app = ttk.Window()

colors = ['primary', 'secondary', 'success', 'info', 'warning', 'danger']

for color in colors:
    b = ttk.Button(app, text=color.title(), bootstyle=color, width=20, icon="apple", compound="left")
    b.pack(padx=20, pady=20)

app.mainloop()