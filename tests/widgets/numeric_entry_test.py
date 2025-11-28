import ttkbootstrap as ttk
from ttkbootstrap.widgets.numericentry import NumericEntry


app = ttk.Window()


ne = NumericEntry(app)
ne.pack(padx=20, pady=20)


app.mainloop()