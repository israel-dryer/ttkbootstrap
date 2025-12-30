import ttkbootstrap as ttk
from ttkbootstrap import PathEntry

app = ttk.Window()


pe = PathEntry(color='success')
pe.pack(fill='x', padx=20, pady=20)

pe.on_changed(lambda e: print(e.data))


app.mainloop()
