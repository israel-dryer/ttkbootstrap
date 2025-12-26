import ttkbootstrap as ttk
from ttkbootstrap import TextEntry

app = ttk.Window(theme="dark")


te = TextEntry(app, value="Israel", label="First Name", required=True, message="What shall we call you?")
te.pack(padx=16, pady=(8, 4), fill='x')

te = TextEntry(app, label="First Name", required=True)
te.insert_addon(ttk.Button, 'before', icon='binoculars-fill')
te.pack(fill='x', padx=16, pady=(4, 8))

te.insert('end', 'Something')

ttk.Button(app, text="Disable Text Entry", command=te.disable).pack(padx=16, pady=(4, 8))
ttk.Button(app, text="Readonly Text Entry", command=te.readonly).pack(padx=16, pady=(4, 8))

te['show'] = '*'


app.run()
