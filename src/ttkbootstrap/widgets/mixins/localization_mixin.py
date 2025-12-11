from __future__ import annotations

from typing import Any, Dict
from tkinter import StringVar, Misc

from ttkbootstrap.core.localization.msgcat import MessageCatalog
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
        if value_format and (hasattr(self, '_textsignal') or hasattr(self, '_textvariable') or self._has_textvariable_configured()):
            # Ensure textsignal exists (triggers lazy creation if needed)
            if not hasattr(self, '_textsignal'):
                # Access the property to trigger lazy creation
                _ = self.textsignal
            # Subscribe to signal and format its values
            self._setup_signal_formatting(value_format)
        else:
            # Register the text field for static localization
            self.register_localized_field('text', text_to_localize, value_format=value_format)

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

        # If we have signal formatting, trigger a re-format with new locale
        if hasattr(self, '_signal_formatter'):
            value_format, formatter, source_signal = self._signal_formatter
            # Re-format current value from source signal with new locale
            formatter(source_signal.get())

    def _refresh_localized_fields(self) -> None:
        """Refresh all registered localized fields with the current locale."""
        locale = MessageCatalog.locale()
        for field_name, spec in self._localized_fields.items():
            if not spec.enabled:
                continue
            value = spec.resolve(locale)
            self._apply_localized_value(field_name, value)

    def _has_textvariable_configured(self) -> bool:
        """Check if the widget has a textvariable configured.

        Returns:
            True if a textvariable is configured on the widget.
        """
        try:
            textvariable_name = self.cget('textvariable')
            return bool(textvariable_name)
        except Exception:
            return False

    def _setup_signal_formatting(self, value_format: str) -> None:
        """Subscribe to textsignal and format its values.

        When formatting is enabled, this creates a private textvariable for this widget
        and subscribes to the source signal to format and display values independently.

        Args:
            value_format: The format spec (e.g., 'currency', 'decimal')
        """
        # Save reference to the source signal (the one we're subscribing to)
        source_signal = self._textsignal

        # Create a NEW private textvariable for formatted display
        # This ensures multiple widgets can share the same source without conflict
        from ttkbootstrap.core.signals import Signal
        formatted_signal = Signal("")

        # Update our internal references to use the new private signal/variable
        self._textsignal = formatted_signal
        self._textvariable = formatted_signal.var

        # Configure widget to use the new private variable
        try:
            self._ttk_base.configure(self, textvariable=self._textvariable)  # type: ignore[misc]
        except:
            pass

        def format_signal_value(value):
            """Format the signal value using current locale."""
            # Create a spec for this value
            spec = LocalizedValueSpec(value=value, format_spec=value_format)
            locale = MessageCatalog.locale()
            formatted = spec.resolve(locale)

            # Update the private textvariable for this widget
            formatted_signal.set(formatted)

        # Subscribe to the SOURCE signal (not our new private one!)
        source_signal.subscribe(format_signal_value, immediate=True)

        # Store references for locale changes
        self._signal_formatter = (value_format, format_signal_value, source_signal)

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
