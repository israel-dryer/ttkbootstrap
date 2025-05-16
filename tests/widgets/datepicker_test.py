import tkinter as tk
from datetime import datetime, date
from ttkbootstrap import Style
from ttkbootstrap.dialogs import Querybox
from ttkbootstrap.dialogs.datepicker import DatePickerDialog


def test_datepicker_dialog():
    """Manual test for DatePickerDialog. Run this and select a date."""
    root = tk.Tk()

    # Setup
    Style("flatly")
    start_date = date(2023, 12, 25)  # Set known start date

    print('about to start dialog')

    dialog = DatePickerDialog(
        parent=root,
        title="Test Date Picker",
        firstweekday=0,  # Monday start
        startdate=start_date,
        color="success",
    )
    print("Selected date:", dialog.date_selected)


if __name__ == "__main__":
    test_datepicker_dialog()
