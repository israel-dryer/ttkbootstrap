# DatePickerPopup

This widget style encomposses a collection of button and label widgets. The 
_header_ and _active date_ are **primary** colored (default) or the 
[selected color](index.md#colors). The _weekdays header_ and _current date_ use the 
`secondary` color.

Check out the [api documentation](../../api/dialogs/datepickerpopup) for
more information on how to use this widget.

![date picker](../assets/widget-styles/date-picker-popup.gif)

```python
# default popup
DatePickerPopup()

# warning colored popup
DatePickerPopup(bootstyle="warning")
```