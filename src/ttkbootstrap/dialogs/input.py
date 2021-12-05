"""
    This module contains helper functions that request and return data
    from the end user.
"""

from ttkbootstrap.dialogs import DatePickerPopup

def ask_date(
    parent=None,
    title='',
    firstweekday=6,
    startdate=None,
    bootstyle='primary'
):
    """Shows a calendar popup and returns the selection.

    Parameters:

        parent (Widget):
            The parent widget; the popup will appear to the 
            bottom-right of the parent widget. If no parent is 
            provided, the widget is centered on the screen. 

        title (str):
            The text that appears on the popup titlebar.

        firstweekday (int):
            Specifies the first day of the week. `0` is Monday, `6` is 
            Sunday (the default). 

        startdate (datetime):
            The date to be in focus when the widget is displayed; 

        bootstyle (str):
            The following colors can be used to change the color of the
            title and hover / pressed color -> primary, secondary, info,
            warning, success, danger, light, dark.       

    Returns:

        datetime:
            The date selected; the current date if no date is selected.
    """
    chooser = DatePickerPopup(
        parent=parent,
        title=title,
        firstweekday=firstweekday,
        startdate=startdate,
        bootstyle=bootstyle
    )
    return chooser.date_selected