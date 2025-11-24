import ttkbootstrap as ttk

app = ttk.Window()

sf = ttk.ScrollView(app, padding=16, scrollbar_style='rounded')
sf.pack(fill='both', expand=True)

text = ttk.Text(sf)

sf.add(text)

app.mainloop()