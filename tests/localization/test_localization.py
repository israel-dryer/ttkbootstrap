import csv
import os
from pathlib import Path

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs.colorchooser import ColorChooserDialog
from ttkbootstrap.localization.msgcat import MessageCatalog
from ttkbootstrap.dialogs.dialogs import QueryDialog, Querybox
from ttkbootstrap.tableview import Tableview

def show_tableview():
    """Show tableview."""
    w = ttk.Toplevel()

    p = os.path.join(Path(__file__).parent, "..", "widgets", "Sample1000.csv")
    with open(p, encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)
        rowdata = list(reader)

    # column configuration options
    # text, image, command, anchor, width, minwidth, maxwidth, stretch
    coldata = [
        {"text": "SerialNumber", "stretch": False},
        "CompanyName",
        "Employee",
        "Description",
        {"text": "Leave", "stretch": False},
    ]

    dt = Tableview(
        master=w,
    #    coldata=coldata,
    #    rowdata=rowdata,
        paginated=True,
        searchable=True,
        bootstyle=PRIMARY,
        stripecolor=(None, None),
        autofit=False
    )
    dt.pack(fill=BOTH, expand=YES, padx=5, pady=5)

    dt.build_table_data(coldata, rowdata)
    #dt.delete_columns(indices=[2, 3])

    # modify the contents of a single cell
    row = dt.get_row(0)
    row.values[2] = "Israel"
    row.refresh()

    # modify an entire row
    row = dt.get_row(1)
    row.values = ['123456', 'My Company', 'Israel', 'Something here', 45]


def show_color_chooser():
    """Show the color dialog"""
    cd = ColorChooserDialog(initialcolor='#1122ff')
    cd.show()


def show_font_selector():
    """Show font selector"""
    Querybox.get_font(title="Querybox.get_font", position=(500, 500))


def show_date_entry():
    """Show a date entry dialog"""
    tl = ttk.Toplevel()
    frame = ttk.Frame(master=tl, padding=10)
    frame.pack(padx=10, pady=10)
    de = ttk.DateEntry(frame)
    de.pack(fill=X)

def change_locale():
    """Query user for new locale string."""
    locale_dialog = QueryDialog(
        prompt="Enter a locale to test:",
        title="Select Locale",
        initialvalue=MessageCatalog.locale("")
        )
    locale_dialog.show()

    selected_locale = locale_dialog.result
    if selected_locale:
        MessageCatalog.locale(selected_locale)
        print(f"Selected locale: '{MessageCatalog.locale(None)}'")

def create_window():
    """Create window."""
    root = ttk.Window()

    ttk.Button(root, text="Change Locale", bootstyle="success",
               command=change_locale, ).pack(side=LEFT, padx=5, pady=1)
    ttk.Button(root, text="Color Chooser",
               command=show_color_chooser).pack(side=LEFT, padx=5, pady=1)
    ttk.Button(root, text="Date entry",
               command=show_date_entry).pack(side=LEFT, padx=5, pady=1)
    ttk.Button(root, text="Font Selector",
               command=show_font_selector).pack(side=LEFT, padx=5, pady=1)
    ttk.Button(root, text="Tableview",
               command=show_tableview).pack(side=LEFT, padx=5, pady=1)

    root.mainloop()

if __name__ == '__main__':
    create_window()
