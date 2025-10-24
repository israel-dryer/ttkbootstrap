import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.tableview import TableRow, Tableview

app = ttk.Window(themename='flatly')
colors = app.style.colors

# p = Path(__file__).parent / "Sample1000.csv"
# with open(p, encoding="utf-8") as f:
#     reader = csv.reader(f)
#     next(reader)
#     rowdata = list(reader)

row_data = [
    (1001, "Acme Corp", "Software Engineer", 5),
    (1002, "BrightPath Ltd", "Data Analyst", 3),
    (1003, "Summit Technologies", "Project Manager", 7),
    (1004, "Northwind Systems", "UX Designer", 4),
    (1005, "BlueSky Analytics", "Database Administrator", 6),
    (1006, "Evergreen Solutions", "Network Engineer", 8),
    (1007, "Nova Group", "HR Specialist", 2),
    (1008, "Horizon Dynamics", "Marketing Coordinator", 5),
    (1009, "Silverline Corp", "Financial Analyst", 4),
    (1010, "Quantum Industries", "Operations Manager", 9),
    (1011, "NextGen Labs", "Research Scientist", 6),
    (1012, "Starwave Media", "Content Strategist", 3),
    (1013, "FusionWorks", "Mechanical Engineer", 10),
    (1014, "Lighthouse Partners", "Business Analyst", 2),
    (1015, "Apex Holdings", "Legal Counsel", 7),
    (1016, "UrbanTech", "Software Architect", 9),
    (1017, "VantagePoint Inc", "Quality Assurance Engineer", 4),
    (1018, "Clearwater Consulting", "Product Owner", 5),
    (1019, "Atlas Retail", "Sales Executive", 3),
    (1020, "Momentum Logistics", "Supply Chain Specialist", 6),
    (1021, "SkyBridge Finance", "Investment Advisor", 8),
    (1022, "Cascade Energy", "Electrical Engineer", 7),
    (1023, "Veridian Health", "Medical Technician", 5),
    (1024, "GreenLeaf Foods", "Production Supervisor", 4),
    (1025, "BrightWorks Design", "Graphic Designer", 3),
]


# column configuration options
# text, image, command, anchor, width, minwidth, maxwidth, stretch
col_data = [
    {"text": "EmployeeNumber", "stretch": False},
    "CompanyName",
    "Occupation",
    {"text": "YearsOfService", "stretch": False},
]


def handle_selection(event: list[TableRow]):
    if len(event) > 0:
        print(event[0].iid)


dt = Tableview(
    coldata=col_data,
    rowdata=row_data,
    master=app,
    paginated=True,
    disable_right_click=True,
    searchable=True,
    bootstyle=PRIMARY,
    stripecolor=(None, None),
    autofit=False,
    on_select=handle_selection,
    iid_field="EmployeeNumber"
)
dt.pack(fill='both', expand=1, padx=5, pady=5)

# dt.build_table_data(coldata, rowdata)
# dt.delete_columns(indices=[2, 3])

# modify the contents of a single cell
#row = dt.get_row(0)
#row.values[2] = "Israel"
#row.refresh()

# modify an entire row
#row = dt.get_row(1)
#row.values = ['123456', 'My Company', 'Israel', 'Something here', 45]

#dt.search_table_data(2, "Leave")

app.mainloop()
