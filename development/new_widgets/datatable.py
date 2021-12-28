import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from uuid import uuid4

testdata = []

for x in range(1000000):
    testdata.append([y + x for y in range(5)])


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
        coldata=[],
        rowdata=[],
        paginated=False,
        pagesize=5,
        height=10,
    ):
        super().__init__(master)
        self.tablecols = []
        self.tablerows = []
        self.viewdata = []
        self.pageindex = 0
        self.height = height
        self.pagesize = pagesize
        self.paginated = paginated
        self.reversed = False

        if not paginated:
            self.pagesize = len(rowdata)
        else:
            self.height = self.pagesize

        self._tableview = ttk.Treeview(
            master=self,
            columns=[x for x in range(len(coldata))],
            height=self.height,
            show=HEADINGS,
            bootstyle=PRIMARY,
        )
        self._tableview.pack(fill=BOTH, expand=YES)

        for cid, col in enumerate(coldata):
            self.tablecols.append(
                DataTableColumn(
                    table=self._tableview, 
                    cid=cid, 
                    headertext=col, 
                    headercommand=lambda x=cid: self.column_sort(x)
                )
            )

        for val in rowdata:
            self.tablerows.append(DataTableRow(self._tableview, val))

        self.build_table()

    def first_page(self):
        """Update table with first page of data"""
        self.pageindex = 0
        self.load_data()

    def last_page(self):
        """Update the table with the last page of data"""
        self.pageindex = len(self.tablerows) - self.pagesize
        self.load_data()

    def next_page(self):
        """Update table with next page of data"""
        self.pageindex += self.pagesize
        self.load_data()

    def prev_page(self):
        """Update table with prev page of data"""
        self.pageindex -= self.pagesize
        self.load_data()

    def column_sort(self, key):
        """Sort data column"""
        # update headers
        self.reset_header_labels()
        self.update_sorted_header(key)

        # update table data
        tablerows = self.tablerows
        sortedrows = sorted(
            tablerows, reverse=self.reversed, key=lambda x: x.values[key]
        )
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

    def unload_data(self):
        for row in self.viewdata:
            row.hide()
        self.viewdata.clear()

    def load_data(self):
        """Load table data"""
        self.unload_data()
        page_start = self.pageindex
        page_end = self.pageindex + self.pagesize
        row_data = self.tablerows[page_start:page_end]
        for row in row_data:
            row.show()
            self.viewdata.append(row)

    def build_pageframe(self):
        pageframe = ttk.Frame(self)
        pageframe.pack(fill=X, expand=YES)
        ttk.Button(
            master=pageframe, text=">>", width=4, command=self.last_page
        ).pack(side=RIGHT)
        ttk.Button(
            master=pageframe, text=">", width=4, command=self.next_page
        ).pack(side=RIGHT, padx=5)
        ttk.Button(
            master=pageframe, text="<", width=4, command=self.prev_page
        ).pack(side=RIGHT)
        ttk.Button(
            master=pageframe, text="<<", width=4, command=self.first_page
        ).pack(side=RIGHT, padx=5)


if __name__ == "__main__":

    app = ttk.Window()

    dt = DataTable(
        master=app,
        coldata=["Col1", "Col2", "Col3", "Col4", "Col5"],
        rowdata=testdata,
        pagesize=15,
        paginated=True,
    )
    dt.pack()

    app.mainloop()
