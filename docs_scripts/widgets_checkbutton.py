import ttkbootstrap as ttk



app = ttk.App(theme="docs-dark")

r1 = ttk.Frame(app, padding=10)
r1.pack(side='top')

r2 = ttk.Frame(app, padding=10)
r2.pack(side='top')

b1 = ttk.CheckButton(r1, text='Unchecked')
b1.pack(side='left', padx=10)
b1.invoke()
b1.invoke()

b2 = ttk.CheckButton(r1, text='Checked')
b2.pack(side='left', padx=10)

b3 = ttk.CheckButton(r1, text='Indeterminate')
b3.pack(side='left', padx=10)

b2.state(['selected'])


b4 = ttk.CheckButton(r2, text='Toggle (unselected)', bootstyle='toggle')
b4.pack(side='left', padx=10)
b4.state(['!selected'])

b4 = ttk.CheckButton(r2, text='Toggle (selected)', bootstyle='toggle')
b4.pack(side='left', padx=10)
b4.state(['selected'])

app.mainloop()