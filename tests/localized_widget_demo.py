import ttkbootstrap as ttk

app = ttk.App(
    title="Localization Demo",
    settings=ttk.AppSettings(locale="ja")
)

var = ttk.DoubleVar(value=100)

sl = ttk.Scale(app, variable=var, from_=0, to=1000000)
sl.pack(fill='x')

# Label uses a shared variable
ttk.Label(app, textvariable=var, value_format='thousands').pack(padx=10, pady=10)

# Label uses the scale variable
ttk.Label(app, textvariable=sl.variable, value_format='fixedPoint').pack(padx=10, pady=10)

# Label uses the scale signal
ttk.Label(app, textvariable=sl.signal, value_format='currency').pack(padx=10, pady=10)

app.mainloop()