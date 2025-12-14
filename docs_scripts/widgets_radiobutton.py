import ttkbootstrap as ttk

app = ttk.App(theme="docs-light")

r1 = ttk.Frame(app, padding=10)
r1.pack(side='top', fill='x')

r2 = ttk.Frame(app, padding=10)
r2.pack(side='top', fill='x')

sig = ttk.Signal(0)

ttk.RadioButton(r1, signal=sig, text="Selected", value=0).pack(side='left', padx=10)
ttk.RadioButton(r1, signal=sig, text="Unselected", value=1).pack(side='left', padx=10)
ttk.RadioButton(r1, signal=sig, text="Disabled", value=3, state='disabled').pack(side='left', padx=10)


ttk.RadioButton(r2, signal=sig, text="Primary", value=0).pack(side='left', padx=10)
ttk.RadioButton(r2, signal=sig, text="Secondary", value=0, bootstyle="secondary").pack(side='left', padx=10)
ttk.RadioButton(r2, signal=sig, text="Success", value=0, bootstyle="success").pack(side='left', padx=10)
ttk.RadioButton(r2, signal=sig, text="Info", value=0, bootstyle="info").pack(side='left', padx=10)
ttk.RadioButton(r2, signal=sig, text="Warning", value=0, bootstyle="warning").pack(side='left', padx=10)
ttk.RadioButton(r2, signal=sig, text="Danger", value=0, bootstyle="danger").pack(side='left', padx=10)

app.mainloop()