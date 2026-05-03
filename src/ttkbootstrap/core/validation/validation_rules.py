"""Built-in validation rule implementations."""
import re
from typing import Callable

from ttkbootstrap.core.validation.types import RuleTriggerType, RuleType
from ttkbootstrap.core.validation.validation_result import ValidationResult


class ValidationRule:
    """A single validation rule that can be applied to a string value.

    Supports the built-in rule types `'required'`, `'email'`, `'stringLength'`,
    `'pattern'`, and `'custom'`, and carries a trigger
    policy that controls when the rule is evaluated.

    Attributes:
        type (RuleType): The validation rule type.
        message (str): Custom error message; if empty a default is generated.
        trigger (RuleTriggerType): When the rule fires — `'always'`, `'blur'`, or `'manual'`.
        params (dict): Additional parameters specific to the rule type
            (e.g., `min`/`max` for `'stringLength'`, `pattern` for `'pattern'`,
            `func` for `'custom'`).

    """

    def __init__(
            self,
            rule_type: RuleType,
            message: str = "",
            **kwargs
    ):
        r"""Create a validation rule.

        Args:
            rule_type: The type of validation to apply.
            message: Custom error message. If empty, a sensible default is used.
            **kwargs: Rule-specific parameters.  Pass `trigger` to override the
                default trigger policy; all other keys are stored in `params`
                (e.g., `min=3, max=20` for `'stringLength'`, `pattern=r'\d+'`
                for `'pattern'`, `func=callable` for `'custom'`).

        """
        self.type = rule_type
        self.message = message
        self.trigger = kwargs.pop('trigger', self._default_trigger())
        self.params = kwargs

    def validate(self, value: str) -> ValidationResult:
        """Apply this rule to a value and return the result.

        Args:
            value: The string value to validate.

        Returns:
            A ValidationResult with `is_valid=True` on success or `is_valid=False`
            with an error message on failure.

        """
        msg = self.message or self._default_message()

        if self.type == "required":
            if value is None:
                return ValidationResult(False, msg)
            if isinstance(value, str) and not value.strip():
                return ValidationResult(False, msg)
            # Everything else is valid (non-empty string, number, date, etc.)
            return ValidationResult(True, "")

        elif self.type == "email":
            if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
                return ValidationResult(False, msg)
        elif self.type == "stringLength":
            min_len = self.params.get("min", 0)
            max_len = self.params.get("max", float("inf"))
            if not (min_len <= len(value) <= max_len):
                return ValidationResult(False, msg)
        elif self.type == "pattern":
            pattern = self.params.get("pattern", "")
            if not re.match(pattern, value):
                return ValidationResult(False, msg)
        elif self.type == "custom":
            func: Callable[[str], bool] = self.params.get("func")
            if func and not func(value):
                return ValidationResult(False, msg)

        return ValidationResult(True)

    def _default_message(self) -> str:
        """Return a sensible default error message for this rule type."""
        if self.type == "required":
            return "This field is required."
        elif self.type == "email":
            return "Enter a valid email address."
        elif self.type == "stringLength":
            min_len = self.params.get("min", 0)
            max_len = self.params.get("max", None)
            if max_len is None or max_len == float("inf"):
                return f"Enter at least {min_len} characters."
            return f"Enter between {min_len} and {max_len} characters."
        elif self.type == "pattern":
            return "Value does not match the required pattern."
        elif self.type == "custom":
            return "Invalid value."
        return "Invalid input."

    def _default_trigger(self) -> RuleTriggerType:
        """Return the default trigger policy for this rule type."""
        if self.type == "required":
            return "always"
        elif self.type in {"stringLength"}:
            return "blur"
        elif self.type in {"email", "pattern"}:
            return "always"
        elif self.type in {"custom"}:
            return "manual"
        return "blur"
