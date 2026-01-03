import ttkbootstrap as ttk

app = ttk.Window()

sf = ttk.ScrollView(app, padding=16, scrollbar_variant='rounded')
sf.pack(fill='both', expand=True)

text = ttk.Text(sf)

text.insert('end', 'Hello world')

sf.add(text)

app.mainloop()