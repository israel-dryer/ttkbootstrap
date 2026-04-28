"""Type aliases for the signal and variable tracing system."""
from typing import Literal

TraceOperation = Literal["array", "read", "write", "unset"]
