import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from math import ceil
from datetime import datetime
from tkinter import font
from ttkbootstrap import utility
from typing import Any, List, Union

UPARROW = "⬆"
DOWNARROW = "⬇"
ASCENDING = 0
DESCENDING = 1


class TableColumn:
    """Represents a column in a Tableview object"""

    def __init__(
        self,
        view,
        cid,
        text,
        image="",
        command="",
        anchor=W,
        width=200,
        minwidth=20,
        stretch=False,
    ):
        """
        Parameters:

            view (Treeview):
                The internal Treeview object of the Tableview.

            cid (str):
                The column id.

            text (str):
                The header text.

            image (PhotoImage):
                An image that is displayed to the left of the header text.

            command (Callable):
                A function called whenever the header button is clicked.

            anchor (str):
                The position of the header text within the header. One
                of "e", "w", "center".

            width (int):
                Specifies the width of the column in pixels.

            minwidth (int):
                Specifies the minimum width of the column in pixels.

            stretch (bool):
                Specifies whether or not the column width should be
                adjusted whenever the widget is resized or the user
                drags the column separator.
        """
        self._cid = cid
        self._headertext = text
        self._sort = ASCENDING
        self._settings_column = {}
        self._settings_heading = {}
        
        self.view: ttk.Treeview = view
        self.view.column(
            self._cid,
            width=width,
            minwidth=minwidth,
            stretch=stretch,
            anchor=anchor,
        )
        self.view.heading(
            self._cid,
            text=text,
            anchor=anchor,
            image=image,
            command=command,
        )
        self._capture_settings()

    @property
    def cid(self):
        """A unique column identifier"""
        return self._cid

    def configure(self, opt=None, **kwargs):
        """Configure the column. If opt is provided, the 
        current value is returned, otherwise, sets the widget 
        options specified in kwargs. See the documentation for
        `Tableview.insert_column` for configurable options.

        Parameters:

            opt (str):
                A configuration option to query.

            **kwargs (Dict):
                Optional keyword arguments used to configure the
                column and headers.
        """
        # return queried options
        if opt is not None:
            if opt in ("anchor", "width", "minwidth", "stretch"):
                return self.view.column(self._cid, opt)
            elif opt in ("command", "text", "image"):
                return self.view.heading(self._cid, opt)
            else:
                return

        # configure column and heading
        for k, v in kwargs.items():
            if k in ("anchor", "width", "minwidth", "stretch"):
                self._settings_column[k] = v
            elif k in ("command", "text", "image"):
                self._settings_heading[k] = v
        self.view.column(self._cid, **self._settings_column)
        self.view.heading(self._cid, **self._settings_heading)
        if "text" in kwargs:
            self._headertext = kwargs["text"]

    def show(self):
        """Make the column visible in the tableview"""
        displaycols = list(self.view.configure("displaycolumns"))
        if "#all" in displaycols:
            return
        if str(self._cid) in displaycols:
            return
        columns = list(self.view.configure("columns"))
        index = columns.index(str(self._cid))
        displaycols.insert(index, str(self._cid))
        self.view.configure(displaycolumns=displaycols)   

    def hide(self):
        """Hide the column in the tableview"""
        displaycols = list(self.view.configure("displaycolumns"))
        cols = list(self.view.configure("columns"))
        if "#all" in displaycols:
            displaycols = cols
        displaycols.remove(str(self._cid))
        self.view.configure(displaycolumns=displaycols)         

    def restore_settings(self):
        """Update the configuration based on stored settings"""
        self.view.column(self.cid, **self._settings_column)
        self.view.heading(self.cid, **self._settings_heading)        

    def _capture_settings(self):
        """Udpate the stored settings for the column and heading.
        This is required because the settings are erased whenever
        the `columns` parameter is configured in the underlying
        Treeview widget."""
        self._settings_heading = self.view.heading(self.cid)
        self._settings_heading.pop('state')
        self._settings_column = self.view.column(self.cid)
        self._settings_column.pop('id')                


class TableRow:
    """Represents a row in a Tableview object"""

    def __init__(self, table, values):
        """
        Parameters:

            table (Treeview):
                The inner Treeview object within the Tableview

            values (List[Any, ...]):
                A list of values to display in the row
        """
        self._values = values
        self._iid = None
        self.view: ttk.Treeview = table

    @property
    def iid(self):
        """A unique record identifier"""
        return self._iid

    def configure(self, opt=None, **kwargs):
        """Configure the row. If opt is provided, the 
        current value is returned, otherwise, sets the widget
        options specified in kwargs. See the documentation for
        `Tableview.insert_row` for configurable options.

        Parameters:

            opt (str):
                A configuration option to query.

            **kwargs { values, tags }:
                Optional keyword arguments used to configure the
                row.
        """
        if self._iid is None:
            self.build()
        
        if opt is not None:
            return self.view.item(self.iid, opt)
        else:
            self.view.item(self.iid, **kwargs)

    def show(self, striped=False):
        """Show the row in the data table view"""
        if self._iid is None:
            self.build()
        self.view.reattach(self._iid, "", END)

        # remove existing stripes
        tags = list(self.view.item(self._iid, "tags"))
        try:
            tags.remove("striped")
        except ValueError:
            pass

        # add stripes (if needed)
        if striped:
            tags.append("striped")
        self.view.item(self._iid, tags=tags)

    def hide(self):
        """Remove the row from the data table view"""
        self.view.detach(self._iid)

    def build(self):
        """Create the row object in the `Treeview` and capture
        the resulting item id (iid).
        """
        if self._iid is None:
            self._iid = self.view.insert("", END, values=self._values)


