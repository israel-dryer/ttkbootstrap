import csv
import time
from pathlib import Path

import ttkbootstrap as ttk
from ttkbootstrap.widgets.datagrid import DataGrid

p = Path(__file__).parent / "people-1000.csv"
with open(p, encoding="utf-8") as f:
    reader = csv.DictReader(f)
    rows = [
        {
            "Index": row.get("Index"),
            "UserId": row.get("User Id"),
            "FirstName": row.get("First Name"),
            "LastName": row.get("Last Name"),
            "Sex": row.get("Sex"),
            "Email": row.get("Email"),
            "Phone": row.get("Phone"),
            "BirthDate": row.get("Date of birth"),
            "JobTitle": row.get("Job Title"),
        }
        for row in reader
    ]

# Keep the sample size modest for demo purposes
print(f"Preparing {len(rows)} records")

app = ttk.Window(themename="dark", size=(1200, 800))

columns = [
    {"text": "Index", "key": "Index", "anchor": "e"},
    {"text": "UserId", "key": "UserId"},
    {"text": "First", "key": "FirstName"},
    {"text": "Last", "key": "LastName"},
    {"text": "Sex", "key": "Sex", "width": 80},
    {"text": "Email", "key": "Email", "width": 200},
    {"text": "Phone", "key": "Phone", "width": 140},
    {"text": "BirthDate", "key": "BirthDate", "width": 110},
    {"text": "JobTitle", "key": "JobTitle", "width": 200},
]

start = time.perf_counter()
grid = DataGrid(
    app,
    columns=columns,
    rows=rows,
    # show_xscroll=False,
    # page_size=200,
    # virtual_scroll=False,
    # allow_column_hiding=False,
    # show_table_status=False,
    # show_context_menus="headers",
)
grid.pack(fill="both", expand=True, padx=5, pady=5)
elapsed = time.perf_counter() - start
print(f"DataGrid build time: {elapsed:.3f}s for {len(rows)} rows")

app.mainloop()
