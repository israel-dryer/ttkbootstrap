import ttkbootstrap as ttk
from ttkbootstrap.widgets.pathentry import PathEntry

app = ttk.Window()


pe = PathEntry()
pe.pack(fill='x', padx=20, pady=20)

pe.on_changed(lambda e: print(e.data))


app.mainloop()