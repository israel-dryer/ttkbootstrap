import ttkbootstrap as ttk
from ttkbootstrap import NumericEntry


app = ttk.Window()


ne = NumericEntry(app, accent='danger')
ne.pack(padx=20, pady=20)


app.mainloop()
