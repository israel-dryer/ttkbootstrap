from __future__ import annotations

from typing import Any, Dict
from tkinter import StringVar, Misc

from ttkbootstrap.core.localization.msgcat import MessageCatalog
from ttkbootstrap.core.localization.specs import (
    LocalizedSpec,
    LocalizedTextSpec,
    LocalizedValueSpec,
)


class LocalizableWidgetMixin(Misc):
    """Mixin for widgets that support automatic text and value localization.

    This mixin enables widgets to automatically localize text and format values
    according to the current locale. It listens for locale change events and
    updates all registered fields accordingly.

    Attributes:
        localize: Controls whether literals are auto-wrapped into localization specs.
            Can be True, False, or "auto".
        value_format: Default IntlFormatter spec for non-string values (e.g., 'currency',
            'decimal', 'percent').
    """

    def __init__(self, *args, localize="auto", value_format=None, **kwargs):
        """Initialize the localizable widget mixin.

        Args:
            *args: Positional arguments passed to parent class.
            localize: Localization mode - True, False, or "auto" (default).
            value_format: Default format spec for numeric/date values.
            **kwargs: Keyword arguments passed to parent class.
        """
        super().__init__(*args, **kwargs)

        self._localized_fields: Dict[str, LocalizedSpec] = {}
        self._localize_mode = localize
        self._default_value_format = value_format

        self.bind("<<LocaleChanged>>", self._on_locale_changed, add="+")

    def register_localized_field(
        self,
        field_name: str,
        value: Any,
        *,
        value_format=None,
        localize=None,
    ) -> None:
        """Register a widget field for automatic localization.

        Args:
            field_name: The widget field name (e.g., "text", "textvariable").
            value: The value to localize. Can be a literal string/number or a LocalizedSpec.
            value_format: Optional IntlFormatter spec for non-string values (e.g., 'currency').
            localize: Override the widget's default localization mode for this field.
        """
        if value is None:
            return

        localize_mode = self._localize_mode if localize is None else localize

        if isinstance(value, LocalizedSpec):
            self._localized_fields[field_name] = value
            self._apply_spec_now(field_name, value)
            return

        if localize_mode is False:
            return

        if isinstance(value, str):
            spec = LocalizedTextSpec(key=value, original=value)
        else:
            fmt = value_format or self._default_value_format or "decimal"
            spec = LocalizedValueSpec(value=value, format_spec=fmt)

        self._localized_fields[field_name] = spec
        self._apply_spec_now(field_name, spec)

    def _apply_spec_now(self, field_name: str, spec: LocalizedSpec) -> None:
        """Resolve a localization spec using the current locale and apply immediately.

        Args:
            field_name: The widget field name to update.
            spec: The LocalizedSpec to resolve and apply.
        """
        if not spec.enabled:
            return
        locale = MessageCatalog.locale()
        value = spec.resolve(locale)
        self._apply_localized_value(field_name, value)

    def _on_locale_changed(self, event=None):
        """Handle locale change events by refreshing all localized fields.

        Args:
            event: The Tkinter event object (unused).
        """
        self._refresh_localized_fields()

    def _refresh_localized_fields(self) -> None:
        """Refresh all registered localized fields with the current locale."""
        locale = MessageCatalog.locale()
        for field_name, spec in self._localized_fields.items():
            if not spec.enabled:
                continue
            value = spec.resolve(locale)
            self._apply_localized_value(field_name, value)

    def _apply_localized_value(self, field_name: str, value: str) -> None:
        """Apply a localized value to the widget field.

        If the field is a StringVar, sets its value. Otherwise, attempts to
        configure the widget option with the given name.

        Args:
            field_name: The widget field name to update.
            value: The localized value to apply.
        """
        var = getattr(self, field_name, None)
        if isinstance(var, StringVar):
            var.set(value)
            return

        try:
            self.configure({field_name: value})
        except Exception:
            pass
