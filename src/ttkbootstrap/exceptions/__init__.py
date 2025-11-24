from __future__ import annotations

from typing import Optional


class TTKBootstrapError(Exception):
    """Base for all ttkbootstrap errors."""
    __slots__ = ("hint", "code", "widget_id")

    def __init__(
            self, message: str, *, hint: Optional[str] = None,
            code: Optional[str] = None, widget_id: Optional[str] = None):
        super().__init__(message)
        self.hint = hint
        self.code = code
        self.widget_id = widget_id

    def __str__(self) -> str:
        base = super().__str__()
        if self.hint:
            return f"{base} — Hint: {self.hint}"
        return base


class LayoutError(TTKBootstrapError): ...


class ThemeError(TTKBootstrapError): ...


class ConfigError(TTKBootstrapError): ...


class StateError(TTKBootstrapError): ...


class NavigationError(TTKBootstrapError): ...


class BootstyleBuilderError(TTKBootstrapError): ...


class BootstyleParsingError(TTKBootstrapError): ...

class ConfigurationWarning(Warning): ...