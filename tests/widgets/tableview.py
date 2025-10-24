import csv
from pathlib import Path

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import Tableview

app = ttk.Window(themename='flatly')
colors = app.style.colors

p = Path(__file__).parent / "Sample1000.csv"
with open(p, encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader)
    rowdata = list(reader)

# column configuration options
# text, image, command, anchor, width, minwidth, maxwidth, stretch
coldata = [
    {"text": "SerialNumber", "stretch": False},
    "CompanyName",
    "Employee",
    "Description",
    {"text": "Leave", "stretch": False},
]

dt = Tableview(
    master=app,
    paginated=True,
    disable_right_click=True,
    searchable=True,
    bootstyle=PRIMARY,
    stripecolor=(None, None),
    autofit=False
)
dt.pack(fill=BOTH, expand=YES, padx=5, pady=5)

dt.build_table_data(coldata, rowdata)
# dt.delete_columns(indices=[2, 3])

# modify the contents of a single cell
row = dt.get_row(0)
row.values[2] = "Israel"
row.refresh()

# modify an entire row
row = dt.get_row(1)
row.values = ['123456', 'My Company', 'Israel', 'Something here', 45]

dt.search_table_data(2, "Leave")

app.mainloop()
