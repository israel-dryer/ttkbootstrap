import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from pathlib import Path
import csv
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.utility import scale_size

app = ttk.Window(themename='darkly')
colors = app.style.colors

p = Path(".") / "development/new_widgets/Sample1000.csv"
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
#    coldata=coldata,
#    rowdata=rowdata,
    paginated=True,
    searchable=True,
    bootstyle=PRIMARY,
    stripecolor=(None, None),
    autofit=False
)
dt.pack(fill=BOTH, expand=YES, padx=5, pady=5)

dt.build_table_data(coldata, rowdata)
#dt.delete_columns(indices=[2, 3])

app.mainloop()
