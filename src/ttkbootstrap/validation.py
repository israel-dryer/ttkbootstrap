"""
    This module contains classes and functions that are used to add
    validation to Entry, Spinbox, and Combobox widgets. Several helper 
    methods are included which start with the "add" prefix.

    ## Using predefined methods
    
    When validation is applied to a widget and the input is determined
    to be invalid, a 'danger' colored border is applied to the widget.
    This border disappears when the widget is determined to have valid
    contents.

    Below are a few examples using predefined validation. Browse the 
    full list in the documentation below:
    ```python
    app = ttk.Window()

    entry = ttk.Entry()
    entry.pack(padx=10, pady=10)

    # check if contents is text
    add_text_validation(entry)

    # prevent any entry except text
    add_text_validation(entry, when='key')

    # check for a specific list of options
    add_option_validation(entry, ['red', 'blue', 'green'])

    # validate against a specific regex expression
    add_regex_validation(entry, r'\d{4}-\d{2}-\d{2}')    
    ```

    ## Adding a custom validation

    First, create a custom validation function. This must accept a 
    `ValidationEvent` object and should return a boolean. You should
    also use the @validator decorator to convert this method to a
    validation method. Check the `ValidationEvent` attributes to 
    learn about what is returned in this event.

    ```python
    from ttkbootstrap import validator, add_validation

    @validator
    def validate_long_text(event):
        if len(event.postchangetext) > 20:
            return True
        else:
            return False
    ```

    Apply your custom validation to the widget
    ```python
    add_validation(entry, validate_long_text)
    ```
"""
import ttkbootstrap as ttk
import re


class ValidationEvent:
    """Contains the attributes of a validation event returned by the
    `validatecommand` on a tkinter widget.

    Attributes:

        actioncode (str):
            0 for an attempted deletion, 1 for an attempted insertion,
            or -1 if the callback was for focusin, focusout, or a
            change to the textvariable.

        insertdeletetext (str):
            When the user attempts to insert or delete text, this
            attribute will be the index of the beginning of the
            insertion or deletion. If the callback was due to focusin,
            focusout, or a change to the textvariable, the attribute
            will be -1.

        postchangetext (str):
            The value that the text will have if the change is allowed.

        prechangetext (str):
            The text in the entry before the change.

        insertdeletetext (str):
            The text inserted or deleted if the call was due to an
            insertion or deletion.

        validationtype (str):
            Specifies the widget's validation option which specifies
            _when_ the validation will occur.

        widget (Widget):
            The widget object that is being validated.
    """

    def __init__(self, d, i, P, s, S, v, V, W):
        self.actioncode = d
        self.insertdeletetext = i
        self.postchangetext = P
        self.prechangetext = s
        self.insertdeletetext = S
        self.validationtype = v
        self.validationreason = V

        style = ttk.Style.get_instance()
        self.widget = style.master.nametowidget(
            W
        )  # replace with another method


def validator(func):
    """Decorates a standard function so that it receives the validation
    events returned by the validate command on the tkinter widgets.

    Parameters:

        func (Callable):
            The validation function to be decorated.
    """

    def inner(*args, **kw):
        event = ValidationEvent(*args)
        return func(event, **kw)

    return inner


def add_validation(widget, func, when="focusout", **kwargs):
    """Adds validation to the widget of type `Entry`, `Combobox`, or
    `Spinbox`. The func should accept a parameter of type
    `ValidationEvent` and should return a boolean value.

    Parameters:

        widget (Widget):
            The widget on which validation will be applied.

        func (Callable):
            The function that will be called when a validation event
            occurs.

        when (str):
            Indicates when the validation event should occur. Possible
            values include:

            * focus - whenever the widget gets or loses focus
            * focusin - whenever the widget gets focus
            * focusout - whenever the widget loses focus
            * key - whenever a key is pressed
            * all - validate in all of the above situations

        kwargs (Dict):
            Optional arguments passed to the callback.
    """
    f = widget.register(lambda *e: func(*e, **kwargs))
    subs = (r"%d", r"%i", r"%P", r"%s", r"%S", r"%v", r"%V", r"%W")
    widget.configure(validate=when, validatecommand=(f, *subs))


