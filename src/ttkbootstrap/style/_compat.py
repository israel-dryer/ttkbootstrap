"""Compatibility quarantine for the bootstyle grammar (2.0 Workstream D/F).

Everything that translates a *legacy* bootstyle spelling into the canonical
form, and everything that decides how loudly the resolver complains about an
invalid one, lives here -- isolated from the resolver so the deprecation surface
is in one place and can be retired wholesale in 3.0.

Public-to-the-package, not to end users, except `set_bootstyle_strict` /
`is_bootstyle_strict`, which `ttkbootstrap` re-exports.
"""
import os
import warnings

# ---------------------------------------------------------------------------
# Strictness policy (Fork 1: warn by default, opt-in strict).
# ---------------------------------------------------------------------------
_TRUE = {"1", "true", "yes", "on"}
_STRICT = os.environ.get("TTKBOOTSTRAP_STRICT", "").strip().lower() in _TRUE


def set_bootstyle_strict(strict: bool = True) -> None:
    """Choose how the resolver reacts to an invalid bootstyle.

    In the default (non-strict) mode an unknown token or an unbuildable
    ``(modifier, widget)`` combination emits a ``UserWarning`` and the resolver
    falls back to a best-effort style. In strict mode the same conditions raise
    ``ValueError`` instead -- useful in tests/CI to turn typos into hard
    failures. Also settable at import via the ``TTKBOOTSTRAP_STRICT`` env var.
    """
    global _STRICT
    _STRICT = bool(strict)


def is_bootstyle_strict() -> bool:
    """Return whether strict bootstyle validation is active."""
    return _STRICT


def report_invalid(kind: str, token: str, source: str, suggestions=()) -> None:
    """Report an invalid bootstyle token/pair: raise (strict) or warn.

    Parameters:
        kind: what is wrong -- e.g. ``"token"``, ``"color"``, ``"modifier"``.
        token: the offending token (or ``"(modifier, family)"`` pair text).
        source: the original bootstyle string, for context.
        suggestions: optional near-matches to include in the message.
    """
    msg = f"invalid bootstyle {kind} {token!r} in {source!r}"
    if suggestions:
        hint = " or ".join(repr(s) for s in suggestions)
        msg += f"; did you mean {hint}?"
    msg += " (unknown tokens are ignored; see the bootstyle reference)"
    if _STRICT:
        raise ValueError(msg)
    warnings.warn(msg, UserWarning, stacklevel=3)


def warn_deprecated(old: str, new: str, *, removed_in: str = "3.0") -> None:
    """Emit the quarantine's standard deprecation warning."""
    warnings.warn(
        f"{old} is deprecated and will be removed in {removed_in}; use {new}.",
        DeprecationWarning,
        stacklevel=3,
    )


# ---------------------------------------------------------------------------
# Window/Toplevel keyword renames (2.0 shipped-widget API pass, PR B).
# ---------------------------------------------------------------------------
# The raw-Tk-mirroring constructor kwargs were renamed to snake_case. The old
# spellings are accepted through 2.x with a DeprecationWarning, removed in 3.0.
_WINDOW_KWARG_ALIASES = {
    "overrideredirect": "override_redirect",
    "windowtype": "window_type",
    "toolwindow": "tool_window",
    "hdpi": "high_dpi",
}


def normalize_window_kwargs(kwargs: dict) -> dict:
    """Pop deprecated raw-Tk-name window kwargs from ``kwargs`` in place.

    Returns a ``{new_name: value}`` dict for any legacy spelling found, emitting
    the standard deprecation warning for each. The caller merges the result over
    its explicit parameters, e.g.::

        aliases = normalize_window_kwargs(kwargs)
        high_dpi = aliases.get("high_dpi", high_dpi)
    """
    out = {}
    for old, new in _WINDOW_KWARG_ALIASES.items():
        if old in kwargs:
            warn_deprecated(f"the {old!r} window argument", f"{new!r}")
            out[new] = kwargs.pop(old)
    return out


def normalize_option_names(kwargs: dict, aliases: dict, context: str) -> dict:
    """Rename deprecated option keys in ``kwargs`` in place; warn per rename.

    Generic helper for the 2.0 custom-widget API review: a widget whose authored
    option names were snake_cased accepts the old spellings through 2.x. Any
    ``old`` key found in ``kwargs`` is popped and returned under its ``new`` name
    (with a ``DeprecationWarning``), so the caller can fold the result over its
    explicit parameters::

        opts.update(normalize_option_names(kwargs, ALIASES, "Meter"))

    Returns a ``{new_name: value}`` dict for the legacy keys found.
    """
    out = {}
    for old, new in aliases.items():
        if old in kwargs:
            warn_deprecated(f"the {old!r} {context} option", f"{new!r}")
            out[new] = kwargs.pop(old)
    return out


# Meter authored-option renames (2.0 shipped-widget API pass, PR 2).
_METER_KWARG_ALIASES = {
    "arcrange": "arc_range",
    "arcoffset": "arc_offset",
    "amountmin": "amount_min",
    "amounttotal": "amount_total",
    "amountused": "amount_used",
    "amountformat": "amount_format",
    "wedgesize": "wedge_size",
    "metersize": "meter_size",
    "metertype": "meter_type",
    "meterthickness": "meter_thickness",
    "showtext": "show_text",
    "stripethickness": "stripe_thickness",
    "textleft": "text_left",
    "textright": "text_right",
    "textfont": "text_font",
    "subtextstyle": "subtext_style",
    "subtextfont": "subtext_font",
    "stepsize": "step_size",
}


