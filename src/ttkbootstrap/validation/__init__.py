"""Shim exposing validation helpers via the core layer."""

from ttkbootstrap.core.validation.validation_rules import ValidationRule
from ttkbootstrap.core.validation.validation_result import ValidationResult

__all__ = ["ValidationRule", "ValidationResult"]
