import ttkbootstrap as ttk
from ttkbootstrap.constants import *

root = ttk.Window("FloodGauge Demo")
style = ttk.Style()


p1 = ttk.FloodGauge(
    accent="danger",
    mask="Memory Used {}%",
    value=45
)
p1.pack(fill=BOTH, expand=YES, padx=10, pady=10)
p1.start()

btn = ttk.Button(text="Change Theme", accent="danger", command=ttk.toggle_theme)
btn.pack(padx=10, pady=10)

root.mainloop()
