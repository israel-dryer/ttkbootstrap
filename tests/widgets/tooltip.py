import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.tooltip import ToolTip

app = ttk.Window(size=(400, 100))

b1 = ttk.Button(app, text="default tooltip")
b1.pack(side=LEFT, padx=10, pady=10, fill=X, expand=YES)
ToolTip(
    b1,
    text="This is the default tooltip. This yellow background and black foreground will be applied by default.",
)

b2 = ttk.Button(app, text="styled tooltip")
b2.pack(side=LEFT, padx=10, pady=10, fill=X, expand=YES)
ToolTip(
    b2,
    text="This is a styled tooltip. You can change this style by using the `bootstyle` parameter with label style keywords.",
    bootstyle="danger-inverse",
)

app.mainloop()
