import ttkbootstrap as ttk

window = ttk.Window(size=(800, 800))

meter = ttk.Meter(amountmin=-100, amounttotal=100, amountused=-25, interactive=True)
meter.pack(fill='both')
window.mainloop()
