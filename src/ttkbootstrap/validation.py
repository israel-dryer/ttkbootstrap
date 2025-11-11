r"""Validation framework for ttkbootstrap entry widgets.

This module provides classes and functions for adding validation to Entry,
Spinbox, and Combobox widgets. When validation fails, a 'danger' colored
border is applied to the widget, which disappears when the contents become valid.

The module includes:
    - Predefined validation functions (text, numeric, phone number, regex, etc.)
    - Custom validation decorator (@validator)
    - Helper functions starting with "add_" prefix for quick validation setup

Classes:
    ValidationEvent: Contains attributes of a validation event from tkinter

Functions:
    add_validation: Core function to add validation to any compatible widget
    add_text_validation: Validate that contents is alphabetic text
    add_numeric_validation: Validate that contents is numeric
    add_phonenumber_validation: Validate phone number format
    add_regex_validation: Validate against custom regex pattern
    add_range_validation: Validate numeric value is within range
    add_option_validation: Validate value is in list of options

Example:
    Using predefined validation:
    ```python
    import ttkbootstrap as ttk
    from ttkbootstrap.validation import *

    app = ttk.Window()
    entry = ttk.Entry()
    entry.pack(padx=10, pady=10)

    # Check if contents is text
    add_text_validation(entry)

    # Prevent any entry except text
    add_text_validation(entry, when='key')

    # Check for specific list of options
    add_option_validation(entry, ['red', 'blue', 'green'])

    # Validate against regex expression
    add_regex_validation(entry, r'\d{4}-\d{2}-\d{2}')

    app.mainloop()
    ```

    Creating custom validation:
    ```python
    from ttkbootstrap.validation import validator, add_validation

    @validator
    def validate_long_text(event):
        if len(event.postchangetext) > 20:
            return True
        else:
            return False

    # Apply custom validation
    add_validation(entry, validate_long_text)
    ```
"""
import re
from tkinter import Misc
from typing import Any, Callable, Union

import ttkbootstrap as ttk


class ValidationEvent:
    """Contains the attributes of a validation event returned by the
    `validatecommand` on a tkinter widget.

    Attributes:

        actioncode (str):
            0 for an attempted deletion, 1 for an attempted insertion,
            or -1 if the callback was for focusin, focusout, or a
            change to the textvariable.

        insertdeleteindex (str):
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

        validationreason (str):
            The reason for the validation callback (key, focusin,
            focusout, forced).

        widget (Widget):
            The widget object that is being validated.
    """

    def __init__(self, d: str, i: str, P: str, s: str, S: str, v: str, V: str, W: str) -> None:
        self.actioncode = d
        self.insertdeleteindex = i
        self.postchangetext = P
        self.prechangetext = s
        self.insertdeletetext = S
        self.validationtype = v
        self.validationreason = V

        style = ttk.Style.get_instance()
        self.widget = style.master.nametowidget(
            W
        )  # replace with another method


def validator(func: Callable[[ValidationEvent], bool]) -> Callable[..., bool]:
    """Decorates a standard function so that it receives the validation
    events returned by the validate command on the tkinter widgets.

    Parameters:

        func (Callable):
            The validation function to be decorated.
    """

    def inner(*args: Any, **kw: Any) -> bool:
        event = ValidationEvent(*args)
        return func(event, **kw)

    return inner


def add_validation(widget: Misc, func: Callable[..., bool], when: str = "focusout", **kwargs: Any) -> None:
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
def _validate_text(event: ValidationEvent) -> bool:
    """Contents is text."""
    if len(event.postchangetext) == 0:
        return True
    return str(event.postchangetext).isalpha()


@validator
def _validate_number(event: ValidationEvent) -> bool:
    """Contents is a number."""
    if len(event.postchangetext) == 0:
        return True
    return str(event.postchangetext).isnumeric()


@validator
def _validate_options(event: ValidationEvent, options: list[Any]) -> bool:
    """Contents is in a list of options"""
    return event.postchangetext in options


@validator
def _validate_range(
    event: ValidationEvent, startrange: Union[int, float], endrange: Union[int, float]
) -> bool:
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
def _validate_regex(event: ValidationEvent, pattern: str) -> bool:
    """Contents matches a regex expression"""
    match = re.match(pattern, event.postchangetext)
    return match is not None


# helper methods


def add_text_validation(widget: Misc, when: str = "focusout") -> None:
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


def add_numeric_validation(widget: Misc, when: str = "focusout") -> None:
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


def add_phonenumber_validation(widget: Misc, when: str = "focusout") -> None:
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


def add_regex_validation(widget: Misc, pattern: str, when: str = "focusout") -> None:
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


def add_range_validation(
    widget: Misc,
    startrange: Union[int, float],
    endrange: Union[int, float],
    when: str = "focusout",
) -> None:
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


def add_option_validation(widget: Misc, options: list[Any], when: str = "focusout") -> None:
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
    def my_validation(event: ValidationEvent) -> bool:
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
