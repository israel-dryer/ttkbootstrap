import ttkbootstrap as ttk
from ttkbootstrap.widgets.dateentry import DateEntry


app = ttk.Window()

de = DateEntry()
de.pack(padx=20, pady=20)
de = DateEntry()
de.pack(padx=20, pady=20)


app.mainloop()