"""Typography helpers over the standard Tk named fonts.

A small utility for the FAQ that had no answer before 2.0 -- "how do I change
the global font?" -- built on the **standard Tk named fonts** every interpreter
already ships (`TkDefaultFont`, `TkTextFont`, `TkFixedFont`, ...). Because every
widget reads those fonts, retinting them restyles the whole app with zero
interception, and `font="TkHeadingFont"` keeps working on stock tkinter
widgets. There is no ttkbootstrap font vocabulary and no bracket DSL -- a
parallel `body`/`heading-lg` token set would be overhead to document and sync
for no payoff (see the boundary rule in the compat & utilities design note).

Two surfaces:

- `Fonts` -- a namespace of classmethods operating on the *live* root:
  `set_global_family` / `configure` / `describe` / `names` / `create_alias` /
  `reset`. Each needs an interpreter, so call them after `App()` exists.
- `set_global_family(family, *, mono_family=None)` -- the headline one-liner as
  a **module-level** function that rides the deferred-config seam (Slice 5): set
  it at the top of a file before `App()` and it applies when the root comes up;
  if a root already exists it applies live.
"""
import tkinter
from tkinter import font
from typing import Any, Optional

# The standard Tk named fonts. The proportional set is retinted together by
# `set_global_family(family=...)`; `TkFixedFont` is the monospace font and gets
# `mono_family` instead. Some names (Tooltip/Icon/SmallCaption) are absent on
# some platforms -- lookups guard for that -- so this is the *canonical* set, not
# a promise every one exists in a given interpreter.
PROPORTIONAL_FONTS = (
    "TkDefaultFont",
    "TkTextFont",
    "TkMenuFont",
    "TkHeadingFont",
    "TkCaptionFont",
    "TkSmallCaptionFont",
    "TkIconFont",
    "TkTooltipFont",
)
MONOSPACE_FONTS = ("TkFixedFont",)

# Cache of `font.Font` wrappers keyed by named-font name. Wrappers pin a Tcl
# interpreter, so a wrapper cached against a root that was later destroyed is
# stale; `_named_font` re-fetches when the interpreter no longer matches, and
# `Fonts.reset()` (wired into `App.destroy`) clears the cache proactively.
_font_cache: "dict[str, font.Font]" = {}


def _named_font(name: str) -> font.Font:
    """Return the `font.Font` wrapper for named font `name` on the live root."""
    # local import breaks the utils <- window import chain (window imports the
    # style package, which imports utils) -- fonts is imported eagerly by
    # utils/__init__, so it must not pull in window at module load.
    from ttkbootstrap.window import get_default_root

    root = get_default_root()
    cached = _font_cache.get(name)
    if cached is not None and cached._tk is root.tk:
        return cached
    resolved = font.nametofont(name, root=root)
    _font_cache[name] = resolved
    return resolved


class Fonts:
    """Namespace of typography helpers over the standard Tk named fonts.

    Every method operates on the live application root, so call them once `App()`
    exists. For the pre-root "set it at the top of the file" case use the
    module-level `set_global_family`, which rides the deferred-config seam.
    """

    @classmethod
    def set_global_family(cls, family: str, *, mono_family: Optional[str] = None) -> None:
        """Retint every proportional named font to `family` in one call.

        The headline typography one-liner: because widgets read the standard
        named fonts, this restyles the whole app. `TkFixedFont` (the monospace
        font, used by `Text`/console-style widgets) is left alone unless
        `mono_family` is given. Named fonts absent on the current platform are
        skipped.
        """
        for name in PROPORTIONAL_FONTS:
            try:
                _named_font(name).configure(family=family)
            except tkinter.TclError:
                continue  # not present on this platform
        if mono_family is not None:
            for name in MONOSPACE_FONTS:
                try:
                    _named_font(name).configure(family=mono_family)
                except tkinter.TclError:
                    continue

    @classmethod
    def configure(cls, name: str, **opts: Any) -> None:
        """Tweak a single named font (`family`/`size`/`weight`/`slant`/...).

        Thin wrapper over `font.nametofont(name).configure(**opts)`; the change
        is seen live by every widget that reads that named font.
        """
        _named_font(name).configure(**opts)

    @classmethod
    def create_alias(cls, name: str, **opts: Any) -> font.Font:
        """Register a user named font `name` and return its `font.Font`.

        A convenience over `font.Font(name=name, ...)` so an app can define its
        own named font once and refer to it by name (`font="Body"`) everywhere,
        the same seam the standard `Tk*Font` names use. Returns the wrapper for
        further tweaking; re-registering a name reconfigures it.
        """
        from ttkbootstrap.window import get_default_root

        root = get_default_root()
        if name in font.names(root):
            # already registered -> reconfigure rather than error on duplicate
            alias = font.nametofont(name, root=root)
            if opts:
                alias.configure(**opts)
        else:
            alias = font.Font(root=root, name=name, exists=False, **opts)
        _font_cache[name] = alias
        return alias

    @classmethod
    def names(cls) -> "tuple[str, ...]":
        """Return the standard named fonts this utility manages (see `describe`)."""
        return PROPORTIONAL_FONTS + MONOSPACE_FONTS

    @classmethod
    def describe(cls, name: Optional[str] = None) -> dict:
        """Return each named font's resolved family/size/weight/slant/... .

        With `name`, return the one font's actual options; otherwise a mapping of
        every managed named font (from `names()`) to its actual options. The
        "see what the fonts actually are" helper; fonts absent on the platform
        are omitted from the full mapping.
        """
        if name is not None:
            return dict(_named_font(name).actual())
        result = {}
        for n in cls.names():
            try:
                result[n] = dict(_named_font(n).actual())
            except tkinter.TclError:
                continue
        return result

    @classmethod
    def reset(cls) -> None:
        """Drop the cached `font.Font` wrappers.

        Called from `App.destroy` so wrappers pinned to a destroyed root are not
        reused by a later root (the same singleton/root-rebind hazard `Style`
        clears). The named fonts themselves live in the interpreter and die with
        it; this only clears our Python-side cache.
        """
        _font_cache.clear()


def set_global_family(family: str, *, mono_family: Optional[str] = None) -> None:
    """Set the global proportional (and, optionally, monospace) font family.

    Called **before** `App()` exists, the setting is queued and applied when the
    root is created (the intended top-of-file use). If a root already exists it
    applies immediately. `mono_family`, when given, retints `TkFixedFont` too.

    This is the deferred-config-seam sibling of `set_locale` /
    `set_default_button`; for live tweaks against an existing root call
    `Fonts.set_global_family` / `Fonts.configure` directly.
    """
    # local import breaks the utils.fonts <- utils.config <- style cycle; the
    # seam applies now if a root exists, else queues under "global_family".
    from ttkbootstrap.utils import config

    config.defer(
        "global_family",
        lambda: Fonts.set_global_family(family, mono_family=mono_family),
    )
