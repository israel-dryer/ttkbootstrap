"""Core widget capabilities for ttkbootstrap.

This package provides framework services that can be used by widget mixins
and other parts of the library. Each capability module contains reusable
logic that mixins delegate to, keeping the mixins themselves as thin glue.

Capabilities:
    signals: Signal/Variable binding and normalization
    localization: Text translation and value formatting
"""

from ttkbootstrap.core.capabilities.signals import (
    SignalBinding,
    is_signal,
    is_variable,
    normalize_signal,
    create_signal,
    infer_default_value_for_widget,
    query_binding,
)

from ttkbootstrap.core.capabilities.localization import (
    resolve_text,
    resolve_variable_text,
    apply_spec,
    get_current_locale,
    create_formatted_signal,
)

__all__ = [
    # Signals capability
    "SignalBinding",
    "is_signal",
    "is_variable",
    "normalize_signal",
    "create_signal",
    "infer_default_value_for_widget",
    "query_binding",
    # Localization capability
    "resolve_text",
    "resolve_variable_text",
    "apply_spec",
    "get_current_locale",
    "create_formatted_signal",
]