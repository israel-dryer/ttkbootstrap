import csv
import time
from pathlib import Path

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.widgets.tableview import TableRow, Tableview

app = ttk.Window(themename='flatly')
colors = app.style.colors

p = Path(__file__).parent / "Sample1000.csv"
with open(p, encoding="utf-8") as f:
    reader = csv.reader(f)
    next(reader)
    row_data = list(reader)

    table_data = []

for x in range(1002):
    table_data.extend(row_data)

print(f"Combined row count: {len(table_data):,}")

# row_data = [
#     (1001, "Acme Corp", "Software Engineer", 5),
#     (1002, "BrightPath Ltd", "Data Analyst", 3),
#     (1003, "Summit Technologies", "Project Manager", 7),
#     (1004, "Northwind Systems", "UX Designer", 4),
#     (1005, "BlueSky Analytics", "Database Administrator", 6),
#     (1006, "Evergreen Solutions", "Network Engineer", 8),
#     (1007, "Nova Group", "HR Specialist", 2),
#     (1008, "Horizon Dynamics", "Marketing Coordinator", 5),
#     (1009, "Silverline Corp", "Financial Analyst", 4),
#     (1010, "Quantum Industries", "Operations Manager", 9),
#     (1011, "NextGen Labs", "Research Scientist", 6),
#     (1012, "Starwave Media", "Content Strategist", 3),
#     (1013, "FusionWorks", "Mechanical Engineer", 10),
#     (1014, "Lighthouse Partners", "Business Analyst", 2),
#     (1015, "Apex Holdings", "Legal Counsel", 7),
#     (1016, "UrbanTech", "Software Architect", 9),
#     (1017, "VantagePoint Inc", "Quality Assurance Engineer", 4),
#     (1018, "Clearwater Consulting", "Product Owner", 5),
#     (1019, "Atlas Retail", "Sales Executive", 3),
#     (1020, "Momentum Logistics", "Supply Chain Specialist", 6),
#     (1021, "SkyBridge Finance", "Investment Advisor", 8),
#     (1022, "Cascade Energy", "Electrical Engineer", 7),
#     (1023, "Veridian Health", "Medical Technician", 5),
#     (1024, "GreenLeaf Foods", "Production Supervisor", 4),
#     (1025, "BrightWorks Design", "Graphic Designer", 3),
# ]


# column configuration options
# text, image, command, anchor, width, minwidth, maxwidth, stretch
col_data = [
    "Serial Number", "Company Name", "Employee", "Description", "Leave"
]


def handle_selection(event: list[TableRow]):
    if len(event) > 0:
        print(event[0].iid)


# ============ PERFORMANCE TEST ============
print("\n" + "="*60)
print("PERFORMANCE TEST: Loading table data into Tableview")
print("="*60)

start_time = time.perf_counter()
dt = Tableview(
    coldata=col_data,
    rowdata=table_data,
    master=app,
    paginated=True,
    disable_right_click=True,
    searchable=True,
    bootstyle=PRIMARY,
    autofit=False,
    on_select=handle_selection
)
end_time = time.perf_counter()
load_time = end_time - start_time

print(f"✓ Table created with {len(table_data):,} rows")
print(f"✓ Load time: {load_time:.4f} seconds ({load_time*1000:.2f}ms)")
print(f"✓ Rows per second: {len(table_data)/load_time:,.0f}")
print("="*60 + "\n")

dt.pack(fill='both', expand=1, padx=5, pady=5)

# ============ PERFORMANCE TEST PANEL ============
test_frame = ttk.Frame(app, padding=10)
test_frame.pack(fill='x', side='bottom')

ttk.Label(test_frame, text="Performance Tests:", font=('TkDefaultFont', 10, 'bold')).pack(side='left', padx=(0, 10))

def check_paging():
    """Test page navigation speed"""
    iterations = 100
    print(f"\nTesting page navigation ({iterations} iterations)...")

    start = time.perf_counter()
    for i in range(iterations):
        dt.goto_next_page()
    mid = time.perf_counter()
    for i in range(iterations):
        dt.goto_prev_page()
    end = time.perf_counter()

    next_time = (mid - start) / iterations * 1000
    prev_time = (end - mid) / iterations * 1000

    print(f"  ✓ Next page: {next_time:.2f}ms per page")
    print(f"  ✓ Prev page: {prev_time:.2f}ms per page")
    print(f"  ✓ Average: {(next_time + prev_time)/2:.2f}ms per page")

def check_search():
    """Test search performance"""
    print(f"\nTesting search performance...")

    start = time.perf_counter()
    dt.search_table_data("Corp")
    end = time.perf_counter()
    search_time = (end - start) * 1000

    filtered_count = len(dt.tablerows_filtered)
    print(f"  ✓ Search time: {search_time:.2f}ms")
    print(f"  ✓ Found: {filtered_count:,} matching rows")

    # Reset
    dt.reset_row_filters()
    print(f"  ✓ Filter reset")

def check_jump_to_end():
    """Test jumping to last page"""
    print(f"\nTesting jump to last page...")

    start = time.perf_counter()
    dt.goto_last_page()
    end = time.perf_counter()
    jump_time = (end - start) * 1000

    print(f"  ✓ Jump to end: {jump_time:.2f}ms")

    # Go back to start
    dt.goto_first_page()

ttk.Button(test_frame, text="Test Paging", command=check_paging, bootstyle="success").pack(side='left', padx=2)
ttk.Button(test_frame, text="Test Search", command=check_search, bootstyle="info").pack(side='left', padx=2)
ttk.Button(test_frame, text="Test Jump to End", command=check_jump_to_end, bootstyle="warning").pack(side='left', padx=2)

app.mainloop()
