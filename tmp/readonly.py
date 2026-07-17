import ttkbootstrap as ttk

app = ttk.App(theme="darkly")

var = ttk.StringVar(value="Israel")

te = ttk.Entry(state="readonly", textvariable=var).pack(padx=20, pady=20)
te.insert(0, 'hello')

app.mainloop()