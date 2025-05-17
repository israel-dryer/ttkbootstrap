import ttkbootstrap as ttk

def run_visual_test():
    app = ttk.Window(title="Meter Visual Test", themename="flatly")

    meter1 = ttk.Meter(app, metersize=150, amountused=65, subtext="CPU Usage", color="primary")
    meter1.pack(padx=10, pady=10)

    meter2 = ttk.Meter(app, metersize=150, amountused=25, metertype="semi", subtext="Load", color="danger", stripethickness=3)
    meter2.pack(padx=10, pady=10)

    meter3 = ttk.Meter(app, metersize=150, amountused=85, subtext="Battery", color="success", wedgesize=10)
    meter3.pack(padx=10, pady=10)

    meter4 = ttk.Meter(app, metersize=150, amountused=40, subtext="Interactive", interactive=True, color="info")
    meter4.pack(padx=10, pady=10)

    app.mainloop()

if __name__ == "__main__":
    run_visual_test()
