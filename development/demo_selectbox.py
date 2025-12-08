import ttkbootstrap as ttk
from ttkbootstrap import SelectBox


app = ttk.Window(themename="darkly")

sb = SelectBox(app, "Python", label="Choose your language", items=['Javascript', 'Python', 'C#', 'Ruby', 'Rust'])
sb.pack(padx=10, pady=10)
sb.on_changed(lambda x: print(x))

app.mainloop()
