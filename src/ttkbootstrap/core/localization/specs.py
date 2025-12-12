from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Optional, Tuple, Union

from .msgcat import MessageCatalog
from .intl_format import IntlFormatter, FormatSpec


class LocalizedSpec:
    """Base class for all localization specifications.

    Localization specs define how text or values should be localized when
    the locale changes. Subclasses implement specific localization strategies.

    Attributes:
        enabled: Whether this spec is currently enabled for localization.
    """
    enabled: bool = True

    def resolve(self, locale: str) -> str:
        """Resolve this spec to a localized string for the given locale.

        Args:
            locale: The locale code to use for resolution.

        Returns:
            The localized string value.

        Raises:
            NotImplementedError: Subclasses must implement this method.
        """
        raise NotImplementedError("Subclasses must implement resolve().")


@dataclass
class LocalizedTextSpec(LocalizedSpec):
    """Localization spec for translatable text via MessageCatalog.

    This spec translates text using gettext catalogs and MessageCatalog,
    with optional format arguments for interpolation.

    Attributes:
        key: The message ID or semantic key for translation lookup.
        fmtargs: Tuple of formatting arguments for MessageCatalog interpolation.
        original: Fallback literal text if translation fails.
        enabled: Whether this spec is currently enabled for localization.
    """
    key: str
    fmtargs: Tuple[Any, ...] = ()
    original: Optional[str] = None

    enabled: bool = True

    def resolve(self, locale: str) -> str:
        """Resolve to translated text using MessageCatalog.

        Args:
            locale: The locale code (unused, MessageCatalog uses its own state).

        Returns:
            The translated string, or the original/key as fallback.
        """
        try:
            return MessageCatalog.translate(self.key, *self.fmtargs)
        except Exception:
            return self.original or self.key


@dataclass
class LocalizedValueSpec(LocalizedSpec):
    """Localization spec for locale-aware value formatting.

    This spec formats numbers, dates, times, and currency values using
    IntlFormatter according to the current locale.

    Attributes:
        value: The value to format (number, date, datetime, time, etc.).
        format_spec: IntlFormatter spec such as "currency", "decimal", "percent",
            or a dict with formatting options.
        enabled: Whether this spec is currently enabled for localization.
    """
    value: Any
    format_spec: FormatSpec

    enabled: bool = True

    def resolve(self, locale: str) -> str:
        """Resolve to a locale-formatted string using IntlFormatter.

        Args:
            locale: The locale code (unused, uses MessageCatalog's current locale).

        Returns:
            The formatted string, or str(value) as fallback.
        """
        try:
            current_locale = MessageCatalog.locale()
            fmt = IntlFormatter(locale=current_locale)
            return fmt.format(self.value, self.format_spec)
        except Exception:
            return str(self.value)


def L(key: str, *fmtargs: Any) -> LocalizedTextSpec:
    """Create a LocalizedTextSpec for translatable text.

    Shorthand constructor that creates a text localization spec with the
    translation key and optional format arguments.

    Args:
        key: The message ID or semantic key for translation lookup.
        *fmtargs: Optional formatting arguments for string interpolation.

    Returns:
        A LocalizedTextSpec instance.

    Example:
        >>> spec = L("greeting", "World")
        >>> # Will translate "greeting" with "World" as format argument
    """
    return LocalizedTextSpec(key=key, fmtargs=fmtargs, original=key)


def LV(value: Any, format_spec: FormatSpec) -> LocalizedValueSpec:
    """Create a LocalizedValueSpec for locale-aware value formatting.

    Shorthand constructor that creates a value formatting spec for numbers,
    dates, times, and currency values.

    Args:
        value: The value to format (number, date, datetime, time, etc.).
        format_spec: IntlFormatter spec like "currency", "decimal", "percent",
            or a dict with detailed formatting options.

    Returns:
        A LocalizedValueSpec instance.

    Example:
        >>> spec = LV(1234.56, "currency")
        >>> # Will format as currency in the current locale
    """
    return LocalizedValueSpec(value=value, format_spec=format_spec)
