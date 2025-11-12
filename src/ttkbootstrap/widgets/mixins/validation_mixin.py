from __future__ import annotations

from collections import deque
from tkinter import TclError
from tkinter.ttk import Widget
from typing import Any, Callable, Optional

from ttkbootstrap.validation import ValidationRule
from ttkbootstrap.validation.types import RuleTriggerType, RuleType, ValidationOptions


class ValidationMixin(Widget):
    """
    Pure-Tkinter validation mixin for bound widgets.

    - Debounced auto-validate on key/blur
    - Emits virtual events with payload:
        <<Tkb-Valid>>, <<Tkb-Invalid>>, <<Tkb-Validated>>
    - Payload is retrieved via get_event_payload(event_name)
    """

    EVENT_VALID = '<<Tkb-Valid>>'
    EVENT_INVALID = '<<Tkb-Invalid>>'
    EVENT_VALIDATED = '<<Tkb-Validated>>'
    SEQ_KEYUP = '<KeyRelease>'
    SEQ_BLUR = '<FocusOut>'

    def __init__(self, *args, **kwargs):
        # Validation rules
        self._rules: list[ValidationRule] = []

        # Per-event payload queues and state
        self._emit_queue: dict[str, deque[dict[str, Any]]] = {
            self.EVENT_VALID: deque(),
            self.EVENT_INVALID: deque(),
            self.EVENT_VALIDATED: deque(),
        }
        self._emit_flushing: dict[str, bool] = {
            self.EVENT_VALID: False,
            self.EVENT_INVALID: False,
            self.EVENT_VALIDATED: False,
        }
        self._payload_by_event: dict[str, dict[str, Any]] = {
            self.EVENT_VALID: {},
            self.EVENT_INVALID: {},
            self.EVENT_VALIDATED: {},
        }

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
        """Default value accessor; override for non-Entry widgets."""
        if hasattr(self, 'get'):
            try:
                return self.get()
            except AttributeError:
                return None
        return None

    def add_validation_rule(self, rule_type: RuleType, **kwargs: ValidationOptions) -> None:
        """Add a single validation rule."""
        self._rules.append(ValidationRule(rule_type, **kwargs))

    def add_validation_rules(self, rules: list[ValidationRule]) -> None:
        """Replace all validation rules."""
        self._rules = list(rules)

    def validate(self, value: Any, trigger: RuleTriggerType = "manual") -> bool:
        """
        Run validation rules against a raw/model value.
        Emits events with payload when rules run.
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
                self._emit_with_payload(self.EVENT_INVALID, payload)
                self._emit_with_payload(self.EVENT_VALIDATED, payload)
                return False

        if ran_rule:
            self._emit_with_payload(self.EVENT_VALID, payload)
            self._emit_with_payload(self.EVENT_VALIDATED, payload)

        return ran_rule

    def get_event_payload(self, event_name: str) -> dict[str, Any]:
        """Read the most recent payload for a given virtual event."""
        return dict(self._payload_by_event.get(event_name, {}))

    # Optional: ergonomic callback registration
    def on_invalid(self, func: Callable[[dict[str, Any]], None]) -> None:
        self._on_invalid_command = func

    def on_valid(self, func: Callable[[dict[str, Any]], None]) -> None:
        self._on_valid_command = func

    def on_validated(self, func: Callable[[dict[str, Any]], None]) -> None:
        self._on_validated_command = func

    # ---------------- Internals ----------------

    def _setup_validation_binds(self, keyup_delay_ms: int = 50, blur_delay_ms: int = 50) -> None:
        # Auto-validate (debounced)
        self.bind(self.SEQ_KEYUP, lambda e: self._debounced("key", keyup_delay_ms), add=True)
        self.bind(self.SEQ_BLUR, lambda e: self._debounced("blur", blur_delay_ms), add=True)

        # Wire optional convenience callbacks if set later
        self.bind(self.EVENT_VALIDATED, self._dispatch_validated, add=True)
        self.bind(self.EVENT_VALID, self._dispatch_valid, add=True)
        self.bind(self.EVENT_INVALID, self._dispatch_invalid, add=True)

    def _debounced(self, trigger: RuleTriggerType, ms: int) -> None:
        key = f"debounce:{trigger}"
        aid: Optional[str] = self._debounce_ids.get(key)
        if aid:
            try:
                self.after_cancel(aid)
            except TclError:
                pass
        # defer reading value until the timer fires
        self._debounce_ids[key] = self.after(ms, self.validate, self.value(), trigger)

    # ----- payload queue management -----

    def _emit_with_payload(self, event_name: str, payload: dict[str, Any]) -> None:
        """Queue payload for the specific virtual event name."""
        self._emit_queue[event_name].append(dict(payload))  # copy for isolation
        if not self._emit_flushing[event_name]:
            self._emit_flushing[event_name] = True
            # Use partial to keep type checkers happy
            self.after_idle(self._flush_event_queue, event_name)

    def _flush_event_queue(self, event_name: str) -> None:
        """Emit one payload per idle tick for each event name."""
        try:
            if not self._emit_queue[event_name]:
                return

            payload = self._emit_queue[event_name].popleft()
            self._payload_by_event[event_name] = payload
            self.event_generate(event_name, when="tail")

            # Clear exactly this payload dict after handlers have run
            self.after_idle(payload.clear)

            # If more items remain, schedule another idle tick
            if self._emit_queue[event_name]:
                self.after_idle(self._flush_event_queue, event_name)
        finally:
            if not self._emit_queue[event_name]:
                self._emit_flushing[event_name] = False

    # ----- optional dispatchers for on_* convenience -----

    def _dispatch_validated(self, _) -> None:
        if self._on_validated_command:
            self._on_validated_command(self.get_event_payload(self.EVENT_VALIDATED))

    def _dispatch_valid(self, _) -> None:
        if self._on_valid_command:
            self._on_valid_command(self.get_event_payload(self.EVENT_VALID))

    def _dispatch_invalid(self, _) -> None:
        if self._on_invalid_command:
            self._on_invalid_command(self.get_event_payload(self.EVENT_INVALID))
