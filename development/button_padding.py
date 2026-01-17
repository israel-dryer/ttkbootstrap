import ttkbootstrap as ttk


app = ttk.App()

f = ttk.Frame(app, padding=16).pack(fill='both')

btn = ttk.CheckToggle(f, icon='bootstrap', text='Destination', accent='primary', variant='ghost', padding=(64, 4, 16, 4)).pack()

app.mainloop()