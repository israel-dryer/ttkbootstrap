import ttkbootstrap as ttk



app = ttk.App()

f1 = ttk.Frame(width=100, height=100)
f1.pack()

f2 = ttk.Frame(width=200, height=200, bootstyle='danger')
f2.pack(fill='both', expand=True)

b1 = ttk.Button(f2, text='Test')
b1.pack()

#f2.configure_style_options(surface_color='primary')
f2.configure(bootstyle='primary')

app.mainloop()