import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from pathlib import Path
import csv
from ttkbootstrap.utility import scale_size

app = ttk.Window(themename='sandstone')
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

# tv = ttk.Treeview(bootstyle=PRIMARY, columns = [0, 1, 2, 3, 4], show=HEADINGS)
# colnames = ['SerialNumber', 'CompanyName', 'Employee', 'Description', 'Leave']
# for i, col in enumerate(colnames):
#     tv.heading(i, text=col, anchor=W)
#     tv.column(i, stretch=False)

# for row in rowdata:
#     tv.insert('', END, values=row)

# tv.pack(fill=BOTH, expand=YES, padx=10, pady=(10, 0))
# sb = ttk.Scrollbar(orient=HORIZONTAL, command=tv.xview)
# tv.configure(xscrollcommand=sb.set)
# sb.pack(fill=X, padx=10, pady=(0, 10))

# # calculate the best size for each column
# from tkinter import font
# f = font.nametofont('TkDefaultFont')
# widths = []
# for col in colnames:
#     widths.append(f.measure(col) + scale_size(tv, 10))

# for row in rowdata:
#     for i, col in enumerate(row):
#         measure = f.measure(col)
#         if measure > widths[i]:
#             widths[i] = measure

# for i, width in enumerate(widths):
#     tv.column(i, width=width)

dt = ttk.Tableview(
    master=app,
    coldata=coldata,
    rowdata=rowdata,
    paginated=True,
    searchable=True,
    bootstyle=DARK,
    stripecolor=('#eee', None),
    autofit=False
)
dt.pack(fill=BOTH, expand=YES, padx=5, pady=5)
print(app.style.colors.inputbg)

app.mainloop()
