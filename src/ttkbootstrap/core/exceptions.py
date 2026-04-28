from __future__ import annotations

from typing import Optional


class TTKBootstrapError(Exception):
    """Base for all ttkbootstrap errors."""
    __slots__ = ("hint", "code", "widget_id")

    def __init__(
            self, message: str, *, hint: Optional[str] = None,
            code: Optional[str] = None, widget_id: Optional[str] = None):
        """Create a ttkbootstrap error.

        Args:
            message: Human-readable description of what went wrong.
            hint: Optional suggestion for how to resolve the error.
            code: Optional machine-readable error code for programmatic handling.
            widget_id: Optional Tk widget path string identifying the source widget.
        """
        super().__init__(message)
        self.hint = hint
        self.code = code
        self.widget_id = widget_id

    def __str__(self) -> str:
        base = super().__str__()
        if self.hint:
            return f"{base} — Hint: {self.hint}"
        return base


class LayoutError(TTKBootstrapError):
    """Raised when a widget layout operation fails.

    Examples: invalid geometry manager usage, pane configuration errors,
    or attempting to pack/grid/place a widget into an incompatible container.
    """


class ThemeError(TTKBootstrapError):
    """Raised when a theme-related operation fails.

    Examples: requesting an unknown theme name, loading a malformed theme
    definition, or applying a theme before the style system is initialised.
    """


class ConfigError(TTKBootstrapError):
    """Raised when a widget or application configuration is invalid.

    Examples: passing mutually exclusive options, supplying an unsupported
    value for a configuration key, or configuring a widget after it has
    been destroyed.
    """


class StateError(TTKBootstrapError):
    """Raised when an operation is attempted while the widget is in an invalid state.

    Examples: calling `start()` on an already-running animation, or
    modifying a widget that has been destroyed.
    """


class NavigationError(TTKBootstrapError):
    """Raised when a navigation operation fails.

    Examples: referencing a tab key that does not exist, supplying an index
    that is out of range, or navigating in a container that has no items.
    """


class BootstyleBuilderError(TTKBootstrapError):
    """Raised when a style builder encounters an error during style construction.

    Examples: a builder receiving an unsupported option, a required theme
    color token being missing, or an internal style-engine failure.
    """


class BootstyleParsingError(TTKBootstrapError):
    """Raised when a bootstyle string cannot be parsed into valid tokens.

    Examples: an unrecognised accent name, an invalid variant, or a
    combination of tokens that the parser cannot resolve.
    """


class ConfigurationWarning(Warning):
    """Issued when a widget receives a deprecated or questionable configuration option.

    Examples: passing the legacy `bootstyle` keyword instead of the
    recommended `accent`/`variant` pair.
    """