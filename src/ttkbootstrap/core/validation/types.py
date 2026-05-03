"""Type definitions for widget validation rules."""
from typing import Callable, Literal, Optional, TypedDict

RuleType = Literal["required", "email", "pattern", "stringLength", "custom"]
RuleTriggerType = Literal['key', 'blur', 'always', 'manual']


class ValidationOptions(TypedDict, total=False):
    """Options dictionary for configuring a validation rule."""

    pattern: str
    message: str
    min: int
    max: int
    trigger: Optional[Literal["key", "blur", "always", "manual"]]
    func: Callable[[str], bool]