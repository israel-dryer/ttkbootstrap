from __future__ import annotations

import ast
import tkinter


class SetVar(tkinter.Variable):
    """
    A tkinter variable that holds a set of values.

    This variable serializes a Python set into its string representation
    for storage and deserializes it back into a set on retrieval.
    """

    def __init__(self, master=None, value: set | None = None, name: str | None = None):
        """
        Initialize the SetVar.

        Args:
            master (Widget, optional): The parent widget. Defaults to None.
            value (set, optional): The initial value. Defaults to an empty set.
            name (str, optional): The name of the variable. Defaults to None.
        """
        if value is None:
            value = set()
        super().__init__(master, value, name)

    def set(self, value: set | frozenset):
        """
        Set the variable to a new value.

        The value is converted to its string representation for storage.

        Args:
            value (set | frozenset): The new value. Should be a set or frozenset.
        """
        if not isinstance(value, (set, frozenset)):
            raise TypeError(f"Expected set or frozenset, got {type(value).__name__}")
        super().set(repr(value))

    def get(self) -> set:
        """
        Return the value of the variable as a Python set.

        The string representation is deserialized back into a set.

        Returns:
            set: The current value of the variable.
        """
        value_str = super().get()
        if not value_str:
            return set()

        try:
            # Use literal_eval for safe evaluation of the string representation
            deserialized_value = ast.literal_eval(value_str)
            if isinstance(deserialized_value, (set, frozenset)):
                return set(deserialized_value)
            else:
                return set()
        except (ValueError, SyntaxError):
            return set()
