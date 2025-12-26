"""Localization mixin for ttkbootstrap widgets.

Provides automatic text translation and value formatting based on the current
locale. Widgets using this mixin will automatically update when the locale
changes.

This mixin is a thin glue layer that delegates resolution logic to the core
localization capability module.
"""

from __future__ import annotations

from typing import Any, Dict
from tkinter import StringVar, Misc

from ttkbootstrap.core.capabilities.localization import (
    resolve_text,
    resolve_variable_text,
    apply_spec,
    get_current_locale,
    create_formatted_signal,
)
from ttkbootstrap.core.localization.specs import (
    LocalizedSpec,
    LocalizedTextSpec,
    LocalizedValueSpec,
)
from ttkbootstrap.runtime.app import get_app_settings


class LocalizationMixin(Misc):
    """Mixin for widgets that support automatic text and value localization.

    This mixin enables widgets to automatically localize text and format values
    according to the current locale. It listens for locale change events and
    updates all registered fields accordingly.

    This mixin delegates resolution logic to the core localization capability.

    Attributes:
        localize: Controls whether literals are auto-wrapped into localization specs.
            Can be True, False, or "auto".
        value_format: Default IntlFormatter spec for non-string values (e.g., 'currency',
            'decimal', 'percent').
    """

    def __init__(self, *args, **kwargs):
        """Initialize the localizable widget mixin.

        This mixin intercepts localization-related kwargs. It inspects 'text'
        for localization without consuming it, so it can be passed to the
        underlying widget. It consumes 'localize' and 'value_format' as they
        are not standard ttk options.
        """
        # Determine the localization mode. A widget-specific 'localize' argument
        # overrides the global app setting. This argument is consumed from kwargs.
        localize = kwargs.pop('localize', get_app_settings().localize_mode)
        value_format = kwargs.pop('value_format', None)

        # Get 'text' for localization without removing it from kwargs.
        text_to_localize = kwargs.get('text')

        # Call the next class in the MRO with the remaining kwargs.
        # 'text' is still in kwargs for the underlying widget to use.
        super().__init__(*args, **kwargs)

        # --- Post-init setup ---
        self._localized_fields: Dict[str, LocalizedSpec] = {}
        self._localize_mode = localize
        self._default_value_format = value_format

        root = self.winfo_toplevel()  # event is generated on root
        root.bind("<<LocaleChanged>>", self._on_locale_changed, add="+")

        # Check if widget has a textsignal or textvariable with value_format
        if value_format and self._has_signal_or_variable():
            self._setup_signal_formatting(value_format)
        else:
            # Register the text field for static localization
            self.register_localized_field('text', text_to_localize, value_format=value_format)

    def _has_signal_or_variable(self) -> bool:
        """Check if the widget has a textsignal, textvariable, or configured textvariable.

        Returns:
            True if any signal/variable binding exists.
        """
        if hasattr(self, '_textsignal') or hasattr(self, '_textvariable'):
            return True
        try:
            textvariable_name = self.cget('textvariable')
            return bool(textvariable_name)
        except Exception:
            return False

    def register_localized_field(
        self,
        field_name: str,
        value: Any,
        *,
        value_format: str | None = None,
        localize: bool | str | None = None,
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

        if isinstance(value, str) and value == "":
            return

        localize_mode = self._localize_mode if localize is None else localize

        # If already a spec, use it directly
        if isinstance(value, LocalizedSpec):
            self._localized_fields[field_name] = value
            self._apply_spec_now(field_name, value)
            return

        if localize_mode is False:
            return

        # Resolve the value to a spec using core capability
        if isinstance(value, str):
            spec = resolve_text(value, localize_mode=localize_mode)
        else:
            spec = resolve_variable_text(
                value,
                value_format=value_format,
                default_format=self._default_value_format or "decimal",
            )

        if spec is not None:
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
        value = apply_spec(spec)
        self._apply_localized_value(field_name, value)

    def _on_locale_changed(self, event=None):
        """Handle locale change events by refreshing all localized fields.

        Args:
            event: The Tkinter event object (unused).
        """
        self._refresh_localized_fields()

        # If we have signal formatting, trigger a re-format with new locale
        if hasattr(self, '_signal_formatter'):
            value_format, formatter, source_signal = self._signal_formatter
            # Re-format current value from source signal with new locale
            formatter(source_signal.get())

    def _refresh_localized_fields(self) -> None:
        """Refresh all registered localized fields with the current locale."""
        for field_name, spec in self._localized_fields.items():
            if not spec.enabled:
                continue
            value = apply_spec(spec)
            self._apply_localized_value(field_name, value)

    def _setup_signal_formatting(self, value_format: str) -> None:
        """Subscribe to textsignal and format its values.

        When formatting is enabled, this creates a private textvariable for this widget
        and subscribes to the source signal to format and display values independently.

        Args:
            value_format: The format spec (e.g., 'currency', 'decimal').
        """
        # Ensure textsignal exists (triggers lazy creation if needed)
        if not hasattr(self, '_textsignal'):
            _ = self.textsignal

        # Save reference to the source signal (the one we're subscribing to)
        source_signal = self._textsignal

        # Create formatted signal using core capability
        formatted_signal, formatter = create_formatted_signal(source_signal, value_format)

        # Update our internal references to use the new private signal/variable
        self._textsignal = formatted_signal
        self._textvariable = formatted_signal.var

        # Configure widget to use the new private variable
        try:
            self._ttk_base.configure(self, textvariable=self._textvariable)  # type: ignore[misc]
        except Exception:
            pass

        # Store references for locale changes
        self._signal_formatter = (value_format, formatter, source_signal)

    def _apply_localized_value(self, field_name: str, value: str) -> None:
        """Apply a localized value to the widget field.

        Checks for associated textvariable/variable first to ensure proper
        integration with textsignal/signal reactive bindings. Falls back to
        direct widget configuration if no variable is found.

        Args:
            field_name: The widget field name to update.
            value: The localized value to apply.
        """
        # Check if field has a direct attribute (less common)
        var = getattr(self, field_name, None)
        if isinstance(var, StringVar):
            var.set(value)
            return

        # Check for textvariable (for 'text' field)
        if field_name == 'text':
            # Try cached _textvariable first
            if hasattr(self, '_textvariable') and self._textvariable:
                self._textvariable.set(value)
                return

            # Try to get textvariable from widget configuration
            try:
                textvariable_name = self.cget('textvariable')
                if textvariable_name:
                    # Get the actual variable object via the property
                    self.textvariable.set(value)
                    return
            except Exception:
                pass

        # Check for variable (for 'value' or other fields)
        if hasattr(self, '_variable') and self._variable and field_name != 'text':
            self._variable.set(value)
            return

        # Fallback: configure the widget option directly
        try:
            self.configure({field_name: value})
        except Exception:
            pass


__all__ = ["LocalizationMixin"]