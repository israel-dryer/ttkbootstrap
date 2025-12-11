import ttkbootstrap as ttk
from ttkbootstrap import MessageCatalog
from ttkbootstrap import IntlFormatter

app = ttk.App()


MessageCatalog.locale('zh')
formatter = IntlFormatter('zh')

ttk.Label(app, text='Cancel').pack(padx=10, pady=10)

sl = ttk.Scale(app, from_=0, to=1000000)
sl.pack(fill='x')

# Use signal.map to create a new, formatted signal
formatted_signal = sl.signal.map(lambda v: formatter.format(v, 'currency'))

# The Label now uses the new formatted signal
ttk.Label(app, textsignal=formatted_signal).pack(padx=10, pady=10)

ttk.Button(app, text='Ok').pack(padx=10, pady=10)


app.mainloop()