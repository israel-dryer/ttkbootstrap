"""Validation result container."""


class ValidationResult:
    """The outcome of a single validation check.

    Attributes:
        is_valid (bool): True if validation passed, False otherwise.
        message (str): Error message when `is_valid` is False; empty string otherwise.

    """

    def __init__(self, is_valid: bool, message: str = ""):
        """Create a validation result.

        Args:
            is_valid: True if validation passed.
            message: Error message. Defaults to an empty string.

        """
        self.is_valid = is_valid
        self.message = message

    def __bool__(self) -> bool:
        return self.is_valid
