import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import font


# https://kivymd.readthedocs.io/en/0.104.1/components/datatables/index.html
# https://tcl.tk/man/tcl8.6/TkCmd/ttk_treeview.htm
# load all into table and then detach first, then load from attachments

UPARROW = "⯅"
DOWNARROW = "⯆"

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
        colwidth=None,
        colminwidth=None,
        colmaxwidth=500,
        colstretch=False,
    ):
        self.cid = cid
        self.headertext = headertext
        self.table: ttk.Treeview = table
        self.colmaxwidth = colmaxwidth
        
        f = font.Font()

        self.table.column(
            self.cid,
            width=colwidth or 200,
            minwidth=colminwidth or 20,
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

    def show(self, striped=False):
        """Show the row in the data table view"""
        if self.iid is None:
            self.build_row()
        self.table.reattach(self.iid, "", END)

        # remove existing stripes
        tags = list(self.table.item(self.iid, 'tags'))
        try:
            tags.remove('striped')
        except ValueError:
            pass
        
        # add stripes (if needed)
        if striped:
            tags.append('striped')
        self.table.item(self.iid, tags=tags)

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
        bootstyle=DEFAULT,
        coldata=[],
        rowdata=[],
        paginated=False,
        searchable=False,
        autosize=True,
        autoalign=True,
        stripecolor=None,
        pagesize=15,
        height=10,
    ):
        super().__init__(master)
        self.tablecols = []
        self.tablerows = []
        self.tablerows_filtered = []
        self.viewdata = []
        self.rowindex = ttk.IntVar(value=0)
        self.pageindex = ttk.IntVar(value=1)
        self.pagelimit = ttk.IntVar(value=0)    
        self.height = height
        self.pagesize = pagesize
        self.paginated = paginated
        self.searchable = searchable
        self.stripecolor = stripecolor
        self.autosize = autosize
        self.autoalign = autoalign
        self.reversed = False
        self.filtered = False
        self.criteria = ttk.StringVar()

        if not paginated:
            self.pagesize = len(rowdata)
        else:
            self.height = self.pagesize

        self.build_table(coldata, rowdata, bootstyle)

    # DATA LOADING

    def unload_table_data(self):
        for row in self.viewdata:
            row.hide()
        self.viewdata.clear()

    def load_table_data(self):
        """Load table data"""
        self.unload_table_data()
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

        self.pageindex.set((self.rowindex.get() // self.pagesize) + 1)

        for i, row in enumerate(rowdata):
            if self.stripecolor is not None and i%2 == 0:
                row.show(True)
            else:
                row.show(False)
            self.viewdata.append(row)

    # WIDGET BUILDERS

    def build_table(self, coldata, rowdata, bootstyle):
        """Build the data table"""
        if self.searchable:
            self.build_search_frame()

        self._tableview = ttk.Treeview(
            master=self,
            columns=[x for x in range(len(coldata))],
            height=self.height,
            show=HEADINGS,
            bootstyle=bootstyle,
        )
        self._tableview.pack(fill=BOTH, expand=YES)

        self.build_table_columns(coldata)
        self.build_table_rows(rowdata)

        self.load_table_data()
        
        if self.autosize:
            self.autosize_columns()

        if self.autoalign:
            self.autoalign_columns()

        if self.paginated:
            self.build_pagination_frame()

        if self.stripecolor is not None:
            self.configure_table_stripes(self.stripecolor)

    def build_search_frame(self):
        """Build the search frame containing the search widgets. This
        frame is only created if `searchable=True` when creating the
        widget.
        """
        frame = ttk.Frame(self, padding=5)
        frame.pack(fill=X, side=TOP)
        ttk.Label(frame, text="Search").pack(side=LEFT, padx=5)
        searchterm = ttk.Entry(frame, textvariable=self.criteria)
        searchterm.pack(fill=X, side=LEFT, expand=YES)
        searchterm.bind("<Return>", self.search_table_data)
        ttk.Button(
            frame,
            text="⤵",
            command=self.clear_table_filter,
            style="symbol.Link.TButton",
        ).pack(side=LEFT)

    def build_pagination_frame(self):
        """Build the frame containing the pagination widgets. This
        frame is only built if `pagination=True` when creating the
        widget.
        """
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

    def build_table_rows(self, rowdata):
        """Build, load, and configure the DataTableRow objects

        Parameters:

            rowdata (List):
                An iterable of row data
        """
        for row in rowdata:
            self.tablerows.append(DataTableRow(self._tableview, row))

    def build_table_columns(self, coldata):
        """Build, load, and configure the DataTableColumn objects

        Parameters:

            coldata (List):
                An iterable of column names and configuration settings.
        """
        for cid, col in enumerate(coldata):
            self.tablecols.append(
                DataTableColumn(
                    table=self._tableview,
                    cid=cid,
                    headertext=col,
                    headercommand=lambda x=cid: self.column_sort_data(x),
                )
            )

    # PAGE NAVIGATION

    def first_page(self):
        """Update table with first page of data"""
        self.rowindex.set(0)
        self.load_table_data()

    def last_page(self):
        """Update the table with the last page of data"""
        if self.filtered:
            self.rowindex.set(len(self.tablerows_filtered) - self.pagesize)
        else:
            self.rowindex.set(len(self.tablerows) - self.pagesize)
        self.load_table_data()

    def next_page(self):
        """Update table with next page of data"""
        if self.pageindex.get() >= self.pagelimit.get():
            return
        rowindex = self.rowindex.get()
        self.rowindex.set(rowindex + self.pagesize)
        self.load_table_data()

    def prev_page(self):
        """Update table with prev page of data"""
        if self.pageindex.get() <= 1:
            return
        rowindex = self.rowindex.get()
        self.rowindex.set(rowindex - self.pagesize)
        self.load_table_data()

    def goto_page(self, *_):
        """Go to a specific page indicate in the page entry widget."""
        pageindex = self.pageindex.get() - 1
        self.rowindex.set(pageindex * self.pagesize)
        self.load_table_data()

    # COLUMN SORTING

    def column_sort_data(self, cid):
        """Sort the table rows by the specified column id"""
        # update headers
        self.column_sort_header_reset()
        self.column_sort_header_update(cid)

        # update table data
        if self.filtered:
            tablerows = self.tablerows_filtered
        else:
            tablerows = self.tablerows

        sortedrows = sorted(
            tablerows, reverse=self.reversed, key=lambda x: x.values[cid]
        )
        if self.filtered:
            self.tablerows_filtered = sortedrows
        else:
            self.tablerows = sortedrows

        self.reversed = not self.reversed
        self.unload_table_data()
        self.load_table_data()

    def column_sort_header_reset(self):
        """Remove sort character from column headers"""
        for col in self.tablecols:
            self._tableview.heading(col.cid, text=col.headertext)

    def column_sort_header_update(self, cid):
        """Add sort character to the sorted column"""
        col = self.tablecols[cid]
        arrow = UPARROW if self.reversed else DOWNARROW
        headertext = f"{col.headertext} {arrow}"
        self._tableview.heading(col.cid, text=headertext)

    # DATA SEARCH

    def clear_table_filter(self):
        """Remove all filters from table data and set filtered flag."""
        self.filtered = False
        self.criteria.set("")
        self.unload_table_data()
        self.load_table_data()

    def search_table_data(self, _):
        """Search the table data for records that meet search criteria.
        Currently, this search locates any records that contains the
        specified text; it is also case insensitive.
        """
        criteria = self.criteria.get()
        self.filtered = True
        self.tablerows_filtered.clear()
        self.unload_table_data()
        data = self.tablerows
        for row in data:
            for col in row.values:
                if str(criteria).lower() in str(col).lower():
                    self.tablerows_filtered.append(row)
                    break
        self.rowindex.set(0)
        self.load_table_data()

    # OTHER FORMATTING

    def configure_table_stripes(self, stripecolor):
        """Add stripes to even table rows"""
        if len(stripecolor) == 2:
            self.stripecolor = stripecolor
            bg, fg = stripecolor
            self._tableview.tag_configure('striped', background=bg, foreground=fg)

    def autosize_columns(self):
        """Fit the column to the data in the current view, bounded by the 
        max size and minsize"""
        f = font.Font()
        column_widths = []
        
        for i, row in enumerate(self.viewdata):
            if i == 0:
                for col in self.tablecols:
                    column_widths.append(f.measure(f'{col.headertext} {DOWNARROW}'))

            for j, value in enumerate(row.values):
                measure = f.measure(str(value) + ' ')
                if column_widths[j] > measure:
                    pass
                elif measure < self.tablecols[j].colmaxwidth:
                    column_widths[j] = measure

        for i, width in enumerate(column_widths):
            self._tableview.column(i, width=width)
        
    def autoalign_columns(self):
        """Align the columns and headers based on the data type of the
        values. Text is left-aligned, numbers are right-aligned."""
        values = self.tablerows[0].values
        for i, value in enumerate(values):
            if str(value).isnumeric():
                self._tableview.column(i, anchor=E)
                self._tableview.heading(i, anchor=E)


if __name__ == "__main__":

    import csv
    from pathlib import Path

    p = Path(".") / "development/new_widgets/Sample1000.csv"

    with open(p, encoding="utf-8") as f:
        reader = csv.reader(f)
        coldata = next(reader)
        rowdata = list(reader)

    app = ttk.Window()
    app.style.configure("symbol.Link.TButton", font="-size 16")
    dt = DataTable(
        master=app,
        coldata=coldata,
        rowdata=rowdata,
        paginated=True,
        searchable=True,
        bootstyle=INFO,
        stripecolor=(app.style.colors.light, app.style.colors.fg)
    )
    dt.pack(fill=BOTH, expand=YES, padx=10, pady=10)

    app.mainloop()
