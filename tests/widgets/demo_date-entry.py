import ttkbootstrap as ttk
from ttkbootstrap import DateEntry


app = ttk.App()

de = DateEntry()
de.pack(padx=20, pady=20)
de = DateEntry(accent='info')
de.pack(padx=20, pady=20)


app.mainloop()
