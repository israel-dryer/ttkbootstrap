import csv
import time
from pathlib import Path

import ttkbootstrap as ttk

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

app = ttk.App(
    theme="dark",
    size=(1200, 800),
    settings=ttk.AppSettings(locale='ja')
)

columns = [
    {"text": "Index", "key": "Index", "anchor": "e"},
    {"text": "UserId", "key": "UserId"},
    {"text": "First", "key": "FirstName"},
    {"text": "Last", "key": "LastName"},
    {"text": "Sex", "key": "Sex"},
    {"text": "Email", "key": "Email"},
    {"text": "Phone", "key": "Phone"},
    {"text": "BirthDate", "key": "BirthDate", "dtype": "date"},
    {"text": "JobTitle", "key": "JobTitle"},
]

start = time.perf_counter()
grid = ttk.TableView(
    app,
    columns=columns,
    rows=rows,
    search={"event": "enter"},
    column_auto_width=True,
    row_alternation={"enabled": True},
    editing={"updating": True}
)
grid.pack(fill="both", expand=True, padx=5, pady=5)

grid.on_row_click(print)

elapsed = time.perf_counter() - start
print(f"DataGrid build time: {elapsed:.3f}s for {len(rows)} rows")

app.mainloop()
