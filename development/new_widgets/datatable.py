import ttkbootstrap as ttk
from ttkbootstrap.constants import *


# https://kivymd.readthedocs.io/en/0.104.1/components/datatables/index.html
# https://tcl.tk/man/tcl8.6/TkCmd/ttk_treeview.htm
# load all into table and then detach first, then load from attachments

UPARROW = "🔺"
DOWNARROW = "🔻"


class DataTableRow:
    def __init__(self):
        ...


class DataTableColumn:
    """Represents a column in a DataTable object"""

    def __init__(
        self,
        table,
        cid,
        headertext,
        headerimage="",
        headeranchor=W,
        headercommand="",
        colanchor=W,
        colwidth=200,
        colminwidth=20,
        colstretch=True,
    ):
        self.cid = cid
        self.headertext = headertext
        self.table: ttk.Treeview = table
        self.table.column(
            self.cid,
            width=colwidth,
            minwidth=colminwidth,
            stretch=colstretch,
            anchor=colanchor,
        )
        self.table.heading(
            self.cid,
            text=headertext,
            anchor=headeranchor,
            image=headerimage,
            command=headercommand,
        )


class DataTableRow:
    """Represents a row in a DataTable object"""

    def __init__(self, table, values):
        self.table: ttk.Treeview = table
        self.values = values
        self.iid = None

    def show(self):
        """Show the row in the data table view"""
        if self.iid is None:
            self.build_row()
        self.table.reattach(self.iid, "", END)

    def hide(self):
        """Remove the row from the data table view"""
        self.table.detach(self.iid)

    def cell_configure(self, index, value):
        """Modify the value of a specific cell"""
        self.values[index] = value
        self.table.item(self.iid, values=self.values)

    def build_row(self):
        self.iid = self.table.insert("", END, values=self.values)