@validator
def _validate_text(event: ValidationEvent):
    """Contents is text."""
    if len(event.postchangetext) == 0:
        return True
    return str(event.postchangetext).isalpha()


@validator
def _validate_number(event: ValidationEvent):
    """Contents is a number."""
    if len(event.postchangetext) == 0:
        return True
    return str(event.postchangetext).isnumeric()


@validator
def _validate_options(event: ValidationEvent, options):
    """Contents is in a list of options"""
    return event.postchangetext in options


@validator
def _validate_range(event: ValidationEvent, startrange, endrange):
    """Contents is a number between the startrange and endrange
    inclusive
    """
    if len(event.postchangetext) == 0:
        return True
    try:
        num = float(event.postchangetext)
        result = num >= startrange and num <= endrange
        return result
    except:
        return False


@validator
def _validate_regex(event: ValidationEvent, pattern):
    """Contents matches a regex expression"""
    match = re.match(pattern, event.postchangetext)
    return match is not None


# helper methods


def add_text_validation(widget, when="focusout"):
    """Check if widget contents is alpha. Sets the state to 'Invalid'
    if not text.

    Parameters:

        widget (Widget):
            The widget on which to add validation.

        when (str):
            Specifies when to apply validation. See the `add_validation`
            method docstring for a full list of options.
    """
    add_validation(widget, _validate_text, when=when)


def add_numeric_validation(widget, when="focusout"):
    """Check if widget contents is numeric. Sets the state to 'Invalid'
    if not a number.

    Parameters:

        widget (Widget):
            The widget on which to add validation.

        when (str):
            Specifies when to apply validation. See the `add_validation`
            method docstring for a full list of options.
    """
    add_validation(widget, _validate_number, when=when)


def add_phonenumber_validation(widget, when="focusout"):
    """Check if the widget contents matches a phone number pattern.

    Parameters:

        widget (Widget):
            The widget on which to add validation.

        when (str):
            Specifies when to apply validation. See the `add_validation`
            method docstring for a full list of options.
    """
    pattern = r"^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$"
    add_validation(widget, _validate_regex, pattern=pattern, when=when)


def add_regex_validation(widget, pattern, when="focusout"):
    """Check if widget contents matches regular expresssion. Sets the
    state to 'Invalid' if no match is found.

    Parameters:

        widget (Widget):
            The widget on which to add validation.

        when (str):
            Specifies when to apply validation. See the `add_validation`
            method docstring for a full list of options.
    """
    add_validation(widget, _validate_regex, pattern=pattern, when=when)


def add_range_validation(widget, startrange, endrange, when="focusout"):
    """Check if widget contents is within a range of numbers, inclusive.
    Sets the state to 'Invalid' if the number is outside of the range.

    Parameters:

        widget (Widget):
            The widget on which to add validation.

        when (str):
            Specifies when to apply validation. See the `add_validation`
            method docstring for a full list of options.
    """
    add_validation(
        widget,
        _validate_range,
        startrange=startrange,
        endrange=endrange,
        when=when,
    )


def add_option_validation(widget, options, when="focusout"):
    """Check if the widget contents is in a list of options.


    Parameters:

        widget (Widget):
            The widget on which to add validation.

        when (str):
            Specifies when to apply validation. See the `add_validation`
            method docstring for a full list of options.
    """
    add_validation(widget, _validate_options, options=options, when=when)


if __name__ == "__main__":

    app = ttk.Window()

    @validator
    def myvalidation(event: ValidationEvent) -> bool:
        print(event.postchangetext)
        return True

    entry = ttk.Entry()
    entry.pack(padx=10, pady=10)
    entry2 = ttk.Entry()
    entry2.pack(padx=10, pady=10)
    # add_validation(entry, validate_range, startrange=5, endrange=10)
    # add_validation(entry, validate_regex, pattern="israel")
    add_text_validation(entry, when="key")  # prevents from using any numbers
    add_text_validation(entry2, when="key")
    # add_option_validation(entry, ['red', 'blue', 'green'], 'focusout')
    # add_regex_validation(entry, r'\d{4}-\d{2}-\d{2}')
    ttk.Button(text="Other").pack(padx=10, pady=10)
    app.mainloop()
