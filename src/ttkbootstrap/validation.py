r"""Validation framework for ttkbootstrap entry widgets.

Adds input validation to Entry, Spinbox, and Combobox widgets: a failing value
flags the widget with the ttk ``invalid`` state (a 'danger'-colored border) that
clears once the contents become valid. The public surface is the `Validation`
namespace (`Validation.numeric`, `Validation.range`, ..., and `Validation.add`
for a custom rule) plus the `@validator` decorator and the `ValidationEvent`
passed to a rule.

The pre-2.0 module-level `add_*_validation` functions remain as thin deprecated
aliases (removed in 3.0); new code should call the `Validation` namespace.
"""
import re
from tkinter import Misc
from typing import Any, Callable, Union

import ttkbootstrap as ttk
from ttkbootstrap.style._compat import warn_deprecated


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


# A common phone-number shape, shared by Validation.phonenumber.
_PHONE_PATTERN = r"^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$"


class Validation:
    """Namespace of input-validation rules for ``Entry``, ``Spinbox``, and
    ``Combobox``.

    Each method attaches a rule to a widget; a value that fails the rule flags
    the widget with the ttk ``invalid`` state (a ``danger``-colored border) until
    the contents become valid again. Call them like ``Validation.numeric(entry)``.

    The ``when`` argument on every method controls *when* the rule runs:

    * ``"focusout"`` — when the widget loses focus (the default)
    * ``"focusin"`` — when the widget gains focus
    * ``"focus"`` — on both focus in and focus out
    * ``"key"`` — on every keystroke, as the user types
    * ``"all"`` — in all of the above situations

    Use ``Validation.add`` for a custom rule (a function decorated with
    ``@validator``).
    """

    @staticmethod
    def add(widget: Misc, func: Callable[..., bool], when: str = "focusout", **kwargs: Any) -> None:
        """Attach a custom rule to `widget`.

        The rule `func` receives a `ValidationEvent` and returns a boolean; it is
        usually written with the `@validator` decorator. Extra keyword arguments
        are forwarded to the rule on each call (as `add_range_validation` forwards
        its bounds).

        Parameters:

            widget (Widget):
                The `Entry`, `Combobox`, or `Spinbox` to validate.

            func (Callable):
                The validation function, called on each validation event.

            when (str):
                When the rule runs. See the class docstring for the options.

            kwargs (Dict):
                Optional arguments forwarded to `func`.
        """
        f = widget.register(lambda *e: func(*e, **kwargs))
        subs = (r"%d", r"%i", r"%P", r"%s", r"%S", r"%v", r"%V", r"%W")
        widget.configure(validate=when, validatecommand=(f, *subs))

    @staticmethod
    def text(widget: Misc, when: str = "focusout") -> None:
        """Require the contents to be alphabetic (an empty field passes)."""
        Validation.add(widget, _validate_text, when=when)

    @staticmethod
    def numeric(widget: Misc, when: str = "focusout") -> None:
        """Require the contents to be numeric (an empty field passes)."""
        Validation.add(widget, _validate_number, when=when)

    @staticmethod
    def range(
        widget: Misc,
        start: Union[int, float],
        end: Union[int, float],
        when: str = "focusout",
    ) -> None:
        """Require a number within `start`–`end` inclusive (an empty field passes).

        Parameters:

            widget (Widget):
                The widget on which to add validation.

            start (int or float):
                The lower bound of the accepted range, inclusive.

            end (int or float):
                The upper bound of the accepted range, inclusive.

            when (str):
                When the rule runs. See the class docstring for the options.
        """
        Validation.add(widget, _validate_range, startrange=start, endrange=end, when=when)

    @staticmethod
    def regex(widget: Misc, pattern: str, when: str = "focusout") -> None:
        """Require the contents to match the regular expression `pattern`."""
        Validation.add(widget, _validate_regex, pattern=pattern, when=when)

    @staticmethod
    def options(widget: Misc, options: list[Any], when: str = "focusout") -> None:
        """Require the contents to be one of the values in `options`."""
        Validation.add(widget, _validate_options, options=options, when=when)

    @staticmethod
    def phonenumber(widget: Misc, when: str = "focusout") -> None:
        """Require the contents to match a common phone-number pattern."""
        Validation.add(widget, _validate_regex, pattern=_PHONE_PATTERN, when=when)


# ---------------------------------------------------------------------------
# Deprecated pre-2.0 free functions -> Validation namespace (removed in 3.0).
# ---------------------------------------------------------------------------


def add_validation(widget: Misc, func: Callable[..., bool], when: str = "focusout", **kwargs: Any) -> None:
    """Deprecated alias for `Validation.add` (removed in 3.0)."""
    warn_deprecated("add_validation()", "Validation.add()")
    Validation.add(widget, func, when=when, **kwargs)


def add_text_validation(widget: Misc, when: str = "focusout") -> None:
    """Deprecated alias for `Validation.text` (removed in 3.0)."""
    warn_deprecated("add_text_validation()", "Validation.text()")
    Validation.text(widget, when=when)


def add_numeric_validation(widget: Misc, when: str = "focusout") -> None:
    """Deprecated alias for `Validation.numeric` (removed in 3.0)."""
    warn_deprecated("add_numeric_validation()", "Validation.numeric()")
    Validation.numeric(widget, when=when)


def add_phonenumber_validation(widget: Misc, when: str = "focusout") -> None:
    """Deprecated alias for `Validation.phonenumber` (removed in 3.0)."""
    warn_deprecated("add_phonenumber_validation()", "Validation.phonenumber()")
    Validation.phonenumber(widget, when=when)


def add_regex_validation(widget: Misc, pattern: str, when: str = "focusout") -> None:
    """Deprecated alias for `Validation.regex` (removed in 3.0)."""
    warn_deprecated("add_regex_validation()", "Validation.regex()")
    Validation.regex(widget, pattern, when=when)


def add_range_validation(
    widget: Misc,
    startrange: Union[int, float],
    endrange: Union[int, float],
    when: str = "focusout",
) -> None:
    """Deprecated alias for `Validation.range` (removed in 3.0)."""
    warn_deprecated("add_range_validation()", "Validation.range()")
    Validation.range(widget, startrange, endrange, when=when)


def add_option_validation(widget: Misc, options: list[Any], when: str = "focusout") -> None:
    """Deprecated alias for `Validation.options` (removed in 3.0)."""
    warn_deprecated("add_option_validation()", "Validation.options()")
    Validation.options(widget, options, when=when)


if __name__ == "__main__":
    app = ttk.App()

    @validator
    def my_validation(event: ValidationEvent) -> bool:
        print(event.postchangetext)
        return True

    entry = ttk.Entry().pack(padx=10, pady=10)
    entry2 = ttk.Entry().pack(padx=10, pady=10)
    Validation.text(entry, when="key")  # prevents from using any numbers
    Validation.text(entry2, when="key")
    ttk.Button(text="Other").pack(padx=10, pady=10)
    app.mainloop()