class Tableview(ttk.Frame):
    """A class built on the `ttk.Treeview` widget for arranging data in
    rows and columns. The underlying Treeview object and its methods are
    exposed in the `Tableview.view` property.

    A Tableview object contains various features such has striped rows,
    pagination, and autosized and autoaligned columns.

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

    The object has a right-click menu on the header and the cells that
    allow you to configure various settings.

    ![](../../assets/widgets/tableview-1.png)
    ![](../../assets/widgets/tableview-2.png)

    Examples:

        Adding data with the constructor
        ```python
        import ttkbootstrap as ttk
        from ttkbootstrap.constants import *

        app = ttk.Window()
        colors = app.style.colors

        coldata = [
            {"text": "LicenseNumber", "stretch": False},
            "CompanyName",
            {"text": "UserCount", "stretch": False},
        ]

        rowdata = [
            ('A123', 'IzzyCo', 12),
            ('A136', 'Kimdee Inc.', 45),
            ('A158', 'Farmadding Co.', 36)
        ]

        dt = ttk.Tableview(
            master=app,
            coldata=coldata,
            rowdata=rowdata,
            paginated=True,
            searchable=True,
            bootstyle=PRIMARY,
            stripecolor=(colors.light, None),
        )
        dt.pack(fill=BOTH, expand=YES, padx=10, pady=10)

        app.mainloop()
        ```

        Add data with methods
        ```python
        dt.insert_row('end', ['Marzale LLC', 26])
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
        autofit=False,
        autoalign=True,
        stripecolor=None,
        pagesize=10,
        height=10,
        delimiter=","
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
                maxwidth, stretch. Also see `Tableview.insert_column`.

            rowdata (List):
                An iterable of row data. The lenth of each row of data
                must match the number of columns. Also see
                `Tableview.insert_row`.

            paginated (bool):
                Specifies that the data is to be paginated. A pagination
                frame will be created below the table with controls that
                enable the user to page forward and backwards in the
                data set.

            pagesize (int):
                When `paginated=True`, this specifies the number of rows
                to show per page.

            searchable (bool):
                If `True`, a searchbar will be created above the table.
                Press the <Return> key to initiate a search. Searching
                with an empty string will reset the search criteria, or
                pressing the reset button to the right of the search
                bar. Currently, the search method looks for any row
                that contains the search text. The filtered results
                are displayed in the table view.

            autofit (bool):
                If `True`, the table columns will be automatically sized
                when loaded based on the records in the current view.
                Also see `Tableview.autofit_columns`.

            autoalign (bool):
                If `True`, the column headers and data are automatically
                aligned. Numbers and number headers are right-aligned
                and all other data types are left-aligned. The auto
                align method evaluates the first record in each column
                to determine the data type for alignment. Also see
                `Tableview.autoalign_columns`.

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
                specified hexadecimal color. Also see 
                `Tableview.apply_table_stripes`.

            height (int):
                Specifies how many rows will appear in the table's viewport.
                If the number of records extends beyond the table height,
                the user may use the mousewheel or scrollbar to navigate
                the data.

            delimiter (str):
                The character to use as a delimiter when exporting data
                to CSV.
        """
        super().__init__(master)
        self._tablecols = []
        self._tablerows = []
        self._tablerows_filtered = []
        self._viewdata = []
        self._rowindex = tk.IntVar(value=0)
        self._pageindex = tk.IntVar(value=1)
        self._pagelimit = tk.IntVar(value=0)
        self._height = height
        self._pagesize = tk.IntVar(value=pagesize)
        self._paginated = paginated
        self._searchable = searchable
        self._stripecolor = stripecolor
        self._autofit = autofit
        self._autoalign = autoalign
        self._filtered = False
        self._searchcriteria = tk.StringVar()
        self._rightclickmenu_cell = None
        self._delimiter = delimiter
        
        self.view: ttk.Treeview = None
        self._build_table(coldata, rowdata, bootstyle)

    def configure(self, cnf=None, **kwargs) -> Union[Any, None]:
        """Configure the internal `Treeview` widget. If cnf is provided, 
        value of the option is return. Otherwise the widget is 
        configured via kwargs.

        Parameters:

            cnf (Any):
                An option to query.

            **kwargs (Dict):
                Optional keyword arguments used to configure the internal
                Treeview widget.

        Returns:

            Union[Any, None]:
                The value of cnf or None.
        """    
        try:
            self.view.configure(cnf, **kwargs)
        except:
            super().configure(cnf, **kwargs)

    # DATA HANDLING

    def insert_row(self, index=END, values=[]) -> TableRow:
        """Insert a row into the tableview at index.

        You must call `Tableview.load_table_data()` to update the
        current view. If the data is filtered, you will need to call
        `Tableview.load_table_data(clear_filters=True)`.

        Parameters:

            index (Union[int, str]):
                A numerical index that specifieds where to insert
                the record in the dataset. You may also use the string
                'end' to append the record to the end of the data set.
                If the index exceeds the record count, it will be
                appended to the end of the dataset.

            values (Iterable):
                An iterable of values to insert into the data set.
                The number of columns implied by the list of values
                must match the number of columns in the data set for
                the values to be visible.

        Returns:

            TableRow:
                A table row object.
        """
        rowcount = len(self._tablerows)

        # validate the index
        if len(values) == 0:
            return
        if index == END:
            index = -1
        elif index > rowcount - 1:
            index = -1

        record = TableRow(self.view, values)
        if rowcount == 0 or index == -1:
            self._tablerows.append(record)
        else:
            self._tablerows.insert(index, record)
        
        return record

    def insert_column(
        self,
        index,
        text="",
        image="",
        command="",
        anchor=W,
        width=200,
        minwidth=20,
        stretch=False,
    ) -> TableColumn:
        """
        Parameters:

            index (Union[int, str]):
                A numerical index that specifieds where to insert
                the column. You may also use the string 'end' to
                insert the column in the right-most position. If the
                index exceeds the column count, it will be inserted
                at the right-most position.

            text (str):
                The header text.

            image (PhotoImage):
                An image that is displayed to the left of the header text.

            command (Callable):
                A function called whenever the header button is clicked.

            anchor (str):
                The position of the header text within the header. One
                of "e", "w", "center".

            width (int):
                Specifies the width of the column in pixels.

            minwidth (int):
                Specifies the minimum width of the column in pixels.

            stretch (bool):
                Specifies whether or not the column width should be
                adjusted whenever the widget is resized or the user
                drags the column separator.

        Returns:

            TableColumn:
                A table column object.
        """
        self.clear_filters()
        colcount = len(self._tablecols)
        cid = colcount
        if index == END:
            index = -1
        elif index > colcount - 1:
            index = -1

        # actual columns
        cols = self.view.cget("columns")
        if len(cols) > 0:
            cols = [int(x) for x in cols]
            cols.append(cid)
            # if index == -1:
            #     cols.append(cid)
            # else:
            #     cols.insert(index, cid)
        else:
            cols = [cid]

        # visible columns
        dcols = self.view.cget("displaycolumns")
        if "#all" in dcols:
            dcols = cols
        elif len(dcols) > 0:
            dcols = [int(x) for x in dcols]
            if index == -1:
                dcols.append(cid)
            else:
                dcols.insert(index, cid)
        else:
            dcols = [cid]

        self.view.configure(columns=cols, displaycolumns=dcols)

        # configure new column
        column = TableColumn(
            view=self.view,
            cid=cid,
            text=text,
            image=image,
            command=command,
            anchor=anchor,
            width=width,
            minwidth=minwidth,
            stretch=stretch,
        )
        self._tablecols.append(column)
        # must be called to show the header after initially creating it
        # ad hoc, not sure why this should be the case;
        self._column_sort_header_reset()

        # update settings after they are erased when a column is 
        #   inserted
        for column in self._tablecols:
            column.restore_settings()

        return column

    def unload_table_data(self):
        """Unload all data from the table"""
        for row in self._viewdata:
            row.hide()
        self._viewdata.clear()

    def load_table_data(self, clear_filters=False):
        """Load records into the tableview.

        Parameters:

            clear_filters (bool):
                Specifies that the table filters should be cleared
                before loading the data into the view.
        """
        if len(self._tablerows) == 0:
            return

        if clear_filters:
            self.clear_filters()
        self.unload_table_data()
        page_start = self._rowindex.get()
        page_end = self._rowindex.get() + self._pagesize.get()

        if self._filtered:
            rowdata = self._tablerows_filtered[page_start:page_end]
            rowcount = len(self._tablerows_filtered)
        else:
            rowdata = self._tablerows[page_start:page_end]
            rowcount = len(self._tablerows)

        self._pagelimit.set(ceil(rowcount / self._pagesize.get()))

        pageindex = ceil(page_end / self._pagesize.get())
        pagelimit = self._pagelimit.get()
        self._pageindex.set(min([pagelimit, pageindex]))

        for i, row in enumerate(rowdata):
            if self._stripecolor is not None and i % 2 == 0:
                row.show(True)
            else:
                row.show(False)
            self._viewdata.append(row)

    def fill_empty_columns(self, fillvalue=''):
        """Fill empty columns with the fillvalue.

        This method can be used to fill in missing values when a column
        column is inserted after data has already been inserted into
        the tableview.
        
        Parameters:

            fillvalue (Any):
                A value to insert into an empty column
        """
        rowcount = len(self._tablerows)
        if rowcount == 0:
            return
        colcount = len(self._tablecols)
        for row in self._tablerows:
            var = colcount - len(row._values)
            if var <= 0:
                return
            else:
                for _ in range(var):
                    row._values.append(fillvalue)
                row.configure(values=row._values)

    # CONFIGURATION

    def get_columns(self) -> List[TableColumn]:
        """Returns a list of all column objects"""
        return self._tablecols

    def get_column(self, index, visible=False) -> Union[TableColumn, None]:
        """Returns the `TableColumn` object for the column at index
        within the current data set. Unless specified otherwise,
        the column index refers to the index within the original
        dataset.

        Parameters:

            index (int):
                The numerical index of the column.

            visible (bool):
                Use the index of the visible columns as they appear
                in the table.

        Returns:

            Union[TableColumn, None]:
                The table column object at index or None if no object
                exists.
        """
        if not visible:
            # original column index
            try:
                return self._tablecols[index]
            except IndexError:
                return None
        else:
            # visible column index
            cols = self.view.cget("columns")
            if len(cols) > 0:
                cols = [int(x) for x in cols]
            else:
                cols = []

            dcols = self.view.cget("displaycolumns")
            if "#all" in dcols:
                dcols = cols
            else:
                try:
                    x = int(dcols[index])
                    for c in self._tablecols:
                        if c.cid == x:
                            return c
                except ValueError:
                    return None

    def get_rows(self, visible=False, filtered=False) -> List[TableRow]:
        """Return a list of TableRow objects.
        
        Parameters:

            visible (bool):
                If true, only records in the current view will be returned.

            filtered (bool):
                If True, only rows in the filtered dataset will be returned.

        Returns:

            List[TableRow]:
                A list of TableRow objects.
        """
        if visible:
            return self._viewdata
        elif filtered:
            return self._tablerows_filtered
        else:
            return self._tablerows

    def get_row(self, index, visible=False, filtered=False):
        """Returns the `TableRow` object for the row at index
        within the current data set. Unless specified otherwise,
        the row index refers to the index within the original
        dataset.

        When choosing a subset of data, the visible data takes
        priority over filtered if both flags are set.

        Parameters:

            index (int):
                The numerical index of the column.

            visible (bool):
                Use the index of the visible rows as they appear
                in the current table view.

            filtered (bool):
                Use the index of the rows within the filtered data
                set.

        Returns:

            Union[TableRow, None]:
                The table column object at index or None if no object
                exists.
        """
        if visible:
            try:
                return self._viewdata[index]
            except IndexError:
                return None
        elif filtered:
            try:
                return self._tablerows_filtered[index]
            except IndexError:
                return None
        else:
            try:
                return self._tablerows[index]
            except IndexError:
                return None

    # PAGE NAVIGATION

    def goto_first_page(self):
        """Update table with first page of data"""
        self._rowindex.set(0)
        self.load_table_data()

    def goto_last_page(self):
        """Update table with the last page of data"""
        self._rowindex.set(self._pagesize.get() * (self._pagelimit.get() - 1))
        self.load_table_data()

    def goto_next_page(self):
        """Update table with next page of data"""
        if self._pageindex.get() >= self._pagelimit.get():
            return
        rowindex = self._rowindex.get()
        self._rowindex.set(rowindex + self._pagesize.get())
        self.load_table_data()

    def goto_prev_page(self):
        """Update table with prev page of data"""
        if self._pageindex.get() <= 1:
            return
        rowindex = self._rowindex.get()
        self._rowindex.set(rowindex - self._pagesize.get())
        self.load_table_data()

    def goto_page(self, *_):
        """Go to a specific page indicated by the page entry widget."""
        pageindex = self._pageindex.get() - 1
        self._rowindex.set(pageindex * self._pagesize.get())
        self.load_table_data()

    # COLUMN SORTING

    def sort_column_data(self, event=None, cid=None, sort=None):
        """Sort the table rows by the specified column. This method
        may be trigged by an event or manually.

        Parameters:

            event (Event):
                A window event.

            cid (int):
                A unique column identifier; typically the numerical
                index of the column relative to the original data set.

            sort (int):
                Determines the sort direction. 0 = ASCENDING. 1 = DESCENDING.
        """
        if event is not None:
            eo = self._get_event_objects(event)
            cid = eo.get("cid")
        elif cid is None:
            return

        # update table data
        if self._filtered:
            tablerows = self._tablerows_filtered
        else:
            tablerows = self._tablerows

        if sort is not None:
            colsort = sort
        else:
            colsort = self._tablecols[cid]._sort

        if colsort == ASCENDING:
            self._tablecols[cid]._sort = DESCENDING
        else:
            self._tablecols[cid]._sort = ASCENDING

        try:
            sortedrows = sorted(
                tablerows, 
                reverse=colsort, 
                key=lambda x: x._values[cid]
            )
        except IndexError:
            self.fill_empty_columns()
            sortedrows = sorted(
                tablerows, 
                reverse=colsort, 
                key=lambda x: x._values[cid]
            )            
        if self._filtered:
            self._tablerows_filtered = sortedrows
        else:
            self._tablerows = sortedrows

        # update headers
        self._column_sort_header_reset()
        self._column_sort_header_update(cid)

        self.unload_table_data()
        self.load_table_data()

    # DATA SEARCH & FILTERING

    def clear_filters(self):
        """Remove all table data filters"""
        self._filtered = False
        self._searchcriteria.set("")
        self.unload_table_data()
        self.load_table_data()
        self._column_sort_header_reset()

    def filter_column_to_value(self, event=None, cid=None, value=None):
        """Hide all records except for records where the current
        column exactly matches the provided value. This method may
        be triggered by a window event or by specifying the column id.

        Parameters:

            event (Event):
                A window click event.

            cid (int):
                A unique column identifier; typically the numerical
                index of the column within the original dataset.

            value (Any):
                The criteria used to filter the column.
        """
        if event is not None:
            eo = self._get_event_objects(event)
            cid = eo.get("cid")
            value = eo.get("value") or value
        elif cid is None:
            return
        self._filtered = True
        self._tablerows_filtered.clear()
        self.unload_table_data()
        data = self._tablerows
        for row in data:
            if row._values[cid] == value:
                self._tablerows_filtered.append(row)
        self._rowindex.set(0)
        self.load_table_data()

    def filter_to_selected_rows(self):
        """Hide all records except for the selected rows"""
        criteria = self.view.selection()
        if len(criteria) == 0:
            return  # nothing is selected

        if self._filtered:
            for row in self._viewdata:
                if row.iid not in criteria:
                    row.hide()
                    self._tablerows_filtered.remove(row)
        else:
            self._filtered = True
            self._tablerows_filtered.clear()
            for row in self._viewdata:
                if row.iid in criteria:
                    self._tablerows_filtered.append(row)
        self._rowindex.set(0)
        self.load_table_data()

    def hide_selected_rows(self):
        """Hide the currently selected rows"""
        selected = self.view.selection()
        self.view.detach(*selected)
        tablerows = [row for row in self._viewdata if row.iid in selected]

        if not self._filtered:
            self._filtered = True
            self._tablerows_filtered = self._tablerows.copy()

        for row in tablerows:
            if self._filtered:
                self._tablerows_filtered.remove(row)

        self.load_table_data()

    def hide_selected_column(self, event=None, cid=None):
        """Detach the selected column from the tableview. This method
        may be triggered by a window event or by specifying the column
        id.

        Parameters:

            event (Event):
                A window click event

            cid (int):
                A unique column identifier; typically the numerical
                index of the column within the original dataset.
        """
        if event is not None:
            eo = self._get_event_objects(event)
            cid = eo.get("cid")
        elif cid is None:
            return
        displaycols = list(self.view.configure("displaycolumns"))
        cols = list(self.view.configure("columns"))
        if "#all" in displaycols:
            displaycols = cols
        displaycols.remove(str(cid))
        self.view.configure(displaycolumns=displaycols)

    def unhide_selected_column(self, event=None, cid=None):
        """Attach the selected column to the tableview. This method
        may be triggered by a window event or by specifying the column
        id. The column is reinserted at the index in the original data
        set.

        Parameters:

            event (Event):
                An application click event

            cid (int):
                A unique column identifier; typically the numerical
                index of the column within the original dataset.
        """
        if event is not None:
            eo = self._get_event_objects(event)
            cid = eo.get("cid")
        elif cid is None:
            return
        displaycols = list(self.view.configure("displaycolumns"))
        if "#all" in displaycols:
            return
        if str(cid) in displaycols:
            return
        columns = list(self.view.configure("columns"))
        index = columns.index(str(cid))
        displaycols.insert(index, str(cid))
        self.view.configure(displaycolumns=displaycols)

    # DATA EXPORT

    def export_all_records(self):
        """Export all records to a csv file"""
        headers = [col._headertext for col in self._tablecols]
        records = [row._values for row in self._tablerows]
        self.save_data_to_csv(headers, records, self._delimiter)

    def export_current_page(self):
        """Export records on current page to csv file"""
        headers = [col._headertext for col in self._tablecols]
        records = [row._values for row in self._viewdata]
        self.save_data_to_csv(headers, records, self._delimiter)

    def export_current_selection(self):
        """Export rows currently selected to csv file"""
        headers = [col._headertext for col in self._tablecols]
        selected = self.view.selection()
        records = []
        for iid in selected:
            records.append(self.view.item(iid)["values"])
        self.save_data_to_csv(headers, records, self._delimiter)

    def export_records_in_filter(self):
        """Export rows currently filtered to csv file"""
        headers = [col._headertext for col in self._tablecols]
        if not self._filtered:
            return
        records = [row.values for row in self._tablerows_filtered]
        self.save_data_to_csv(headers, records, self._delimiter)

    def save_data_to_csv(self, headers, records, delimiter=","):
        """Save data records to a csv file.

        Parameters:

            headers (List[str]):
                A list of header labels.

            records (List[Tuple[...]]):
                A list of table records.

            delimiter (str):
                The character to use for delimiting the values.
        """
        from tkinter.filedialog import asksaveasfilename
        import csv

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        initialfile = f"tabledata_{timestamp}.csv"
        filetypes = [
            ("CSV UTF-8 (Comma delimited)", "*.csv"),
            ("All file types", "*.*"),
        ]
        filename = asksaveasfilename(
            confirmoverwrite=True,
            filetypes=filetypes,
            defaultextension="csv",
            initialfile=initialfile,
        )
        if filename:
            with open(filename, "w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f, delimiter=delimiter)
                writer.writerow(headers)
                writer.writerows(records)

    # ROW MOVEMENT

    def move_selected_rows_to_top(self):
        """Move the selected rows to the top of the data set"""
        selected = self.view.selection()
        if len(selected) == 0:
            return

        if self._filtered:
            tablerows = self._tablerows_filtered
        else:
            tablerows = self._tablerows

        row_items = []

        for iid in selected:
            for row in tablerows:
                if row.iid == iid:
                    row_items.append(row)
                    break

        for i, item in enumerate(row_items):
            tablerows.remove(item)
            tablerows.insert(i, item)

        if self._filtered:
            self._tablerows_filtered = tablerows
        else:
            self._tablerows = tablerows

        # refresh the table data
        self.unload_table_data()
        self.load_table_data()

    def move_selected_rows_to_bottom(self):
        """Move the selected rows to the bottom of the dataset"""
        selected = self.view.selection()
        if len(selected) == 0:
            return

        if self._filtered:
            tablerows = self._tablerows_filtered
        else:
            tablerows = self._tablerows

        row_items = []

        for iid in selected:
            for row in tablerows:
                if row.iid == iid:
                    row_items.append(row)
                    break

        for item in row_items:
            tablerows.remove(item)
            tablerows.append(item)

        if self._filtered:
            self._tablerows_filtered = tablerows
        else:
            self._tablerows = tablerows

        # refresh the table data
        self.unload_table_data()
        self.load_table_data()

    def move_selected_row_up(self):
        """Move the selected rows up one position in the dataset"""
        selected = self.view.selection()
        if len(selected) == 0:
            return

        if self._filtered:
            tablerows = self._tablerows_filtered
        else:
            tablerows = self._tablerows

        row_items = []

        for iid in selected:
            for i, row in enumerate(tablerows):
                if row.iid == iid:
                    row_items.append([i, row])
                    break

        for index, item in row_items:
            tablerows.remove(item)
            tablerows.insert(index - 1, item)

        if self._filtered:
            self._tablerows_filtered = tablerows
        else:
            self._tablerows = tablerows

        # refresh the table data
        self.unload_table_data()
        self.load_table_data()

    def move_row_down(self):
        """Move the selected rows down one position in the dataset"""
        selected = self.view.selection()
        if len(selected) == 0:
            return

        if self._filtered:
            tablerows = self._tablerows_filtered
        else:
            tablerows = self._tablerows

        row_items = []

        for iid in selected:
            for i, row in enumerate(tablerows):
                if row.iid == iid:
                    row_items.append([i, row])
                    break

        for index, item in reversed(row_items):
            tablerows.remove(item)
            tablerows.insert(index + 1, item)

        if self._filtered:
            self._tablerows_filtered = tablerows
        else:
            self._tablerows = tablerows

        # refresh the table data
        self.unload_table_data()
        self.load_table_data()

    # COLUMN MOVEMENT

    def move_column_left(self, event=None, cid=None):
        """Move column one position to the left. This can be triggered
        by either an event, or by passing in the `cid`, which is the
        index of the column relative to the original data set.

        Parameters:

            event (Event):
                An application click event.

            cid (int):
                A unique column identifier; typically the index of the
                column relative to the original dataset.
        """
        if event is not None:
            eo = self._get_event_objects(event)
            cid = str(eo.get("cid"))
        elif cid is None:
            return
        displaycols = list(self.view.configure("displaycolumns"))
        cols = list(self.view.configure("columns"))
        if "#all" in displaycols:
            displaycols = cols
        old_index = displaycols.index(cid)
        if old_index == 0:
            return
        new_index = old_index - 1
        displaycols.insert(new_index, displaycols.pop(old_index))
        self.view.configure(displaycolumns=displaycols)

    def move_column_right(self, event=None, cid=None):
        """Move column one position to the right. This can be triggered
        by either an event, or by passing in the `cid`, which is the
        index of the column relative to the original data set.

        Parameters:

            event (Event):
                An application click event.

            cid (int):
                A unique column identifier; typically the index of the
                column relative to the original dataset.
        """
        if event is not None:
            eo = self._get_event_objects(event)
            cid = str(eo.get("cid"))
        elif cid is None:
            return
        displaycols = list(self.view.configure("displaycolumns"))
        cols = list(self.view.configure("columns"))
        if "#all" in displaycols:
            displaycols = cols
        old_index = displaycols.index(cid)
        if old_index == len(cols) - 1:
            return
        new_index = old_index + 1
        displaycols.insert(new_index, displaycols.pop(old_index))
        self.view.configure(displaycolumns=displaycols)

    def move_column_to_first(self, event=None, cid=None):
        """Move column to leftmost position. This can be triggered by
        either an event, or by passing in the `cid`, which is the index
        of the column relative to the original data set.

        Parameters:

            event (Event):
                An application click event.

            cid (int):
                A unique column identifier; typically the index of the
                column relative to the original dataset.
        """
        if event is not None:
            eo = self._get_event_objects(event)
            cid = str(eo.get("cid"))
        elif cid is None:
            return
        displaycols = list(self.view.configure("displaycolumns"))
        cols = list(self.view.configure("columns"))
        if "#all" in displaycols:
            displaycols = cols
        old_index = displaycols.index(cid)
        if old_index == 0:
            return
        displaycols.insert(0, displaycols.pop(old_index))
        self.view.configure(displaycolumns=displaycols)

    def move_column_to_last(self, event=None, cid=None):
        """Move column to the rightmost position. This can be triggered
        by either an event, or by passing in the `cid`, which is the
        index of the column relative to the original data set.

        Parameters:

            event (Event):
                An application click event.

            cid (int):
                A unique column identifier; typically the index of the
                column relative to the original dataset.
        """
        if event is not None:
            eo = self._get_event_objects(event)
            cid = str(eo.get("cid"))
        elif cid is None:
            return
        displaycols = list(self.view.configure("displaycolumns"))
        cols = list(self.view.configure("columns"))
        if "#all" in displaycols:
            displaycols = cols
        old_index = displaycols.index(cid)
        if old_index == len(cols) - 1:
            return
        new_index = len(cols) - 1
        displaycols.insert(new_index, displaycols.pop(old_index))
        self.view.configure(displaycolumns=displaycols)

    # OTHER FORMATTING

    def apply_table_stripes(self, stripecolor):
        """Add stripes to even-numbered table rows as indicated by the
        `stripecolor` of (background, foreground). Either element may be
        specified as `None`, but both elements must be present.

        Parameters:

            stripecolor (Tuple[str, str]):
                A tuple of colors to apply to the table stripe. The
                tuple represents (background, foreground).
        """
        if len(stripecolor) == 2:
            self._stripecolor = stripecolor
            bg, fg = stripecolor
            kw = {}
            if bg is not None:
                kw["background"] = bg
            if fg is not None:
                kw["foreground"] = fg
            self.view.tag_configure("striped", **kw)

    def autofit_columns(self):
        """Autofit all columns in the current view"""
        f = font.nametofont("TkDefaultFont")
        pad = utility.scale_size(self, 20)
        col_widths = []

        # measure header sizes
        for col in self._tablecols:
            width = f.measure(f"{col._headertext} {DOWNARROW}") + pad
            col_widths.append(width)

        for row in self._viewdata:
            values = row._values
            for i, value in enumerate(values):
                old_width = col_widths[i]
                new_width = f.measure(str(value)) + pad
                width = max(old_width, new_width)
                col_widths[i] = width

        for i, width in enumerate(col_widths):
            self.view.column(i, width=width)

    # COLUMN AND HEADER ALIGNMENT

    def autoalign_columns(self):
        """Align the columns and headers based on the data type of the
        values. Text is left-aligned; numbers are right-aligned. This
        method will have no effect if there is no data in the tables."""
        if len(self._tablerows) == 0:
            return
        values = self._tablerows[0]._values
        for i, value in enumerate(values):
            if str(value).isnumeric():
                self.view.column(i, anchor=E)
                self.view.heading(i, anchor=E)
            else:
                self.view.column(i, anchor=W)
                self.view.heading(i, anchor=W)

    def align_column_left(self, event=None, cid=None):
        """Left align the column text. This can be triggered by
        either an event, or by passing in the `cid`, which is the index
        of the column relative to the original data set.

        Parameters:

            event (Event):
                An application click event.

            cid (int):
                A unique column identifier; typically the index of the
                column relative to the original dataset.
        """
        if event is not None:
            eo = self._get_event_objects(event)
            cid = eo.get("cid")
        elif cid is None:
            return
        self.view.column(cid, anchor=W)

    def align_column_right(self, event=None, cid=None):
        """Right align the column text. This can be triggered by
        either an event, or by passing in the `cid`, which is the index
        of the column relative to the original data set.

        Parameters:

            event (Event):
                An application event.

            cid (int):
                A unique column identifier; typically the index of the
                column relative to the original dataset.
        """
        if event is not None:
            eo = self._get_event_objects(event)
            cid = eo.get("cid")
        elif cid is None:
            return
        self.view.column(cid, anchor=E)

    def align_column_center(self, event=None, cid=None):
        """Center align the column text. This can be triggered by
        either an event, or by passing in the `cid`, which is the index
        of the column relative to the original data set.

        Parameters:

            event (Event):
                An application event.

            cid (int):
                A unique column identifier; typically the index of the
                column relative to the original dataset.
        """
        if event is not None:
            eo = self._get_event_objects(event)
            cid = eo.get("cid")
        elif cid is None:
            return
        self.view.column(cid, anchor=CENTER)

    def align_heading_left(self, event=None, cid=None):
        """Left align the heading text. This can be triggered by
        either an event, or by passing in the `cid`, which is the index
        of the heading relative to the original data set.

        Parameters:

            event (Event):
                An application event.

            cid (int):
                A unique heading identifier; typically the index of the
                heading relative to the original dataset.
        """
        if event is not None:
            eo = self._get_event_objects(event)
            cid = eo.get("cid")
        elif cid is None:
            return
        self.view.heading(cid, anchor=W)

    def align_heading_right(self, event=None, cid=None):
        """Right align the heading text. This can be triggered by
        either an event, or by passing in the `cid`, which is the index
        of the heading relative to the original data set.

        Parameters:

            event (Event):
                An application event.

            cid (int):
                A unique heading identifier; typically the index of the
                heading relative to the original dataset.
        """
        if event is not None:
            eo = self._get_event_objects(event)
            cid = eo.get("cid")
        elif cid is None:
            return
        self.view.heading(cid, anchor=E)

    def align_heading_center(self, event=None, cid=None):
        """Center align the heading text. This can be triggered by
        either an event, or by passing in the `cid`, which is the index
        of the heading relative to the original data set.

        Parameters:

            event (Event):
                An application event.

            cid (int):
                A unique heading identifier; typically the index of the
                heading relative to the original dataset.
        """
        if event is not None:
            eo = self._get_event_objects(event)
            cid = eo.get("cid")
        elif cid is None:
            return
        self.view.heading(cid, anchor=CENTER)

    # PRIVATE METHODS

    def _get_event_objects(self, event):
        iid = self.view.identify_row(event.y)
        item = self.view.item(iid)
        col = self.view.identify_column(event.x)
        cid = int(self.view.column(col, "id"))
        values = item.get("values")
        data = {
            "iid": iid,
            "cid": cid,
            "col": col,
            "item": item,
            "values": values,
        }
        if values:
            data["value"] = values[cid]
        return data

    def _search_table_data(self, _):
        """Search the table data for records that meet search criteria.
        Currently, this search locates any records that contain the
        specified text; it is also case insensitive.
        """
        criteria = self._searchcriteria.get()
        self._filtered = True
        self._tablerows_filtered.clear()
        self.unload_table_data()
        data = self._tablerows
        for row in data:
            for col in row._values:
                if str(criteria).lower() in str(col).lower():
                    self._tablerows_filtered.append(row)
                    break
        self._rowindex.set(0)
        self.load_table_data()        
    
    # PRIVATE METHODS - SORTING

    def _column_sort_header_reset(self):
        """Remove the sort character from the column headers"""
        for col in self._tablecols:
            self.view.heading(col.cid, text=col._headertext)

    def _column_sort_header_update(self, cid):
        """Add sort character to the sorted column"""
        col = self._tablecols[cid]
        arrow = UPARROW if col._sort == ASCENDING else DOWNARROW
        headertext = f"{col._headertext} {arrow}"
        self.view.heading(col.cid, text=headertext)        

    # PRIVATE METHODS - WIDGET BUILDERS

    def _build_table(self, coldata, rowdata, bootstyle):
        """Build the data table"""
        if self._searchable:
            self._build_search_frame()

        self.view = ttk.Treeview(
            master=self,
            columns=[x for x in range(len(coldata))],
            height=self._height,
            selectmode=EXTENDED,
            show=HEADINGS,
            bootstyle=f"{bootstyle}-table",
        )
        self.view.pack(fill=BOTH, expand=YES, side=TOP)
        self.hbar = ttk.Scrollbar(
            master=self, command=self.view.xview, orient=HORIZONTAL
        )
        self.hbar.pack(fill=X)
        self.view.configure(xscrollcommand=self.hbar.set)

        self._build_table_columns(coldata)
        self._build_table_rows(rowdata)
        # self.build_horizontal_scrollbar()

        self.load_table_data()

        if self._autofit:
            self.autofit_columns()

        if self._autoalign:
            self.autoalign_columns()

        if self._paginated:
            self._build_pagination_frame()

        if self._stripecolor is not None:
            self.apply_table_stripes(self._stripecolor)

        self._rightclickmenu_cell = TableCellRightClickMenu(self)
        self.rightclickmenu_head = TableHeaderRightClickMenu(self)
        self._set_widget_binding()

    def _build_search_frame(self):
        """Build the search frame containing the search widgets. This
        frame is only created if `searchable=True` when creating the
        widget.
        """
        frame = ttk.Frame(self, padding=5)
        frame.pack(fill=X, side=TOP)
        ttk.Label(frame, text="Search").pack(side=LEFT, padx=5)
        searchterm = ttk.Entry(frame, textvariable=self._searchcriteria)
        searchterm.pack(fill=X, side=LEFT, expand=YES)
        searchterm.bind("<Return>", self._search_table_data)
        searchterm.bind("<KP_Enter>", self._search_table_data)
        ttk.Button(
            frame,
            text="⎌",
            command=self.clear_filters,
            style="symbol.Link.TButton",
        ).pack(side=LEFT)

    def _build_pagination_frame(self):
        """Build the frame containing the pagination widgets. This
        frame is only built if `pagination=True` when creating the
        widget.
        """
        pageframe = ttk.Frame(self)
        pageframe.pack(fill=X, anchor=N)

        ttk.Button(
            master=pageframe,
            text="»",
            command=self.goto_last_page,
            style="symbol.Link.TButton",
        ).pack(side=RIGHT, fill=Y)
        ttk.Button(
            master=pageframe,
            text="›",
            command=self.goto_next_page,
            style="symbol.Link.TButton",
        ).pack(side=RIGHT, fill=Y)

        ttk.Separator(pageframe, orient=VERTICAL).pack(side=RIGHT)
        lbl = ttk.Label(pageframe, textvariable=self._pagelimit)
        lbl.pack(side=RIGHT, padx=(0, 5))
        ttk.Label(pageframe, text="of").pack(side=RIGHT, padx=(5, 0))

        index = ttk.Entry(pageframe, textvariable=self._pageindex, width=4)
        index.pack(side=RIGHT)
        index.bind("<Return>", self.goto_page, "+")
        index.bind("<KP_Enter>", self.goto_page, "+")

        ttk.Label(pageframe, text="Page").pack(side=RIGHT, padx=5)
        ttk.Separator(pageframe, orient=VERTICAL).pack(side=RIGHT)

        ttk.Button(
            master=pageframe,
            text="‹",
            command=self.goto_prev_page,
            style="symbol.Link.TButton",
        ).pack(side=RIGHT, fill=Y)
        ttk.Button(
            master=pageframe,
            text="«",
            command=self.goto_first_page,
            style="symbol.Link.TButton",
        ).pack(side=RIGHT, fill=Y)

        ttk.Label(pageframe, text="Pagesize").pack(side=LEFT, padx=5, fill=Y)
        values = [5, 10, 25, 50, 75, 100]
        cbo = ttk.Combobox(
            master=pageframe,
            values=values,
            textvariable=self._pagesize,
            width=4,
            state=READONLY,
        )
        cbo.pack(side=LEFT)
        cbo.bind("<<ComboboxSelected>>", self._select_pagesize)

    def _build_table_rows(self, rowdata):
        """Build, load, and configure the DataTableRow objects

        Parameters:

            rowdata (List):
                An iterable of row data
        """
        for row in rowdata:
            self.insert_row(END, row)

    def _build_table_columns(self, coldata):
        """Build, load, and configure the DataTableColumn objects

        Parameters:

            coldata (List[str|Dict[str, Any]]):
                An iterable of column names or a dictionary of column
                configuration settings.
        """
        for cid, col in enumerate(coldata):
            if isinstance(col, str):
                self._tablecols.append(
                    TableColumn(
                        view=self.view,
                        cid=cid,
                        text=col,
                    )
                )
            else:
                if "text" not in col:
                    col["text"] = f"Column {cid}"
                self._tablecols.append(
                    TableColumn(
                        view=self.view,
                        cid=cid,
                        **col,
                    )
                )        

    # PRIVATE METHODS - WIDGET BINDING

    def _set_widget_binding(self):
        """Setup the widget binding"""
        self.view.bind("<Double-Button-1>", self._header_double_leftclick)
        self.view.bind("<Button-1>", self._header_leftclick)
        if self.tk.call("tk", "windowingsystem") == "aqua":
            sequence = "<Button-2>"
        else:
            sequence = "<Button-3>"
        self.view.bind(sequence, self._table_rightclick)

        # add trace to track pagesize changes
        # self.pagesize.trace_add('write', self._trace_pagesize)

    def _select_pagesize(self, event):
        cbo: ttk.Combobox = self.nametowidget(event.widget)
        cbo.select_clear()
        self.goto_first_page()

    def _trace_pagesize(self, *_):
        """Callback for changes to page size"""
        # pagesize = self.pagesize.get()
        # self.tableview.configure(height=pagesize)
        self.goto_first_page()

    def _header_double_leftclick(self, event):
        """Callback for double-click events on the tableview header"""
        region = self.view.identify_region(event.x, event.y)
        if region == "separator":
            self.autofit_columns()

    def _header_leftclick(self, event):
        """Callback for left-click events"""
        region = self.view.identify_region(event.x, event.y)
        if region == "heading":
            # col = self.tableview.identify_column(event.x)
            # cid = int(self.tableview.column(col, "id"))
            self.sort_column_data(event)

    def _table_rightclick(self, event):
        """Callback for right-click events"""
        region = self.view.identify_region(event.x, event.y)
        if region == "heading":
            self.rightclickmenu_head.post(event)
        elif region != "separator":
            self._rightclickmenu_cell.post(event)


class TableCellRightClickMenu(tk.Menu):
    """A right-click menu object for the tableview cells - INTERNAL"""

    def __init__(self, master: Tableview):
        """
        Parameters:

            master (Tableview):
                The parent object
        """
        super().__init__(master, tearoff=False)
        self.master: Tableview = master
        self.view: ttk.Treeview = master.view
        self.cid = None
        self.iid = None

        config = {
            "sortascending": {
                "label": "⬆  Sort Ascending",
                "command": self.sort_column_ascending,
            },
            "sortdescending": {
                "label": "⬇  Sort Descending",
                "command": self.sort_column_descending,
            },
            "clearfilter": {
                "label": "⎌ Clear filters",
                "command": self.master.clear_filters,
            },
            "filterbyvalue": {
                "label": "Filter by cell's value",
                "command": self.filter_to_cell_value,
            },
            "hiderows": {
                "label": "Hide select rows",
                "command": self.hide_selected_rows,
            },
            "showrows": {
                "label": "Show only select rows",
                "command": self.filter_to_selected_rows,
            },
            "exportall": {
                "label": "Export all records",
                "command": self.export_all_records,
            },
            "exportpage": {
                "label": "Export current page",
                "command": self.export_current_page,
            },
            "exportselection": {
                "label": "Export current selection",
                "command": self.export_current_selection,
            },
            "exportfiltered": {
                "label": "Export records in filter",
                "command": self.export_records_in_filter,
            },
            "moveup": {"label": "↑ Move up", "command": self.move_row_up},
            "movedown": {
                "label": "↓ Move down",
                "command": self.move_row_down,
            },
            "movetotop": {
                "label": "⤒ Move to top",
                "command": self.move_row_to_top,
            },
            "movetobottom": {
                "label": "⤓ Move to bottom",
                "command": self.move_row_to_bottom,
            },
            "alignleft": {
                "label": "◧  Align left",
                "command": self.align_column_left,
            },
            "aligncenter": {
                "label": "◫  Align center",
                "command": self.align_column_center,
            },
            "alignright": {
                "label": "◨  Align right",
                "command": self.align_column_right,
            },
        }
        sort_menu = tk.Menu(self, tearoff=False)
        sort_menu.add_command(cnf=config["sortascending"])
        sort_menu.add_command(cnf=config["sortdescending"])
        self.add_cascade(menu=sort_menu, label="⇅ Sort")

        filter_menu = tk.Menu(self, tearoff=False)
        filter_menu.add_command(cnf=config["clearfilter"])
        filter_menu.add_separator()
        filter_menu.add_command(cnf=config["filterbyvalue"])
        filter_menu.add_command(cnf=config["hiderows"])
        filter_menu.add_command(cnf=config["showrows"])
        self.add_cascade(menu=filter_menu, label="⧨  Filter")

        export_menu = tk.Menu(self, tearoff=False)
        export_menu.add_command(cnf=config["exportall"])
        export_menu.add_command(cnf=config["exportpage"])
        export_menu.add_command(cnf=config["exportselection"])
        export_menu.add_command(cnf=config["exportfiltered"])
        self.add_cascade(menu=export_menu, label="↔  Export")

        move_menu = tk.Menu(self, tearoff=False)
        move_menu.add_command(cnf=config["moveup"])
        move_menu.add_command(cnf=config["movedown"])
        move_menu.add_command(cnf=config["movetotop"])
        move_menu.add_command(cnf=config["movetobottom"])
        self.add_cascade(menu=move_menu, label="⇵  Move")

        align_menu = tk.Menu(self, tearoff=False)
        align_menu.add_command(cnf=config["alignleft"])
        align_menu.add_command(cnf=config["aligncenter"])
        align_menu.add_command(cnf=config["alignright"])
        self.add_cascade(menu=align_menu, label="↦  Align")

    def post(self, event):
        """Display the menu below the selected cell.

        Parameters:

            event (Event):
                The click event that triggers menu.
        """
        # capture the column and item that invoked the menu
        self.event = event
        iid = self.view.identify_row(event.y)
        col = self.view.identify_column(event.x)

        # show the menu below the invoking cell
        rootx = self.view.winfo_rootx()
        rooty = self.view.winfo_rooty()
        bbox = self.view.bbox(iid, col)
        try:
            super().post(rootx + bbox[0], rooty + bbox[1] + bbox[3])
        except IndexError:
            pass

    def sort_column_ascending(self):
        """Sort the column in ascending order."""
        self.master.sort_column_data(self.event, sort=ASCENDING)

    def sort_column_descending(self):
        """Sort the column in descending order."""
        self.master.sort_column_data(self.event, sort=DESCENDING)

    def filter_to_cell_value(self):
        """Hide all records except for records where the current
        column exactly matches the current cell value."""
        self.master.filter_column_to_value(self.event)

    def filter_to_selected_rows(self):
        """Hide all records except for the selected rows."""
        self.master.filter_to_selected_rows()

    def export_all_records(self):
        """Export all records to a csv file"""
        self.master.export_all_records()

    def export_current_page(self):
        """Export records on current page"""
        self.master.export_current_page()

    def export_current_selection(self):
        """Export rows currently selected"""
        self.master.export_current_selection()

    def export_records_in_filter(self):
        """Export rows currently filtered"""
        self.master.export_records_in_filter()

    def hide_selected_rows(self):
        """Hide the selected rows"""
        self.master.hide_selected_rows()

    def move_row_to_top(self):
        """Move the row to the top of the data set"""
        self.master.move_selected_rows_to_top()

    def move_row_to_bottom(self):
        """Move the row to the bottom of the dataset"""
        self.master.move_selected_rows_to_bottom()

    def move_row_up(self):
        """Move the selected above the previous sibling"""
        self.master.move_selected_row_up()

    def move_row_down(self):
        """Move the selected row below the next sibling"""
        self.master.move_row_down()

    def align_column_left(self):
        "Left align the column text"
        self.master.align_column_left(self.event)

    def align_column_right(self):
        """Right align the column text"""
        self.master.align_column_right(self.event)

    def align_column_center(self):
        """Center align the column text"""
        self.master.align_column_center(self.event)


class TableHeaderRightClickMenu(tk.Menu):
    """A right-click menu object for the tableview header - INTERNAL"""

    def __init__(self, master: Tableview):
        """
        Parameters:

            master (Tableview):
                The parent object
        """
        super().__init__(master, tearoff=False)
        self.master: Tableview = self.master
        self.view: ttk.Treeview = master.view
        self.event = None

        # HIDE & SHOW
        show_menu = tk.Menu(self, tearoff=False)
        for column in self.master._tablecols:
            variable = f"column_{column.cid}"
            self.view.setvar(variable, True)
            show_menu.add_checkbutton(
                label=column._headertext,
                command=lambda w=column: self.toggle_columns(w.cid),
                variable=variable,
                indicatoron=True,
                onvalue=True,
                offvalue=False,
            )
        self.add_cascade(menu=show_menu, label="±  Columns")

        config = {
            "movetoright": {
                "label": "→  Move to right",
                "command": self.move_column_right,
            },
            "movetoleft": {
                "label": "←  Move to left",
                "command": self.move_column_left,
            },
            "movetofirst": {
                "label": "⇤  Move to first",
                "command": self.move_column_to_first,
            },
            "movetolast": {
                "label": "⇥  Move to last",
                "command": self.move_column_to_last,
            },
            "alignleft": {
                "label": "◧  Align left",
                "command": self.align_heading_left,
            },
            "alignright": {
                "label": "◨  Align right",
                "command": self.align_heading_right,
            },
            "aligncenter": {
                "label": "◫  Align center",
                "command": self.align_heading_center,
            },
            "resettable": {
                "label": "⎌  Reset Table",
                "command": self.master.clear_filters
            }
        }

        # MOVE MENU
        move_menu = tk.Menu(self, tearoff=False)
        move_menu.add_command(cnf=config["movetoleft"])
        move_menu.add_command(cnf=config["movetoright"])
        move_menu.add_command(cnf=config["movetofirst"])
        move_menu.add_command(cnf=config["movetolast"])
        self.add_cascade(menu=move_menu, label="⇄  Move")

        align_menu = tk.Menu(self, tearoff=False)
        align_menu.add_command(cnf=config["alignleft"])
        align_menu.add_command(cnf=config["aligncenter"])
        align_menu.add_command(cnf=config["alignright"])
        self.add_cascade(menu=align_menu, label="↦  Align")

        self.add_command(cnf=config["resettable"])

    def post(self, event):
        # capture the column and item that invoked the menu
        self.event = event

        # show the menu below the invoking cell
        rootx = self.view.winfo_rootx()
        rooty = self.view.winfo_rooty()
        super().post(rootx + event.x, rooty + event.y + 10)

    def toggle_columns(self, cid):
        """Toggles the visibility of the selected column"""
        variable = f"column_{cid}"
        toggled = self.getvar(variable)
        if toggled:
            self.master.unhide_selected_column(cid=cid)
        else:
            self.master.hide_selected_column(cid=cid)

    def move_column_left(self):
        """Move column one position to the left"""
        self.master.move_column_left(self.event)

    def move_column_right(self):
        """Move column on position to the right"""
        self.master.move_column_right(self.event)

    def move_column_to_first(self):
        """Move column to leftmost position"""
        self.master.move_column_to_first(self.event)

    def move_column_to_last(self):
        """Move column to rightmost position"""
        self.master.move_column_to_last(self.event)

    def align_heading_left(self):
        """Left align the column header"""
        self.master.align_heading_left(self.event)

    def align_heading_right(self):
        """Right align the column header"""
        self.master.align_heading_right(self.event)

    def align_heading_center(self):
        """Center align the column header"""
        self.master.align_heading_center(self.event)
