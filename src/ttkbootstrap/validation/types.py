from typing import Callable, Literal, Optional, TypedDict

RuleType = Literal["required", "email", "pattern", "stringLength", "custom", "compare"]
RuleTriggerType = Literal['key', 'blur', 'always', 'manual']


class ValidationOptions(TypedDict, total=False):
    pattern: str
    message: str
    min: int
    max: int
    trigger: Optional[Literal["key", "blur", "always", "manual"]]
    func: Callable[[str], bool]