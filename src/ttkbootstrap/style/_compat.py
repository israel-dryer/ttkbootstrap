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
