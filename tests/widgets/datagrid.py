import csv
import time
from pathlib import Path

import ttkbootstrap as ttk
from ttkbootstrap.widgets.datagrid import DataGrid

p = Path(__file__).parent / "Sample1000.csv"
with open(p, encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader)
    row_data = list(reader)

# Upscale the dataset for a quick performance sanity check
repeat = 2003
rows = row_data * repeat
print(f"Preparing {len(rows)} records")

app = ttk.Window(themename="dark", size=(1200, 800))

columns = [
    {"text": "EmployeeNumber", "key": "EmployeeNumber", "anchor": "w"},
    {"text": "CompanyName", "key": "CompanyName"},
    {"text": "Employee", "key": "Employee"},
    {"text": "Description", "key": "Description"},
    {"text": "YearsOfService", "key": "YearsOfService"},
]

start = time.perf_counter()
grid = DataGrid(
    app,
    columns=columns,
    rows=rows,
    page_size=200,
    show_yscroll=False,
    allow_export=True,
    export_options=['page', 'selection'],
    allow_edit=True,
)
grid.pack(fill="both", expand=True, padx=5, pady=5)
elapsed = time.perf_counter() - start
print(f"DataGrid build time: {elapsed:.3f}s for {len(rows)} rows")

app.mainloop()