class DataTable(ttk.Frame):
    def __init__(
        self,
        master=None,
        bootstyle=PRIMARY,
        coldata=[],
        rowdata=[],
        paginated=False,
        searchable=False,
        pagesize=5,
        height=10,
    ):
        super().__init__(master)
        self.tablecols = []
        self.tablerows = []
        self.tablerows_filtered = []
        self.viewdata = []
        self.rowindex = ttk.IntVar(value=0)
        self.pageindex = ttk.IntVar(value=0)
        self.pagelimit = ttk.IntVar(value=0)
        self.height = height
        self.pagesize = pagesize
        self.paginated = paginated
        self.searchable = searchable
        self.reversed = False
        self.filtered = False
        self.criteria = ttk.StringVar()

        if not paginated:
            self.pagesize = len(rowdata)
        else:
            self.height = self.pagesize

        # create searchbar
        if self.searchable:
            self.build_searchbar()

        # create data table
        self._tableview = ttk.Treeview(
            master=self,
            columns=[x for x in range(len(coldata))],
            height=self.height,
            show=HEADINGS,
            bootstyle=bootstyle,
        )
        self._tableview.pack(fill=BOTH, expand=YES)

        # configure table columns
        for cid, col in enumerate(coldata):
            self.tablecols.append(
                DataTableColumn(
                    table=self._tableview,
                    cid=cid,
                    headertext=col,
                    headercommand=lambda x=cid: self.column_sort(x),
                )
            )

        # build table row objects
        for val in rowdata:
            self.tablerows.append(DataTableRow(self._tableview, val))

        # build the data table
        self.build_table()

    def first_page(self):
        """Update table with first page of data"""
        self.rowindex.set(0)
        self.load_data()

    def last_page(self):
        """Update the table with the last page of data"""
        if self.filtered:
            self.rowindex.set(len(self.tablerows_filtered) - self.pagesize)
        else:
            self.rowindex.set(len(self.tablerows) - self.pagesize)
        self.load_data()

    def next_page(self):
        """Update table with next page of data"""
        pageindex = self.rowindex.get()
        self.rowindex.set(pageindex + self.pagesize)
        self.load_data()

    def prev_page(self):
        """Update table with prev page of data"""
        pageindex = self.rowindex.get()
        self.rowindex.set(pageindex - self.pagesize)
        self.load_data()

    def goto_page(self, *_):
        pageindex = self.pageindex.get()
        self.rowindex.set(pageindex * self.pagesize)
        self.load_data()

    def column_sort(self, key):
        """Sort data column"""
        # update headers
        self.reset_header_labels()
        self.update_sorted_header(key)

        # update table data
        if self.filtered:
            tablerows = self.tablerows_filtered
        else:
            tablerows = self.tablerows

        sortedrows = sorted(
            tablerows, reverse=self.reversed, key=lambda x: x.values[key]
        )
        if self.filtered:
            self.tablerows_filtered = sortedrows
        else:
            self.tablerows = sortedrows

        self.reversed = not self.reversed
        self.unload_data()
        self.load_data()

    def reset_header_labels(self):
        for col in self.tablecols:
            self._tableview.heading(col.cid, text=col.headertext)

    def update_sorted_header(self, cid):
        col = self.tablecols[cid]
        arrow = UPARROW if self.reversed else DOWNARROW
        headertext = f"{col.headertext} {arrow}"
        self._tableview.heading(col.cid, text=headertext)

    def add_rows(self, rowdata=[]):
        ...

    def build_table(self):
        """Build the data table"""
        self.load_data()
        if self.paginated:
            self.build_pageframe()

    def build_searchbar(self):
        """Build the table searchbar"""
        frame = ttk.Frame(self, padding=5)
        frame.pack(fill=X, side=TOP)
        ttk.Label(frame, text="Search").pack(side=LEFT, padx=5)
        searchterm = ttk.Entry(frame, textvariable=self.criteria)
        searchterm.pack(fill=X, side=LEFT, expand=YES)
        searchterm.bind("<Return>", self.search_table_data)
        ttk.Button(frame, text="⤵", command=self.clear_table_filter,
        style='symbol.Link.TButton').pack(
            side=LEFT
        )

    def unload_data(self):
        for row in self.viewdata:
            row.hide()
        self.viewdata.clear()

    def load_data(self):
        """Load table data"""
        self.unload_data()
        page_start = self.rowindex.get()
        page_end = self.rowindex.get() + self.pagesize

        if self.filtered:
            rowdata = self.tablerows_filtered[page_start:page_end]
            rowcount = len(self.tablerows_filtered)
        else:
            rowdata = self.tablerows[page_start:page_end]
            rowcount = len(self.tablerows)

        if len(rowdata) % self.pagesize == 0:
            self.pagelimit.set(rowcount // self.pagesize)
        else:
            self.pagelimit.set((rowcount // self.pagesize) + 1)

        self.pageindex.set(self.rowindex.get() // self.pagesize)

        for row in rowdata:
            row.show()
            self.viewdata.append(row)

    def clear_table_filter(self):
        self.filtered = False
        self.criteria.set("")
        self.unload_data()
        self.load_data()

    def search_table_data(self, _):
        """Search the table for criteria and return the results"""
        criteria = self.criteria.get()
        self.filtered = True
        self.tablerows_filtered.clear()
        self.unload_data()
        data = self.tablerows
        for row in data:
            for col in row.values:
                if str(criteria).lower() in str(col).lower():
                    self.tablerows_filtered.append(row)
                    break
        self.rowindex.set(0)
        self.load_data()

    def build_pageframe(self):
        pageframe = ttk.Frame(self)
        pageframe.pack(fill=X, expand=YES)
        ttk.Button(
            master=pageframe,
            text="»",
            command=self.last_page,
            style="symbol.Link.TButton",
        ).pack(side=RIGHT, fill=Y)
        ttk.Button(
            master=pageframe,
            text="›",
            command=self.next_page,
            style="symbol.Link.TButton",
        ).pack(side=RIGHT, fill=Y)

        ttk.Separator(pageframe, orient=VERTICAL).pack(side=RIGHT)
        ttk.Label(pageframe, textvariable=self.pagelimit).pack(
            side=RIGHT, padx=(0, 5)
        )
        ttk.Label(pageframe, text="of").pack(side=RIGHT, padx=(5, 0))
        index = ttk.Entry(pageframe, textvariable=self.pageindex, width=6)
        index.pack(side=RIGHT)
        index.bind("<Return>", self.goto_page)
        ttk.Label(pageframe, text="Page").pack(side=RIGHT, padx=5)
        ttk.Separator(pageframe, orient=VERTICAL).pack(side=RIGHT)

        ttk.Button(
            master=pageframe,
            text="‹",
            command=self.prev_page,
            style="symbol.Link.TButton",
        ).pack(side=RIGHT, fill=Y)
        ttk.Button(
            master=pageframe,
            text="«",
            command=self.first_page,
            style="symbol.Link.TButton",
        ).pack(side=RIGHT, fill=Y)



if __name__ == "__main__":

    import csv
    from pathlib import Path

    p = Path(".") / "development/new_widgets/Sample1000.csv"

    with open(p, encoding="utf-8") as f:
        reader = csv.reader(f)
        coldata = next(reader)
        rowdata = list(reader)

    app = ttk.Window(themename="flatly")
    app.style.configure("symbol.Link.TButton", font="-size 16")
    dt = DataTable(
        master=app,
        coldata=coldata,
        rowdata=rowdata,
        pagesize=20,
        paginated=True,
        searchable=True,
    )
    dt.pack(fill=BOTH, expand=YES)

    app.mainloop()
