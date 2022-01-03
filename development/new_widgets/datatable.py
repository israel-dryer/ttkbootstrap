import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import font


# https://kivymd.readthedocs.io/en/0.104.1/components/datatables/index.html
# https://tcl.tk/man/tcl8.6/TkCmd/ttk_treeview.htm
# load all into table and then detach first, then load from attachments

UPARROW = "⯅"
DOWNARROW = "⯆"
ASCENDING = 0
DESCENDING = 1


class Tableview(ttk.Frame):
    """A class for arranging data in rows and columns. A Tableview
    object contains various features such has striped rows, pagination,
    and autosized and autoaligned columns.

    The pagination option is recommended when loading a lot of data as
    the table records are inserted on-demand. Table records are only
    created when requested to be in a page view. This allows the table
    to be loaded very quickly even with hundreds of thousands of
    records.

    All table columns are sortable. Clicking a column header will toggle
    between sorting "ascending" and "descending".

    Columns are configurable by passing a simple list of header names or
    by passing in a dictionary of column names with settings. You can
    use both as well, as in the example below, where a column header
    name is use for one column, and a dictionary of settings is used
    for another.

    Examples:

        ```python
        coldata = [
            {"text": "LicenseNumber", "stretch": False},
            "CompanyName",
            {"text": "UserCount", "stretch": False},
        ]

        rowdata = [
            ('A123', 'IzzyCo', 12),
            ('A136', 'Kimdee Inc.', 45)
            ('A158', 'Farmadding Co.', 36)
        ]

        dt = Tableview(
            master=app,
            coldata=coldata,
            rowdata=rowdata,
            paginated=True,
            searchable=True,
            bootstyle=PRIMARY,
            stripecolor=(app.style.colors.light, app.style.colors.fg),
        )
        dt.pack(fill=BOTH, expand=YES, padx=10, pady=10)
        ```
    """

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
        """
        Parameters:

            master (Widget):
                The parent widget.

            bootstyle (str):
                A style keyword used to set the focus color of the entry
                and the background color of the date button. Available
                options include -> primary, secondary, success, info,
                warning, danger, dark, light.

            coldata (List[str | Dict]):
                An iterable containing either the heading name or a
                dictionary of column settings. Configurable settings
                include >> text, image, command, anchor, width, minwidth,
                maxwidth, stretch

            rowdata (List):
                An iterable of row data. The lenth of each row of data
                must match the number of columns.

            paginated (bool):
                Specifies that the data is to be paginated. A pagination
                frame will be created below the table with controls that
                enable the user to page forward and backwards in the
                data set.

            pagesize (int):
                When `paginated=True`, this specifies the number of rows
                to show per page. This is the same as setting `height`
                for non-paginated tables.

            searchable (bool):
                If `True`, a searchbar will be created above the table.
                Press the <Return> key to initiate a search. Searching
                with an empty string will reset the search criteria, or
                pressing the reset button to the right of the search
                bar. Currently, the search method looks for any row
                that contains the search text. The filtered results
                are displayed in the table view.

            autosize (bool):
                If `True`, the table columns will be automatically sized
                based on the records presently in the viewport. You
                may also initiate an adhoc autosize by double-clicking
                the separator between each column header.

            autoalign (bool):
                If `True`, the column headers and data are automatically
                aligned. Numbers and number headers are right-aligned
                and all other data types are left-aligned. The auto
                align method evaluates the first record in each column
                to determine the data type for alignment.

            stripecolor (Tuple[str, str]):
                If provided, even numbered rows will be color using the
                (background, foreground) specified. You may specify one
                or the other by passing in **None**. For example,
                `stripecolor=('green', None)` will set the stripe
                background as green, but the foreground will remain as
                default. You may use standand color names, hexadecimal
                color codes, or bootstyle color keywords. For example,
                ('light', '#222') will set the background to the "light"
                themed ttkbootstrap color and the foreground to the
                specified hexadecimal color.

            height (int):
                Specifies how many rows will appear in the table's viewport.
                If the number of records extends beyond the table height,
                the user may use the mousewheel or scrollbar to navigate
                the data.
        """
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
            if self.stripecolor is not None and i % 2 == 0:
                row.show(True)
            else:
                row.show(False)
            self.viewdata.append(row)

    # WIDGET BUILDERS

    def build_table(self, coldata, rowdata, bootstyle):
        """Build the data table"""
        if self.searchable:
            self.build_search_frame()

        self.tableview = ttk.Treeview(
            master=self,
            columns=[x for x in range(len(coldata))],
            height=self.height,
            show=HEADINGS,
            bootstyle=f"{bootstyle}-table",
        )
        self.tableview.pack(fill=X, side=TOP)

        self.build_table_columns(coldata)
        self.build_table_rows(rowdata)
        # self.build_horizontal_scrollbar()

        self.load_table_data()

        if self.autosize:
            self.autosize_columns()

        if self.autoalign:
            self.autoalign_columns()

        if self.paginated:
            self.build_pagination_frame()

        if self.stripecolor is not None:
            self.configure_table_stripes(self.stripecolor)

        self.widget_binding()

    # def build_horizontal_scrollbar(self):
    #     self.hbar = ttk.Scrollbar(self, orient=HORIZONTAL, command=self.tableview.xview)
    #     self.tableview.configure(xscrollcommand=self.hbar.set)
    #     self.hbar.pack(fill=X, side=TOP)

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
        pageframe.pack(fill=X, anchor=N)

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
        lbl = ttk.Label(pageframe, textvariable=self.pagelimit)
        lbl.pack(side=RIGHT, padx=(0, 5))
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
            self.tablerows.append(TableRow(self.tableview, row))

    def build_table_columns(self, coldata):
        """Build, load, and configure the DataTableColumn objects

        Parameters:

            coldata (List[str|Dict[str, Any]]):
                An iterable of column names or a dictionary of column
                configuration settings.
        """
        for cid, col in enumerate(coldata):
            if isinstance(col, str):
                self.tablecols.append(
                    TableColumn(
                        table=self.tableview,
                        cid=cid,
                        text=col,
                    )
                )
            else:
                if "text" not in col:
                    col["text"] = f"Column {cid}"
                self.tablecols.append(
                    TableColumn(
                        table=self.tableview,
                        cid=cid,
                        **col,
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

        colsort = self.tablecols[cid].sort
        self.tablecols[cid].sort = 1 if colsort == 0 else 0

        sortedrows = sorted(
            tablerows, reverse=colsort, key=lambda x: x.values[cid]
        )
        if self.filtered:
            self.tablerows_filtered = sortedrows
        else:
            self.tablerows = sortedrows

        self.unload_table_data()
        self.load_table_data()

    def column_sort_header_reset(self):
        """Remove sort character from column headers"""
        for col in self.tablecols:
            self.tableview.heading(col.cid, text=col.headertext)

    def column_sort_header_update(self, cid):
        """Add sort character to the sorted column"""
        col = self.tablecols[cid]
        arrow = UPARROW if col.sort else DOWNARROW
        headertext = f"{col.headertext} {arrow}"
        self.tableview.heading(col.cid, text=headertext)

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
            self.tableview.tag_configure(
                "striped", background=bg, foreground=fg
            )

    def autosize_columns(self):
        """Fit the column to the data in the current view, bounded by the
        max size and minsize"""
        f = font.Font()
        column_widths = []

        for i, row in enumerate(self.viewdata):
            if i == 0:
                for col in self.tablecols:
                    column_widths.append(
                        f.measure(f"{col.headertext} {DOWNARROW}")
                    )

            for j, value in enumerate(row.values):
                measure = f.measure(str(value) + " ")
                if column_widths[j] > measure:
                    pass
                elif measure < self.tablecols[j].colmaxwidth:
                    column_widths[j] = measure

        for i, width in enumerate(column_widths):
            self.tableview.column(i, width=width)

    def autoalign_columns(self):
        """Align the columns and headers based on the data type of the
        values. Text is left-aligned, numbers are right-aligned."""
        values = self.tablerows[0].values
        for i, value in enumerate(values):
            if str(value).isnumeric():
                self.tableview.column(i, anchor=E)
                self.tableview.heading(i, anchor=E)

    # Widget binding

    def widget_binding(self):
        self.tableview.bind("<Double-Button-1>", self.header_doubleclick)
        self.tableview.bind("<Button-1>", self.header_click)

    def header_doubleclick(self, event):
        region = self.tableview.identify_region(event.x, event.y)
        if region == "separator":
            self.autosize_columns()

    def header_click(self, event):
        region = self.tableview.identify_region(event.x, event.y)
        if region == "heading":
            cid = (
                int(self.tableview.identify_column(event.x).replace("#", ""))
                - 1
            )
            self.column_sort_data(cid)


class TableColumn:
    """Represents a column in a Tableview object"""

    def __init__(
        self,
        table,
        cid,
        text,
        image="",
        command="",
        anchor=W,
        width=None,
        minwidth=None,
        maxwidth=400,
        stretch=True,
    ):
        self.cid = cid
        self.headertext = text
        self.table: ttk.Treeview = table
        self.colmaxwidth = maxwidth
        self.sort = ASCENDING
        self.tableview = None
        self.hbar = None
        self.table.column(
            self.cid,
            width=width or 200,
            minwidth=minwidth or 20,
            stretch=stretch,
            anchor=anchor,
        )
        self.table.heading(
            self.cid,
            text=text,
            anchor=anchor,
            image=image,
            command=command,
        )


class TableRow:
    """Represents a row in a Tableview object"""

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
        tags = list(self.table.item(self.iid, "tags"))
        # TODO where is the `table.tag_remove` method?
        try:
            tags.remove("striped")
        except ValueError:
            pass

        # add stripes (if needed)
        if striped:
            tags.append("striped")
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
    colors = app.style.colors

    # column configuration options
    # text, image, command, anchor, width, minwidth, maxwidth, stretch
    columns = [
        {"text": "SerialNumber", "stretch": False},
        "CompanyName",
        "Employee",
        "Description",
        {"text": "Leave", "stretch": False},
    ]

    dt = Tableview(
        master=app,
        coldata=columns,
        rowdata=rowdata,
        paginated=True,
        searchable=True,
        bootstyle=PRIMARY,
        stripecolor=(colors.light, colors.fg),
    )
    dt.pack(fill=BOTH, expand=YES, padx=10, pady=10)

    app.mainloop()
