import ttkbootstrap as ttk


app = ttk.Window()

nb = ttk.Notebook(app)
f1 = nb.add_frame("Options", key="options", frame_options={"width": 300, "height": 300, "bootstyle": "danger"}, sticky="nsew")
ttk.Button(f1, text="On Frame 1", bootstyle="warning").pack(padx=20, pady=20)

f2 = nb.add_frame("Configuration", key="configuration", sticky="nsew")
ttk.Button(f2, text="On Frame 2", command=lambda: nb.select("options")).pack(padx=20, pady=20)

nb.pack(fill='both', expand=True)

nb.on_tab_changed(print)

app.mainloop()