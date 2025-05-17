import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from math import ceil
from datetime import datetime
from tkinter import font
from ttkbootstrap import utility
from typing import Any, Dict, List, Union
from ttkbootstrap.localization import MessageCatalog

UPARROW = "⬆"
DOWNARROW = "⬇"
ASCENDING = 0
DESCENDING = 1


class TableColumn:
    """Represents a column in a Tableview object"""

    def __init__(
            self,
            tableview,
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

            tableview (Tableview):
                The parent tableview object.

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
        self._table = tableview
        self._cid = cid
        self._headertext = text
        self._sort = ASCENDING
        self._settings_column = {}
        self._settings_heading = {}

        self.view: ttk.Treeview = tableview.view
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
        self._table._cidmap[self._cid] = self

    @property
    def headertext(self):
        """The text on the header label"""
        return self._headertext

    @property
    def columnsort(self):
        """Indicates how the column is to be sorted when the sorting
        method is invoked."""
        return self._sort

    @columnsort.setter
    def columnsort(self, value):
        self._sort = value

    @property
    def cid(self):
        """A unique column identifier"""
        return str(self._cid)

    @property
    def tableindex(self):
        """The index of the column as it is in the table configuration."""
        cols = self.view.cget("columns")
        if cols is None:
            return
        try:
            return cols.index(self.cid)
        except IndexError:
            return

    @property
    def displayindex(self):
        """The index of the column as it is displayed"""
        cols = self.view.cget("displaycolumns")
        if "#all" in cols:
            return self.tableindex
        else:
            return cols.index(self.cid)

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
                return self.view.column(self.cid, opt)
            elif opt in ("command", "text", "image"):
                return self.view.heading(self.cid, opt)
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
        displaycols = list(self.view.cget("displaycolumns"))
        if "#all" in displaycols:
            return
        if self.cid in displaycols:
            return
        columns = list(self.view.cget("columns"))
        index = columns.index(self.cid)
        displaycols.insert(index, self.cid)
        self.view.configure(displaycolumns=displaycols)

    def hide(self):
        """Hide the column in the tableview"""
        displaycols = list(self.view.cget("displaycolumns"))
        cols = list(self.view.cget("columns"))
        if "#all" in displaycols:
            displaycols = cols
        displaycols.remove(self.cid)
        self.view.configure(displaycolumns=displaycols)

    def delete(self):
        """Remove the column from the tableview permanently."""
        # update the tablerow columns
        index = self.tableindex
        if index is None:
            return

        for row in self._table.tablerows:
            row.values.pop(index)
            row.refresh()

        # actual columns
        cols = list(self.view.cget("columns"))
        cols.remove(self.cid)
        self._table.tablecolumns.remove(self)

        # visible columns
        dcols = list(self.view.cget("displaycolumns"))
        if "#all" in dcols:
            dcols = cols
        else:
            dcols.remove(self.cid)

        # remove cid mapping
        self._table.cidmap.pop(self._cid)

        # reconfigure the tableview column and displaycolumns
        self.view.configure(columns=cols, displaycolumns=dcols)

        # remove the internal object references
        for i, column in enumerate(self._table.tablecolumns):
            if column.cid == self.cid:
                self._table.tablecolumns.pop(i)
            else:
                column.restore_settings()

    def restore_settings(self):
        """Update the configuration based on stored settings"""
        self.view.column(self.cid, **self._settings_column)
        self.view.heading(self.cid, **self._settings_heading)

    def _capture_settings(self):
        """Update the stored settings for the column and heading.
        This is required because the settings are erased whenever
        the `columns` parameter is configured in the underlying
        Treeview widget."""
        self._settings_heading = self.view.heading(self.cid)
        self._settings_heading.pop("state")
        self._settings_column = self.view.column(self.cid)
        self._settings_column.pop("id")


class TableRow:
    """Represents a row in a Tableview object"""

    _cnt = 0

    def __init__(self, tableview, values):
        """
        Parameters:

            tableview (Tableview):
                The Tableview widget that contains this row

            values (List[Any, ...]):
                A list of values to display in the row
        """
        self.view: ttk.Treeview = tableview.view
        self._values = list(values)
        self._iid = None
        self._sort = TableRow._cnt + 1
        self._table = tableview

        # increment cnt
        TableRow._cnt += 1

    @property
    def values(self):
        """The table row values"""
        return self._values

    @values.setter
    def values(self, values):
        self._values = values
        self.refresh()

    @property
    def iid(self):
        """A unique record identifier"""
        return str(self._iid)

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
        elif 'values' in kwargs:
            values = kwargs.pop('values')
            self.values = values
        else:
            self.view.item(self.iid, **kwargs)

    def show(self, striped=False):
        """Show the row in the data table view"""
        if self._iid is None:
            self.build()
        self.view.reattach(self.iid, "", END)

        # remove existing stripes
        tags = list(self.view.item(self.iid, "tags"))
        try:
            tags.remove("striped")
        except ValueError:
            pass

        # add stripes (if needed)
        if striped:
            tags.append("striped")
        self.view.item(self.iid, tags=tags)

    def delete(self):
        """Delete the row from the dataset"""
        if self.iid:
            self._table.iidmap.pop(self.iid)
            self._table.tablerows_visible.remove(self)
            self._table._tablerows.remove(self)
            self._table.load_table_data()
            self.view.delete(self.iid)

    def hide(self):
        """Remove the row from the data table view"""
        self.view.detach(self.iid)

    def refresh(self):
        """Syncs the tableview values with the object values"""
        if self._iid:
            self.view.item(self.iid, values=self.values)

    def build(self):
        """Create the row object in the `Treeview` and capture
        the resulting item id (iid).
        """
        if self._iid is None:
            self._iid = self.view.insert("", END, values=self.values)
            self._table.iidmap[self.iid] = self


class TableEvent:
    """A container class for holding table event objects"""

    def __init__(self, column: TableColumn, row: TableRow):
        self.column = column
        self.row = row


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
        from ttkbootstrap.tableview import Tableview
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

        dt = Tableview(
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
            yscrollbar=False,
            autofit=False,
            autoalign=True,
            stripecolor=None,
            pagesize=10,
            height=10,
            delimiter=",",
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
                
            yscrollbar (bool):
                If `True`, a vertical scrollbar will be created to the right
                of the table.

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
        self._yscrollbar = yscrollbar
        self._stripecolor = stripecolor
        self._autofit = autofit
        self._autoalign = autoalign
        self._filtered = False
        self._sorted = False
        self._searchcriteria = tk.StringVar()
        self._rightclickmenu_cell = None
        self._delimiter = delimiter
        self._iidmap = {}  # maps iid to row object
        self._cidmap = {}  # maps cid to col object

        self.view: ttk.Treeview = None
        self._build_tableview_widget(coldata, rowdata, bootstyle)

    @property
    def tablerows(self):
        """A list of all tablerow objects"""
        return self._tablerows

    @property
    def tablerows_filtered(self):
        """A list of filtered tablerow objects"""
        return self._tablerows_filtered

    @property
    def tablerows_visible(self):
        """A list of visible tablerow objects"""
        return self._viewdata

    @property
    def tablecolumns(self):
        """A list of table column objects"""
        return self._tablecols

    @property
    def tablecolumns_visible(self):
        """A list of visible table column objects"""
        cids = list(self.view.cget("displaycolumns"))
        if "#all" in cids:
            return self._tablecols
        columns = []
        for cid in cids:
            # the cidmap expects an integer
            columns.append(self.cidmap.get(int(cid)))
        return columns

    @property
    def is_filtered(self):
        """Indicates whether the table is currently filtered"""
        return self._filtered

    @property
    def searchcriteria(self):
        """The criteria used to filter the records when the search
        method is invoked"""
        return self._searchcriteria.get()

    @searchcriteria.setter
    def searchcriteria(self, value):
        self._searchcriteria.set(value)

    @property
    def pagesize(self):
        """The number of records visible on a single page"""
        return self._pagesize.get()

    @pagesize.setter
    def pagesize(self, value):
        self._pagesize.set(value)

    @property
    def iidmap(self) -> Dict[str, TableRow]:
        """A map of iid to tablerow object"""
        return self._iidmap

    @property
    def cidmap(self) -> Dict[str, TableColumn]:
        """A map of cid to tablecolumn object"""
        return self._cidmap

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
            if "pagesize" in kwargs:
                pagesize: int = kwargs.pop("pagesize")
                self._pagesize.set(value=pagesize)

            self.view.configure(cnf, **kwargs)
        except:
            super().configure(cnf, **kwargs)

    # DATA HANDLING

    def build_table_data(self, coldata, rowdata):
        """Insert the specified column and row data.

        The coldata can be either a string column name or a dictionary
        of column settings that are passed to the `insert_column`
        method. You may use a mixture of string and dictionary in
        the list of coldata.

        !!!warning "Existing table data will be erased.
            This method will completely rebuild the underlying table
            with the new column and row data. Any existing data will
            be lost.

        Parameters:

            coldata (List[Union[str, Dict]]):
                An iterable of column names and/or settings.

            rowdata (List):
                An iterable of row values.
        """
        # destroy the existing data if existing
        self.purge_table_data()

        # build the table columns
        for i, col in enumerate(coldata):
            if isinstance(col, str):
                # just a column name
                self.insert_column(i, col)
            else:
                # a dictionary of column settings
                self.insert_column(i, **col)

        # build the table rows
        for values in rowdata:
            self.insert_row(values=values)

        # load the table data
        self.load_table_data()

        # apply table formatting
        if self._autofit:
            self.autofit_columns()

        if self._autoalign:
            self.autoalign_columns()

        if self._stripecolor is not None:
            self.apply_table_stripes(self._stripecolor)

        self.goto_first_page()

    def insert_row(self, index=END, values=[]) -> TableRow:
        """Insert a row into the tableview at index.

        Inserting a row will reload the table data and clear the applied filters.

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
            print('[TableView] Cannot insert. No values found.')
            return None
        if index == END:
            index = -1
        elif index > rowcount - 1:
            index = -1

        record = TableRow(self, values)
        if rowcount == 0 or index == -1:
            self._tablerows.append(record)
        else:
            self._tablerows.insert(index, record)

        self.load_table_data(self.is_filtered)

        return record

    def insert_rows(self, index, rowdata):
        """Insert row after index for each row in *row. If index does
        not exist then the records are appended to the end of the table.
        You can also use the string 'end' to append records at the end
        of the table.

        Rows are inserted in reverse order.

        Inserting rows will rebuild the table view and clear the filters.

        Parameters:

            index (Union[int, str]):
                The location in the data set after where the records
                will be inserted. You may use a numerical index or
                the string 'end', which will append the records to the
                end of the data set.

            rowdata (List[Any, List]):
                A list of row values to be inserted into the table.

        Examples:

            ```python
            Tableview.insert_rows('end', ['one', 1], ['two', 2])
            ```
        """
        if len(rowdata) == 0:
            return
        for values in reversed(rowdata):
            self.insert_row(index, values)

    def delete_column(self, index=None, cid=None, visible=True):
        """Delete the specified column based on the column index or the
        unique cid.

        Unless otherwise specified, the index refers to the column index
        as displayed in the tableview.

        If cid is provided, the column associated with the cid is deleted
        regardless of whether it is in the visible data sets.

        Parameters:

            index (int):
                The numerical index of the column.

            cid (str):
                A unique column indentifier.

            visible (bool):
                Specifies that the index should refer to the visible
                columns. Otherwise, if False, the original column
                position is used.
        """
        if cid is not None:
            column: TableColumn = self.cidmap(int(cid))
            column.delete()

        elif index is not None and visible:
            self.tablecolumns_visible[int(index)].delete()

        elif index is None and not visible:
            self.tablecolumns[int(index)].delete()

    def delete_columns(self, indices=None, cids=None, visible=True):
        """Delete columns specified by indices or cids.

        Unless specified otherwise, the index refers to the position
        of the columns in the table from left to right starting with
        index 0.

        !!!Warning "Use this method with caution!
            This method may or may not suffer performance issues.
            Internally, this method calls the `delete_column` method
            on each column specified in the list. The `delete_column`
            method deletes the related column from each record in
            the table data. So, if there are a lot of records this
            could be problematic. It may be more beneficial to use
            the `build_table_data` if you plan on changing the
            structure of the table dramatically.

        Parameters:

            indices (List[int]):
                A list of column indices to delete from the table.

            cids (List[str]):
                A list of unique column identifiers to delete from the
                table.

            visible (bool):
                If True, the index refers to the visible position of the
                column in the stable, from left to right starting at
                index 0.
        """
        if cids is not None:
            for cid in cids:
                self.delete_column(cid=cid)
        elif indices is not None:
            for index in indices:
                self.delete_column(index=index, visible=visible)

    def delete_row(self, index=None, iid=None, visible=True):
        """Delete a record from the data set.

        Unless specified otherwise, the index refers to the record
        position within the visible data set from top to bottom
        starting with index 0.

        If iid is provided, the record associated with the cid is deleted
        regardless of whether it is in the visible data set.

        Parameters:

            index (int):
                The numerical index of the record within the data set.

            iid (str):
                A unique record identifier.

            visible (bool):
                Indicates that the record index is relative to the current
                records in view, otherwise, the original data set index is
                used if False.
        """
        # delete from iid
        if iid is not None:
            record: TableRow = self.iidmap.get(iid)
            record.delete()
        elif index is not None:
            # visible index
            if visible:
                record = self.tablerows_visible[index]
                record.delete()
            # original index
            else:
                for record in self.tablerows:
                    if record._sort == index:
                        record.delete()

    def delete_rows(self, indices=None, iids=None, visible=True):
        """Delete rows specified by indices or iids.

        If both indices and iids are None, then all records in the
        table will be deleted.
        """
        # remove records by iid
        if iids is not None:
            for iid in iids:
                self.delete_row(iid=iid)
        # remove records by index
        elif indices is not None:
            for index in indices:
                self.delete_row(index=index, visible=visible)
        # remove ALL records
        else:
            self._tablerows.clear()
            self._tablerows_filtered.clear()
            self._viewdata.clear()
            self._iidmap.clear()
            records = self.view.get_children()
            self.view.delete(*records)
        # route to new page if no records visible
        if len(self._viewdata) == 0:
            self.goto_page()

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
        self.reset_table()
        colcount = len(self.tablecolumns)
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
            tableview=self,
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

    def purge_table_data(self):
        """Erase all table and column data.

        This method will completely destroy the table data structure.
        The table will need to be completely rebuilt after using this
        method.
        """
        self.delete_rows()
        self.cidmap.clear()
        self.tablecolumns.clear()
        self.view.configure(columns=[], displaycolumns=[])

    def unload_table_data(self):
        """Unload all data from the table"""
        for row in self.tablerows_visible:
            tmp_row_id = row.iid
            for tmp in self._tablerows:
                if tmp_row_id == tmp.iid:
                    row.hide()
        self.tablerows_visible.clear()

    def load_table_data(self, clear_filters=False):
        """Load records into the tableview.

        Parameters:

            clear_filters (bool):
                Specifies that the table filters should be cleared
                before loading the data into the view.
        """
        if len(self.tablerows) == 0:
            return

        if clear_filters:
            self.reset_table()

        self.unload_table_data()

        if self._paginated:
            page_start = self._rowindex.get()
            page_end = self._rowindex.get() + self._pagesize.get()
        else:
            page_start = 0
            page_end = len(self._tablerows)

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

    def fill_empty_columns(self, fillvalue=""):
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
        """Returns a list of all column objects. Same as using the
        `Tableview.tablecolumns` property."""
        return self._tablecols

    def get_column(
            self, index=None, visible=False, cid=None
    ) -> TableColumn:
        """Returns the `TableColumn` object from an index or a cid.

        If index is specified, the column index refers to the index
        within the original, unless the visible flag is set, in which
        case the index is relative to the visible columns in view.

        If cid is specified, the column associated with the cid is
        return regardless of whether it is visible.

        Parameters:

            index (int):
                The numerical index of the column.

            visible (bool):
                Use the index of the visible columns as they appear
                in the table.

        Returns:

            Union[TableColumn, None]:
                The table column object if found, otherwise None.
        """
        if cid is not None:
            return self._cidmap.get(cid)

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

    def get_rows(self, visible=False, filtered=False, selected=False) -> List[TableRow]:
        """Return a list of TableRow objects.

        Return a subset of rows based on optional flags. Only ONE flag can be used
        at a time. If more than one flag is set to `True`, then the first flag will
        be used to return the data.

        Parameters:

            visible (bool):
                If true, only records in the current view will be returned.

            filtered (bool):
                If True, only rows in the filtered dataset will be returned.

            selected (bool):
                If True, only rows that are currently selected will be returned.

        Returns:

            List[TableRow]:
                A list of TableRow objects.
        """
        if visible:
            return self._viewdata
        elif filtered:
            return self._tablerows_filtered
        elif selected:
            return [row for row in self._viewdata if row.iid in self.view.selection()]
        else:
            return self._tablerows

    def get_row(self, index=None, visible=False, filtered=False, iid=None) -> TableRow:
        """Returns the `TableRow` object from an index or the iid.

        If an index is specified, the row index refers to the index
        within the original dataset. When choosing a subset of data,
        the visible data takes priority over filtered if both flags
        are set.

        If an iid is specified, the object attached to that iid is
        returned regardless of whether or not it is visible or
        filtered.

        Parameters:

            index (int):
                The numerical index of the column.

            iid (str):
                A unique column identifier.

            visible (bool):
                Use the index of the visible rows as they appear
                in the current table view.

            filtered (bool):
                Use the index of the rows within the filtered data
                set.

        Returns:

            Union[TableRow, None]:
                The table column object if found, otherwise None
        """
        if iid is not None:
            return self.iidmap.get(iid)

        if visible:
            try:
                return self.tablerows_visible[index]
            except IndexError:
                return None
        elif filtered:
            try:
                return self.tablerows_filtered[index]
            except IndexError:
                return None
        else:
            try:
                return self.tablerows[index]
            except IndexError:
                return None

    # PAGE NAVIGATION

    def _select_first_visible_item(self):
        try:
            iid = self.tablerows_visible[0].iid
            self.view.selection_set(iid)
            # must force focus, sometimes just focus on iid doesn't work
            self.view.focus_force()
            # this sets the focus on the specific row item
            self.view.focus(iid)
            # make sure the row is visible
            self.view.see(iid)
        except:
            pass

    def goto_first_page(self):
        """Update table with first page of data"""
        self._rowindex.set(0)
        self.load_table_data()
        self._select_first_visible_item()

    def goto_last_page(self):
        """Update table with the last page of data"""
        pagelimit = self._pagelimit.get() - 1
        self._rowindex.set(self.pagesize * pagelimit)
        self.load_table_data()
        self._select_first_visible_item()

    def goto_next_page(self):
        """Update table with next page of data"""
        if self._pageindex.get() >= self._pagelimit.get():
            return
        rowindex = self._rowindex.get()
        self._rowindex.set(rowindex + self.pagesize)
        self.load_table_data()
        self._select_first_visible_item()

    def goto_prev_page(self):
        """Update table with prev page of data"""
        if self._pageindex.get() <= 1:
            return
        rowindex = self._rowindex.get()
        self._rowindex.set(rowindex - self.pagesize)
        self.load_table_data()
        self._select_first_visible_item()

    def goto_page(self, *_):
        """Go to a specific page indicated by the page entry widget."""
        pagelimit = self._pagelimit.get()
        pageindex = self._pageindex.get()
        if pageindex > pagelimit:
            pageindex = pagelimit
            self._pageindex.set(pageindex)
        elif pageindex <= 0:
            pageindex = 1
            self._pageindex.set(pageindex)
        rowindex = (pageindex * self.pagesize) - self.pagesize
        self._rowindex.set(rowindex)
        self.load_table_data()
        self._select_first_visible_item()

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
            column = eo.column
            index = column.tableindex
        elif cid is not None:
            column: TableColumn = self.cidmap.get(int(cid))
            index = column.tableindex
        else:
            return

        # update table data
        if self.is_filtered:
            tablerows = self.tablerows_filtered
        else:
            tablerows = self.tablerows

        if sort is not None:
            columnsort = sort
        else:
            columnsort = self.tablecolumns[index].columnsort

        if columnsort == ASCENDING:
            self._tablecols[index].columnsort = DESCENDING
        else:
            self._tablecols[index].columnsort = ASCENDING

        try:
            sortedrows = sorted(
                tablerows, reverse=columnsort, key=lambda x: x.values[index]
            )
        except:
            # when data is missing, or sometimes with numbers
            # this is still not right, but it works most of the time
            # fix sometime down the road when I have time
            self.fill_empty_columns()
            sortedrows = sorted(
                tablerows, reverse=columnsort, key=lambda x: int(x.values[index])
            )
        if self.is_filtered:
            self._tablerows_filtered = sortedrows
        else:
            self._tablerows = sortedrows

        # update headers
        self._column_sort_header_reset()
        self._column_sort_header_update(column.cid)

        self.unload_table_data()
        self.load_table_data()
        self._select_first_visible_item()

    # DATA SEARCH & FILTERING

    def reset_row_filters(self):
        """Remove all row level filters; unhide all rows."""
        self._filtered = False
        self.searchcriteria = ""
        self.unload_table_data()
        self.load_table_data()

    def reset_column_filters(self):
        """Remove all column level filters; unhide all columns."""
        cols = [col.cid for col in self.tablecolumns]
        self.view.configure(displaycolumns=cols)

    def reset_row_sort(self):
        """Display all table rows by original insert index"""
        ...

    def reset_column_sort(self):
        """Display all columns by original insert index"""
        cols = sorted([col.cid for col in self.tablecolumns_visible], key=int)
        self.view.configure(displaycolumns=cols)

    def reset_table(self):
        """Remove all table data filters and column sorts"""
        self._filtered = False
        self.searchcriteria = ""
        try:
            sortedrows = sorted(self.tablerows, key=lambda x: x._sort)
        except IndexError:
            self.fill_empty_columns()
            sortedrows = sorted(self.tablerows, key=lambda x: x._sort)
        self._tablerows = sortedrows
        self.unload_table_data()

        # reset the columns
        self.reset_column_filters()
        self.reset_column_sort()

        self._column_sort_header_reset()
        self.goto_first_page()  # needed?

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
            index = eo.column.tableindex
            value = value or eo.row.values[index]
        elif cid is not None:
            column: TableColumn = self.cidmap.get(cid)
            index = column.tableindex
        else:
            return

        self._filtered = True
        self.tablerows_filtered.clear()
        self.unload_table_data()

        for row in self.tablerows:
            if row.values[index] == value:
                self.tablerows_filtered.append(row)

        self._rowindex.set(0)
        self.load_table_data()

    def filter_to_selected_rows(self):
        """Hide all records except for the selected rows"""
        criteria = self.view.selection()
        if len(criteria) == 0:
            return  # nothing is selected

        if self.is_filtered:
            for row in self.tablerows_visible:
                if row.iid not in criteria:
                    row.hide()
                    self.tablerows_filtered.remove(row)
        else:
            self._filtered = True
            self.tablerows_filtered.clear()
            for row in self.tablerows_visible:
                if row.iid in criteria:
                    self.tablerows_filtered.append(row)
        self._rowindex.set(0)
        self.load_table_data()

    def hide_selected_rows(self):
        """Hide the currently selected rows"""
        selected = self.view.selection()
        view_cnt = len(self._viewdata)
        hide_cnt = len(selected)
        self.view.detach(*selected)

        tablerows = []
        for row in self.tablerows_visible:
            if row.iid in selected:
                tablerows.append(row)

        if not self.is_filtered:
            self._filtered = True
            self._tablerows_filtered = self.tablerows.copy()

        for row in tablerows:
            if self.is_filtered:
                self.tablerows_filtered.remove(row)

        if hide_cnt == view_cnt:
            # assuming that if the count of the records on the page are
            #   selected for hiding, then need to go to the next page
            # The call to `load_table_data` is duplicative, but currently
            #   this is the only way to get this to work until I've
            #   refactored this bit.
            self.load_table_data()
            self.goto_page()
        else:
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
            column = eo.column.hide()
        elif cid is not None:
            column: TableColumn = self.cidmap.get(cid)
            column.hide()

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
            eo.column.show()
        elif cid is not None:
            column = self.cidmap.get(cid)
            column.show()

    # DATA EXPORT

    def export_all_records(self):
        """Export all records to a csv file"""
        headers = [col.headertext for col in self.tablecolumns]
        records = [row.values for row in self.tablerows]
        self.save_data_to_csv(headers, records, self._delimiter)

    def export_current_page(self):
        """Export records on current page to csv file"""
        headers = [col.headertext for col in self.tablecolumns]
        records = [row.values for row in self.tablerows_visible]
        self.save_data_to_csv(headers, records, self._delimiter)

    def export_current_selection(self):
        """Export rows currently selected to csv file"""
        headers = [col.headertext for col in self.tablecolumns]
        selected = self.view.selection()
        records = []
        for iid in selected:
            record: TableRow = self.iidmap.get(iid)
            records.append(record.values)
        self.save_data_to_csv(headers, records, self._delimiter)

    def export_records_in_filter(self):
        """Export rows currently filtered to csv file"""
        headers = [col.headertext for col in self.tablecolumns]
        if not self.is_filtered:
            return
        records = [row.values for row in self.tablerows_filtered]
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

        if self.is_filtered:
            tablerows = self.tablerows_filtered.copy()
        else:
            tablerows = self.tablerows.copy()

        for i, iid in enumerate(selected):
            row = self.iidmap.get(iid)
            tablerows.remove(row)
            tablerows.insert(i, row)

        if self.is_filtered:
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

        if self.is_filtered:
            tablerows = self.tablerows_filtered.copy()
        else:
            tablerows = self.tablerows.copy()

        for iid in selected:
            row = self.iidmap.get(iid)
            tablerows.remove(row)
            tablerows.append(row)

        if self.is_filtered:
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

        if self.is_filtered:
            tablerows = self._tablerows_filtered.copy()
        else:
            tablerows = self.tablerows.copy()

        for iid in selected:
            row = self.iidmap.get(iid)
            index = tablerows.index(row) - 1
            tablerows.remove(row)
            tablerows.insert(index, row)

        if self.is_filtered:
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

        for iid in selected:
            row = self.iidmap.get(iid)
            index = tablerows.index(row) + 1
            tablerows.remove(row)
            tablerows.insert(index, row)

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
            column = eo.column
        elif cid is not None:
            column = self.cidmap.get(cid)
        else:
            return

        displaycols = [x.cid for x in self.tablecolumns_visible]
        old_index = column.displayindex
        if old_index == 0:
            return

        new_index = column.displayindex - 1
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
            column = eo.column
        elif cid is not None:
            column = self.cidmap.get(cid)
        else:
            return

        displaycols = [x.cid for x in self.tablecolumns_visible]
        old_index = column.displayindex
        if old_index == len(displaycols) - 1:
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
            column = eo.column
        elif cid is not None:
            column = self.cidmap.get(cid)
        else:
            return

        displaycols = [x.cid for x in self.tablecolumns_visible]
        old_index = column.displayindex
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
            column = eo.column
        elif cid is not None:
            column = self.cidmap.get(cid)
        else:
            return

        displaycols = [x.cid for x in self.tablecolumns_visible]
        old_index = column.displayindex
        if old_index == len(displaycols) - 1:
            return

        new_index = len(displaycols) - 1
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
        style: ttk.Style = ttk.Style.get_instance()
        colors = style.colors
        if len(stripecolor) == 2:
            self._stripecolor = stripecolor
            bg, fg = stripecolor
            kw = {}
            if bg is None:
                kw["background"] = colors.active
            else:
                kw["background"] = bg
            if fg is None:
                kw["foreground"] = colors.inputfg
            else:
                kw["foreground"] = fg
            self.view.tag_configure("striped", **kw)

    def autofit_columns(self):
        """Autofit all columns in the current view"""
        f = font.nametofont("TkDefaultFont")
        pad = utility.scale_size(self, 20)
        col_widths = []

        # measure header sizes
        for col in self.tablecolumns:
            width = f.measure(f"{col._headertext} {DOWNARROW}") + pad
            col_widths.append(width)

        for row in self.tablerows_visible:
            values = row.values
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
            self.view.column(eo.column.cid, anchor=W)
        elif cid is not None:
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
            self.view.column(eo.column.cid, anchor=E)
        elif cid is not None:
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
            self.view.column(eo.column.cid, anchor=CENTER)
        elif cid is not None:
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
            self.view.heading(eo.column.cid, anchor=W)
        elif cid is not None:
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
            self.view.heading(eo.column.cid, anchor=E)
        elif cid is not None:
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
            self.view.heading(eo.column.cid, anchor=CENTER)
        elif cid is not None:
            self.view.heading(cid, anchor=CENTER)

    # PRIVATE METHODS

    def _get_event_objects(self, event):
        iid = self.view.identify_row(event.y)
        col = self.view.identify_column(event.x)
        cid = int(self.view.column(col, "id"))
        column: TableColumn = self.cidmap.get(cid)
        row: TableRow = self.iidmap.get(iid)
        data = TableEvent(column, row)
        return data

    def _search_table_data(self, _):
        """Search the table data for records that meet search criteria.
        Currently, this search locates any records that contain the
        specified text; it is also case insensitive.
        """
        criteria = self._searchcriteria.get()
        self._filtered = True
        self.tablerows_filtered.clear()
        self.unload_table_data()
        for row in self.tablerows:
            for col in row.values:
                if str(criteria).lower() in str(col).lower():
                    self.tablerows_filtered.append(row)
                    break
        self._rowindex.set(0)
        self.load_table_data()

    # PRIVATE METHODS - SORTING

    def _column_sort_header_reset(self):
        """Remove the sort character from the column headers"""
        for col in self.tablecolumns:
            self.view.heading(col.cid, text=col.headertext)

    def _column_sort_header_update(self, cid):
        """Add sort character to the sorted column"""
        column: TableColumn = self.cidmap.get(int(cid))
        arrow = UPARROW if column.columnsort == ASCENDING else DOWNARROW
        headertext = f"{column.headertext} {arrow}"
        self.view.heading(column.cid, text=headertext)

    # PRIVATE METHODS - WIDGET BUILDERS

    def _build_tableview_widget(self, coldata, rowdata, bootstyle):
        """Build the data table"""
        if self._searchable:
            self._build_search_frame()
            
        table_frame = ttk.Frame(self)
        table_frame.pack(fill=BOTH, expand=YES, side=TOP)

        self.view = ttk.Treeview(
            master=table_frame,
            columns=[x for x in range(len(coldata))],
            height=self._height,
            selectmode=EXTENDED,
            show=HEADINGS,
            bootstyle=f"{bootstyle}-table",
        )
        self.view.pack(fill=BOTH, expand=YES, side=LEFT)
        
        if self._yscrollbar:
            self.ybar = ttk.Scrollbar(
                master=table_frame, command=self.view.yview, orient=VERTICAL
            )
            self.ybar.pack(fill=Y, side=RIGHT)
            self.view.configure(yscrollcommand=self.ybar.set)
        
        self.hbar = ttk.Scrollbar(
            master=self, command=self.view.xview, orient=HORIZONTAL
        )
        self.hbar.pack(fill=X)
        self.view.configure(xscrollcommand=self.hbar.set)

        if self._paginated:
            self._build_pagination_frame()

        self.build_table_data(coldata, rowdata)

        self._rightclickmenu_cell = TableCellRightClickMenu(self)
        self._rightclickmenu_head = TableHeaderRightClickMenu(self)
        self._set_widget_binding()

    def _build_search_frame(self):
        """Build the search frame containing the search widgets. This
        frame is only created if `searchable=True` when creating the
        widget.
        """
        frame = ttk.Frame(self, padding=5)
        frame.pack(fill=X, side=TOP)
        ttk.Label(frame, text=MessageCatalog.translate("Search")).pack(side=LEFT, padx=5)
        searchterm = ttk.Entry(frame, textvariable=self._searchcriteria)
        searchterm.pack(fill=X, side=LEFT, expand=YES)
        searchterm.bind("<Return>", self._search_table_data)
        searchterm.bind("<KP_Enter>", self._search_table_data)
        if not self._paginated:
            ttk.Button(
                frame,
                text=MessageCatalog.translate("⎌"),
                command=self.reset_table,
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
            pageframe,
            text=MessageCatalog.translate("⎌"),
            command=self.reset_table,
            style="symbol.Link.TButton",
        ).pack(side=RIGHT)

        ttk.Separator(pageframe, orient=VERTICAL).pack(side=RIGHT, padx=10)

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

        ttk.Separator(pageframe, orient=VERTICAL).pack(side=RIGHT, padx=10)

        lbl = ttk.Label(pageframe, textvariable=self._pagelimit)
        lbl.pack(side=RIGHT, padx=(0, 5))
        ttk.Label(pageframe, text=MessageCatalog.translate("of")).pack(side=RIGHT, padx=(5, 0))

        index = ttk.Entry(pageframe, textvariable=self._pageindex, width=4)
        index.pack(side=RIGHT)
        index.bind("<Return>", self.goto_page, "+")
        index.bind("<KP_Enter>", self.goto_page, "+")

        ttk.Label(pageframe, text=MessageCatalog.translate("Page")).pack(side=RIGHT, padx=5)

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
                self.tablecolumns.append(
                    TableColumn(
                        tableview=self,
                        cid=cid,
                        text=col,
                    )
                )
            else:
                if "text" not in col:
                    col["text"] = f"Column {cid}"
                self.tablecolumns.append(
                    TableColumn(tableview=self, cid=cid, **col)
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
        self._pagesize.trace_add("write", self._trace_pagesize)

    # def _select_pagesize(self, event):
    #     cbo: ttk.Combobox = self.nametowidget(event.widget)
    #     cbo.select_clear()
    #     self.goto_first_page()

    def _trace_pagesize(self, *_):
        """Callback for changes to page size"""
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
            self.sort_column_data(event)

    def _table_rightclick(self, event):
        """Callback for right-click events"""
        region = self.view.identify_region(event.x, event.y)
        if region == "heading":
            self._rightclickmenu_head.tk_popup(event)
        elif region != "separator":
            self._rightclickmenu_cell.tk_popup(event)


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
                "label": f'''⬆  {MessageCatalog.translate("Sort Ascending")}''',
                "command": self.sort_column_ascending,
            },
            "sortdescending": {
                "label": f'''⬇  {MessageCatalog.translate("Sort Descending")}''',
                "command": self.sort_column_descending,
            },
            "clearfilter": {
                "label": f'''{MessageCatalog.translate("⎌")} {MessageCatalog.translate("Clear filters")}''',
                "command": self.master.reset_row_filters,
            },
            "filterbyvalue": {
                "label": f'''{MessageCatalog.translate("Filter by cell's value")}''',
                "command": self.filter_to_cell_value,
            },
            "hiderows": {
                "label": f'''{MessageCatalog.translate("Hide select rows")}''',
                "command": self.hide_selected_rows,
            },
            "showrows": {
                "label": f'''{MessageCatalog.translate("Show only select rows")}''',
                "command": self.filter_to_selected_rows,
            },
            "exportall": {
                "label": f'''{MessageCatalog.translate("Export all records")}''',
                "command": self.export_all_records,
            },
            "exportpage": {
                "label": f'''{MessageCatalog.translate("Export current page")}''',
                "command": self.export_current_page,
            },
            "exportselection": {
                "label": f'''{MessageCatalog.translate("Export current selection")}''',
                "command": self.export_current_selection,
            },
            "exportfiltered": {
                "label": f'''{MessageCatalog.translate("Export records in filter")}''',
                "command": self.export_records_in_filter,
            },
            "moveup": {
                "label": f'''↑ {MessageCatalog.translate("Move up")}''',
                "command": self.move_row_up
            },
            "movedown": {
                "label": f'''↓ {MessageCatalog.translate("Move down")}''',
                "command": self.move_row_down,
            },
            "movetotop": {
                "label": f'''⤒ {MessageCatalog.translate("Move to top")}''',
                "command": self.move_row_to_top,
            },
            "movetobottom": {
                "label": f'''⤓ {MessageCatalog.translate("Move to bottom")}''',
                "command": self.move_row_to_bottom,
            },
            "alignleft": {
                "label": f'''◧  {MessageCatalog.translate("Align left")}''',
                "command": self.align_column_left,
            },
            "aligncenter": {
                "label": f'''◫  {MessageCatalog.translate("Align center")}''',
                "command": self.align_column_center,
            },
            "alignright": {
                "label": f'''◨  {MessageCatalog.translate("Align right")}''',
                "command": self.align_column_right,
            },
            "deleterows": {
                "label": f'''🞨  {MessageCatalog.translate("Delete selected rows")}''',
                "command": self.delete_selected_rows,
            },
        }
        sort_menu = tk.Menu(self, tearoff=False)
        sort_menu.add_command(cnf=config["sortascending"])
        sort_menu.add_command(cnf=config["sortdescending"])
        self.add_cascade(menu=sort_menu, label=f'''⇅  {MessageCatalog.translate("Sort")}''')

        filter_menu = tk.Menu(self, tearoff=False)
        filter_menu.add_command(cnf=config["clearfilter"])
        filter_menu.add_separator()
        filter_menu.add_command(cnf=config["filterbyvalue"])
        filter_menu.add_command(cnf=config["hiderows"])
        filter_menu.add_command(cnf=config["showrows"])
        self.add_cascade(menu=filter_menu, label=f'''⧨  {MessageCatalog.translate("Filter")}''')

        export_menu = tk.Menu(self, tearoff=False)
        export_menu.add_command(cnf=config["exportall"])
        export_menu.add_command(cnf=config["exportpage"])
        export_menu.add_command(cnf=config["exportselection"])
        export_menu.add_command(cnf=config["exportfiltered"])
        self.add_cascade(menu=export_menu, label=f'''↔  {MessageCatalog.translate("Export")}''')

        move_menu = tk.Menu(self, tearoff=False)
        move_menu.add_command(cnf=config["moveup"])
        move_menu.add_command(cnf=config["movedown"])
        move_menu.add_command(cnf=config["movetotop"])
        move_menu.add_command(cnf=config["movetobottom"])
        self.add_cascade(menu=move_menu, label=f'''⇵  {MessageCatalog.translate("Move")}''')

        align_menu = tk.Menu(self, tearoff=False)
        align_menu.add_command(cnf=config["alignleft"])
        align_menu.add_command(cnf=config["aligncenter"])
        align_menu.add_command(cnf=config["alignright"])
        self.add_cascade(menu=align_menu, label=f'''↦  {MessageCatalog.translate("Align")}''')
        self.add_command(cnf=config["deleterows"])

    def tk_popup(self, event):
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
        try:
            bbox = self.view.bbox(iid, col)
        except:
            return
        try:
            super().tk_popup(rootx + bbox[0], rooty + bbox[1] + bbox[3])
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

    def delete_selected_rows(self):
        """Delete the selected rows"""
        iids = self.view.selection()
        if len(iids) > 0:
            # setting to prev should be in master?
            prev_item = self.view.prev(iids[0])
            self.master.delete_rows(iids=iids)
            self.view.focus(prev_item)
            self.view.selection_set(prev_item)


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
        self.columnvars = []
        self._show_menu = None

        config = {
            "movetoright": {
                "label": f'''→  {MessageCatalog.translate("Move to right")}''',
                "command": self.move_column_right,
            },
            "movetoleft": {
                "label": f'''←  {MessageCatalog.translate("Move to left")}''',
                "command": self.move_column_left,
            },
            "movetofirst": {
                "label": f'''⇤  {MessageCatalog.translate("Move to first")}''',
                "command": self.move_column_to_first,
            },
            "movetolast": {
                "label": f'''⇥  {MessageCatalog.translate("Move to last")}''',
                "command": self.move_column_to_last,
            },
            "alignleft": {
                "label": f'''◧  {MessageCatalog.translate("Align left")}''',
                "command": self.align_heading_left,
            },
            "alignright": {
                "label": f'''◨  {MessageCatalog.translate("Align right")}''',
                "command": self.align_heading_right,
            },
            "aligncenter": {
                "label": f'''◫  {MessageCatalog.translate("Align center")}''',
                "command": self.align_heading_center,
            },
            "resettable": {
                "label": f'''{MessageCatalog.translate("⎌")}  {MessageCatalog.translate("Reset table")}''',
                "command": self.master.reset_table,
            },
            "deletecolumn": {
                "label": f'''🞨  {MessageCatalog.translate("Delete column")}''',
                "command": self.delete_column,
            },
            "hidecolumn": {
                "label": f'''◑  {MessageCatalog.translate("Hide column")}''',
                "command": self.hide_column,
            },
        }

        self.add_command(cnf=config["resettable"])

        # HIDE & SHOW
        self._build_show_menu()
        self.add_cascade(menu=self._show_menu, label=f'''±  {MessageCatalog.translate("Columns")}''')
        self.add_separator()

        # MOVE MENU
        move_menu = tk.Menu(self, tearoff=False)
        move_menu.add_command(cnf=config["movetoleft"])
        move_menu.add_command(cnf=config["movetoright"])
        move_menu.add_command(cnf=config["movetofirst"])
        move_menu.add_command(cnf=config["movetolast"])
        self.add_cascade(menu=move_menu, label=f'''⇄  {MessageCatalog.translate("Move")}''')

        align_menu = tk.Menu(self, tearoff=False)
        align_menu.add_command(cnf=config["alignleft"])
        align_menu.add_command(cnf=config["aligncenter"])
        align_menu.add_command(cnf=config["alignright"])
        self.add_cascade(menu=align_menu, label=f'''↦  {MessageCatalog.translate("Align")}''')
        self.add_command(cnf=config["hidecolumn"])
        self.add_command(cnf=config["deletecolumn"])

    def tk_popup(self, event):
        # capture the column and item that invoked the menu
        self.event = event
        self._build_show_menu()

        # show the menu below the invoking cell
        rootx = self.view.winfo_rootx()
        rooty = self.view.winfo_rooty()
        super().tk_popup(rootx + event.x, rooty + event.y + 10)

    def _build_show_menu(self):
        """Build the show menu based on currently available columns"""
        if self._show_menu is not None:
            self._show_menu.delete(0, END)
        else:
            self._show_menu = tk.Menu(self, tearoff=False)

        self._show_menu.add_command(
            label=MessageCatalog.translate("Show All"), command=self.show_all_columns
        )
        self._show_menu.add_separator()

        displaycolumns = [x.cid for x in self.master.tablecolumns_visible]
        for column in self.master.tablecolumns:
            varname = f"column_{column.cid}"
            # self.columnvars.append(tk.Variable(name=varname, value=True))
            self._show_menu.add_checkbutton(
                label=column._headertext,
                command=lambda w=column: self.toggle_columns(w.cid),
                variable=varname,
                onvalue=True,
                offvalue=False,
            )
            if column.cid in displaycolumns:
                self.setvar(varname, True)
            else:
                self.setvar(varname, False)

    def toggle_columns(self, cid):
        """Toggles the visibility of the selected column"""
        variable = f"column_{cid}"
        toggled = self.getvar(variable)
        if toggled:
            self.master.unhide_selected_column(cid=int(cid))
        else:
            self.master.hide_selected_column(cid=int(cid))

    def show_all_columns(self):
        """Show all columns"""
        for var in self.columnvars:
            var.set(value=True)
        self.master.reset_column_filters()

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

    def delete_column(self):
        """Delete the selected column"""
        eo = self.master._get_event_objects(self.event)
        eo.column.delete()

    def hide_column(self):
        """Hide the selected column"""
        eo = self.master._get_event_objects(self.event)
        eo.column.hide()
