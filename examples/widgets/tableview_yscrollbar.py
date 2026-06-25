"""Demo: Tableview yscrollbar visibility with many columns (issue #1042).

Run this script to verify the vertical scrollbar is visible even with
50 columns. Before the fix, pack() would compress it to ~1px.
"""

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.widgets.tableview import Tableview

app = ttk.Window(themename="flatly", title="Issue #1042 - yscrollbar demo")
app.geometry("900x400")

# 50 columns to trigger the original bug
num_cols = 50
coldata = [f"Col {i}" for i in range(num_cols)]
rowdata = [
    tuple(f"R{r}C{c}" for c in range(num_cols))
    for r in range(100)
]

dt = Tableview(
    master=app,
    coldata=coldata,
    rowdata=rowdata,
    yscrollbar=True,
    paginated=False,
    bootstyle=PRIMARY,
)
dt.pack(fill=BOTH, expand=YES, padx=5, pady=5)

app.mainloop()