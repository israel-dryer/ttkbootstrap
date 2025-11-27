"""Validation mixin for widgets with enhanced event system.

This mixin provides validation functionality using the enhanced event system
that allows passing data directly through virtual events.
"""

from __future__ import annotations

from tkinter import TclError
from tkinter.ttk import Widget
from typing import Any, Callable, Optional

from ttkbootstrap.validation import ValidationRule
from ttkbootstrap.validation.types import RuleTriggerType, RuleType, ValidationOptions


class ValidationMixin(Widget):
    """Pure-Tkinter validation mixin for bound widgets.

    Features:
        - Debounced auto-validate on key/blur
        - Emits virtual events with data payload:
            <<Valid>>, <<Invalid>>, <<Validated>>
        - Event data accessible via event.data in handlers

    Events:
        <<Valid>>: Fired when validation passes
            event.data = {"value": Any, "is_valid": True, "message": str}

        <<Invalid>>: Fired when validation fails
            event.data = {"value": Any, "is_valid": False, "message": str}

        <<Validated>>: Fired after any validation
            event.data = {"value": Any, "is_valid": bool, "message": str}

    Example:
        ```python
        import ttkbootstrap as ttk
        from ttkbootstrap.widgets.parts import TextEntryPart

        root = ttk.Window()
        entry = TextEntryPart(root)
        entry.pack()

        # Add validation rules
        entry.add_validation_rule('required', message='Field is required')
        entry.add_validation_rule('min_length', min_length=5, message='Min 5 chars')

        # Bind to validation events
        def on_invalid(event):
            print(f"Invalid: {event.data['message']}")

        entry.bind('<<Invalid>>', on_invalid)
        root.mainloop()
        ```
    """

    EVENT_VALID = '<<Valid>>'
    EVENT_INVALID = '<<Invalid>>'
    EVENT_VALIDATED = '<<Validated>>'
    SEQ_KEYUP = '<KeyRelease>'
    SEQ_BLUR = '<FocusOut>'

    def __init__(self, *args, **kwargs):
        """Initialize validation mixin."""
        # Validation rules
        self._rules: list[ValidationRule] = []

        # Debounce tracking
        self._debounce_ids: dict[str, str] = {}

        # Optional convenience callbacks
        self._on_invalid_command: Optional[Callable[[dict[str, Any]], None]] = None
        self._on_valid_command: Optional[Callable[[dict[str, Any]], None]] = None
        self._on_validated_command: Optional[Callable[[dict[str, Any]], None]] = None

        super().__init__(*args, **kwargs)  # next in MRO must be a Tk/ttk widget
        self._setup_validation_binds()

    # ---------------- Public API ----------------

    def value(self) -> Any:
        """Default value accessor; override for non-Entry widgets.

        Returns:
            Current widget value
        """
        if hasattr(self, 'get'):
            try:
                return self.get()
            except AttributeError:
                return None
        return None

    def add_validation_rule(self, rule_type: RuleType, **kwargs: ValidationOptions) -> None:
        """Add a single validation rule.

        Args:
            rule_type: Type of validation rule (e.g., 'required', 'min_length')
            **kwargs: Rule-specific options (e.g., min_length=5, message='...')

        Example:
            ```python
            entry.add_validation_rule('required', message='Field is required')
            entry.add_validation_rule('email', message='Invalid email')
            ```
        """
        self._rules.append(ValidationRule(rule_type, **kwargs))

    def add_validation_rules(self, rules: list[ValidationRule]) -> None:
        """Replace all validation rules.

        Args:
            rules: List of ValidationRule objects

        Example:
            ```python
            from ttkbootstrap.validation import ValidationRule

            rules = [
                ValidationRule('required'),
                ValidationRule('min_length', min_length=5)
            ]
            entry.add_validation_rules(rules)
            ```
        """
        self._rules = list(rules)

    def validate(self, value: Any, trigger: RuleTriggerType = "manual") -> bool:
        """Run validation rules against a value.

        Emits <<Valid>>, <<Invalid>>, and <<Validated>> events
        with data payload containing validation results.

        Args:
            value: Value to validate
            trigger: Trigger type ('manual', 'key', 'blur', or 'always')

        Returns:
            True if validation was performed (regardless of result)

        Example:
            ```python
            is_valid = entry.validate(entry.value(), trigger='manual')
            ```
        """
        ran_rule = False
        payload: dict[str, Any] = {"value": value, "is_valid": True, "message": ""}

        for rule in self._rules:
            if trigger != "manual" and rule.trigger not in ("always", trigger):
                continue

            ran_rule = True
            result = rule.validate(value)
            payload.update(is_valid=result.is_valid, message=result.message)

            if not result.is_valid:
                # Emit invalid and validated events with data
                self.event_generate(self.EVENT_INVALID, data=payload)
                self.event_generate(self.EVENT_VALIDATED, data=payload)
                return False

        if ran_rule:
            # Emit valid and validated events with data
            self.event_generate(self.EVENT_VALID, data=payload)
            self.event_generate(self.EVENT_VALIDATED, data=payload)

        return ran_rule

    # Optional: ergonomic callback registration
    def on_invalid(self, func: Callable[[dict[str, Any]], None]) -> None:
        """Register callback for invalid validation.

        Args:
            func: Callback receiving validation data dict

        Example:
            ```python
            def handle_invalid(data):
                print(f"Invalid: {data['message']}")

            entry.on_invalid(handle_invalid)
            ```
        """
        self._on_invalid_command = func

    def on_valid(self, func: Callable[[dict[str, Any]], None]) -> None:
        """Register callback for valid validation.

        Args:
            func: Callback receiving validation data dict

        Example:
            ```python
            def handle_valid(data):
                print(f"Valid: {data['value']}")

            entry.on_valid(handle_valid)
            ```
        """
        self._on_valid_command = func

    def on_validated(self, func: Callable[[dict[str, Any]], None]) -> None:
        """Register callback for any validation (valid or invalid).

        Args:
            func: Callback receiving validation data dict

        Example:
            ```python
            def handle_validated(data):
                if data['is_valid']:
                    print("Validation passed")
                else:
                    print(f"Validation failed: {data['message']}")

            entry.on_validated(handle_validated)
            ```
        """
        self._on_validated_command = func

    # ---------------- Internals ----------------

    def _setup_validation_binds(self, keyup_delay_ms: int = 50, blur_delay_ms: int = 50) -> None:
        """Set up automatic validation bindings with debouncing."""
        # Auto-validate (debounced)
        self.bind(self.SEQ_KEYUP, lambda e: self._debounced("key", keyup_delay_ms), add=True)
        self.bind(self.SEQ_BLUR, lambda e: self._debounced("blur", blur_delay_ms), add=True)

        # Wire optional convenience callbacks
        self.bind(self.EVENT_VALIDATED, self._dispatch_validated, add=True)
        self.bind(self.EVENT_VALID, self._dispatch_valid, add=True)
        self.bind(self.EVENT_INVALID, self._dispatch_invalid, add=True)

    def _debounced(self, trigger: RuleTriggerType, ms: int) -> None:
        """Debounce validation to avoid excessive checks during typing."""
        key = f"debounce:{trigger}"
        aid: Optional[str] = self._debounce_ids.get(key)
        if aid:
            try:
                self.after_cancel(aid)
            except TclError:
                pass
        # defer reading value until the timer fires
        self._debounce_ids[key] = self.after(ms, self.validate, self.value(), trigger)

    # ----- optional dispatchers for on_* convenience -----

    def _dispatch_validated(self, event) -> None:
        """Dispatch validated event to registered callback."""
        if self._on_validated_command:
            self._on_validated_command(event.data)

    def _dispatch_valid(self, event) -> None:
        """Dispatch valid event to registered callback."""
        if self._on_valid_command:
            self._on_valid_command(event.data)

    def _dispatch_invalid(self, event) -> None:
        """Dispatch invalid event to registered callback."""
        if self._on_invalid_command:
            self._on_invalid_command(event.data)