def normalize_meter_kwargs(kwargs: dict) -> dict:
    """Pop deprecated Meter option names from ``kwargs``; return ``{new: value}``."""
    return normalize_option_names(kwargs, _METER_KWARG_ALIASES, "Meter")


def normalize_meter_option(name: str) -> str:
    """Map a single legacy Meter option name to its 2.0 spelling (warns).

    Used by ``configure``/``cget``/item access so a legacy option string
    (``meter.cget("amountused")``) still resolves. Non-legacy names pass through.
    """
    new = _METER_KWARG_ALIASES.get(name)
    if new is not None:
        warn_deprecated(f"the {name!r} Meter option", f"{new!r}")
        return new
    return name


# DateEntry authored-option renames (2.0 shipped-widget API pass, PR 3).
_DATEENTRY_KWARG_ALIASES = {
    "dateformat": "date_format",
    "firstweekday": "first_weekday",
    "startdate": "start_date",
}


def normalize_dateentry_kwargs(kwargs: dict) -> dict:
    """Pop deprecated DateEntry option names from ``kwargs``; return ``{new: value}``."""
    return normalize_option_names(kwargs, _DATEENTRY_KWARG_ALIASES, "DateEntry")


def normalize_dateentry_option(name: str) -> str:
    """Map a single legacy DateEntry option name to its 2.0 spelling (warns).

    Used by ``configure``/``cget``/item access so a legacy option string
    (``dateentry.cget("dateformat")``) still resolves. Non-legacy names pass
    through unchanged.
    """
    new = _DATEENTRY_KWARG_ALIASES.get(name)
    if new is not None:
        warn_deprecated(f"the {name!r} DateEntry option", f"{new!r}")
        return new
    return name


# Date-picker dialog keyword renames (2.0 shipped-widget API pass, PR 3). The
# DateEntry rename is coordinated across the dialog layer: `Querybox.get_date`
# and `DatePickerDialog` carried the same legacy spellings.
_DATEPICKER_KWARG_ALIASES = {
    "firstweekday": "first_weekday",
    "startdate": "start_date",
}


def normalize_datepicker_kwargs(kwargs: dict) -> dict:
    """Pop deprecated date-picker kwargs from ``kwargs``; return ``{new: value}``."""
    return normalize_option_names(kwargs, _DATEPICKER_KWARG_ALIASES, "date picker")


# Floodgauge.start() signature realignment (2.0 shipped-widget API pass, PR 4).
# 2.0 realigns start() to ttk.Progressbar's start(interval); the pre-2.0
# start(step_size, interval) form is accepted through 2.x with a warning.
def normalize_floodgauge_start_args(args: list, kwargs: dict) -> tuple:
    """Resolve ``Floodgauge.start()`` arguments across the 2.x signature change.

    Returns ``(interval, step_size)``. ``step_size`` is ``None`` unless the
    legacy ``start(step_size, interval)`` form -- two positionals, or a
    ``step_size=`` keyword -- was used, in which case a ``DeprecationWarning``
    is emitted. A single positional is the new ``interval``.
    """
    interval = None
    step_size = None
    legacy = False

    if "step_size" in kwargs:
        step_size = kwargs.pop("step_size")
        legacy = True
    if "interval" in kwargs:
        interval = kwargs.pop("interval")
    if kwargs:
        raise TypeError(
            f"start() got unexpected keyword arguments: {', '.join(sorted(kwargs))}"
        )

    if len(args) >= 2:
        step_size, interval = args[0], args[1]
        legacy = True
    elif len(args) == 1:
        interval = args[0]

    if legacy:
        warn_deprecated(
            "Floodgauge.start(step_size, interval)",
            "start(interval)",
        )
    return interval, step_size


# Scrolled widget authored-option renames (2.0 shipped-widget API pass, PR 5).
# `autohide` -> `auto_hide` (ScrolledText + ScrolledFrame); `scrollheight` ->
# `scroll_height` (ScrolledFrame).
_SCROLLED_KWARG_ALIASES = {
    "autohide": "auto_hide",
    "scrollheight": "scroll_height",
}


def normalize_scrolled_kwargs(kwargs: dict) -> dict:
    """Pop deprecated Scrolled option names from ``kwargs``; return ``{new: value}``."""
    return normalize_option_names(kwargs, _SCROLLED_KWARG_ALIASES, "Scrolled")


def normalize_bootstyle(value, *, warn: bool = False) -> str:
    """Return the canonical dash-joined bootstyle string for a legacy value.

    Accepts the retired tuple/list form (``("primary", "outline")``) as well as
    a plain string, and returns a single dash-joined string the tokenizer can
    split. Slot re-ordering is handled downstream by the tokenizer, not here.

    In 2.0 D1 this is called with ``warn=False`` so the internal tuple callers
    (Meter/DateEntry/...) stay quiet until they are migrated in D2; D2 flips the
    default caller to ``warn=True`` so genuine external tuple use is flagged.
    """
    if value is None:
        return ""
    if isinstance(value, (list, tuple)):
        parts = [str(v).strip() for v in value if v is not None and str(v).strip()]
        canonical = "-".join(parts)
        if warn and parts:
            warn_deprecated(
                "passing a tuple/list bootstyle",
                f'the canonical string "{canonical}"',
            )
        return canonical
    return str(value).strip()
