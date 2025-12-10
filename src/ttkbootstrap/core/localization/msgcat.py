"""Localization bridge for ttkbootstrap.

This module integrates Python gettext catalogs (compiled with Babel) with
Tcl/Tk's native msgcat. It preserves ttkbootstrap's existing msgcat-facing
APIs while enabling gettext-powered translations and runtime locale switching.

Key behaviors:
- Prefer gettext (.mo) translations when available, with Python '%' formatting.
- Fall back to Tcl msgcat for formatting (supports legacy placeholders like
  '%1$s') and for untranslated strings.
- Keep runtime overrides set via set/set_many in sync with msgcat and
  consult them first during translation.
- Auto-discover a 'locales/' directory for catalogs unless overridden.

Public API (unchanged signatures):
- MessageCatalog.translate(src, *fmtargs) -> str
- MessageCatalog.locale(newlocale: Optional[str] = None) -> str
- MessageCatalog.preferences() -> list[str]
- MessageCatalog.load(dirname) -> int
- MessageCatalog.set(locale, src, translated=None) -> None
- MessageCatalog.set_many(locale, *args) -> int
- MessageCatalog.max(*src) -> int
- MessageCatalog.init(root=None, locales_dir=None, domain='messages',
  default_locale='en', strip_ampersands=True) -> None
"""

from __future__ import annotations

import gettext
from os import PathLike
from pathlib import Path
from typing import Any, Optional, Union



class MessageCatalog:
    """Facade that unifies gettext and Tcl msgcat for ttkbootstrap.

    Manages the active locale, a gettext translator, and runtime overrides.
    Translation prefers gettext when available and falls back to Tcl msgcat
    for both translation and printf-style formatting.
    """
    # --- internal state for gettext bridge ---
    _inited: bool = False
    _locales_dir: Path | None = None
    _domain: str = "messages"
    _locale: str = "en"
    _gt: gettext.NullTranslations | None = None
    _strip_amp: bool = True
    _emit_event: bool = True
    _event_name: str = "<<LocaleChanged>>"

    # runtime overrides (compatible with your existing set/set_many usage)
    _overrides: dict[str, dict[str, str]] = {}

    # -------------- setup -------------------------------------------------

    @staticmethod
    def init(
            root=None,
            locales_dir: Union[str, Path, None] = None,
            domain: str = "messages",
            default_locale: str = "en",
            strip_ampersands: bool = True,
            emit_virtual_event: bool = True,
            virtual_event_name: str = "<<LocaleChanged>>",
    ) -> None:
        """Initialize the translation system.

        Args:
            root: Optional Tk root to ensure msgcat is available.
            locales_dir: Base directory containing gettext catalogs
                (``<lang>/LC_MESSAGES/<domain>.mo``). If ``None``, the
                directory is auto-discovered.
            domain: Gettext domain name.
            default_locale: Locale to activate after initialization.
            strip_ampersands: If true, remove mnemonic ``&`` markers.
            emit_virtual_event: If true, generate a Tk virtual event after
                locale changes so widgets can refresh themselves.
            virtual_event_name: The virtual event name to emit when the
                locale changes (default ``"<<LocaleChanged>>"``).
        """
        # Ensure a Tk exists so msgcat calls work even if root is omitted
        from ttkbootstrap.runtime.app import get_default_root
        _ = root or get_default_root()

        MessageCatalog._domain = domain
        MessageCatalog._locales_dir = Path(locales_dir) if locales_dir else MessageCatalog._discover_locales_dir()
        MessageCatalog._strip_amp = strip_ampersands
        MessageCatalog._emit_event = bool(emit_virtual_event)
        MessageCatalog._event_name = str(virtual_event_name or "<<LocaleChanged>>")
        MessageCatalog._install_gettext(default_locale)
        MessageCatalog._sync_msgcat_locale(default_locale)
        MessageCatalog._inited = True

    # -------------- core helpers -----------------------------------------

    @staticmethod
    def _install_gettext(lang: str) -> None:
        """Install gettext catalogs for the requested language.

        Prefers an exact match (e.g. ``de_DE``) and falls back to base
        language (``de``) if available.

        Args:
            lang: Requested locale code.
        """
        MessageCatalog._locale = MessageCatalog._normalize_lang(lang)
        # Try exact match, then base language (e.g., de_DE -> de)
        langs = [MessageCatalog._locale]
        if "_" in MessageCatalog._locale:
            langs.append(MessageCatalog._locale.split("_", 1)[0])
        try:
            MessageCatalog._gt = gettext.translation(
                MessageCatalog._domain,
                localedir=str(MessageCatalog._locales_dir or "locales"),
                languages=langs,
                fallback=True,
            )
        except Exception:
            # fallback=True already returns a NullTranslations if not found
            MessageCatalog._gt = gettext.NullTranslations()

    @staticmethod
    def _discover_locales_dir() -> Path:
        """Return a plausible locales directory for this installation.

        Priority order:
        1) ``TTKBOOTSTRAP_LOCALES`` environment variable
        2) Repository root ``locales/``
        3) Package-local ``ttkbootstrap/locales``
        4) Current working directory ``./locales``
        """
        import os
        env = os.environ.get("TTKBOOTSTRAP_LOCALES")
        if env:
            p = Path(env)
            if p.exists():
                return p
        here = Path(__file__).resolve()
        candidates = [
            here.parents[1] / "assets" / "locales",     # in-package assets: ttkbootstrap/assets/locales
            here.parent / "locales",                     # module-local: ttkbootstrap/localization/locales
            here.parents[1] / "locales",                 # package-local: ttkbootstrap/locales
            here.parents[3] / "locales",                 # repo root: .../ttkbootstrap/locales
            Path.cwd() / "locales",                      # current working dir
        ]
        for c in candidates:
            try:
                if c.exists() and c.is_dir() and any(
                        (c / d.name / "LC_MESSAGES").exists() for d in c.iterdir() if d.is_dir()):
                    return c
            except Exception:
                pass
        return here.parents[3] / "locales"

    @staticmethod
    def _sync_msgcat_locale(lang: str) -> None:
        """Set Tcl msgcat locale to match the Python-side locale.

        Args:
            lang: Locale code (e.g. ``en``, ``de_DE``).
        """
        root = get_default_root()

        tcl_lang = MessageCatalog._to_msgcat_locale(lang)
        try:
            root.tk.call("::msgcat::mclocale", tcl_lang)
        except Exception:
            pass

    @staticmethod
    def _normalize_lang(code: str) -> str:
        """Normalize a locale code to gettext style (``ll`` or ``ll_RR``).

        Args:
            code: Input locale code (e.g. ``de-de``, ``pt_br``).

        Returns:
            Normalized locale code for gettext use.
        """
        if not code:
            return "en"
        parts = code.replace("-", "_").split("_")
        return parts[0].lower() if len(parts) == 1 else f"{parts[0].lower()}_{parts[1].upper()}"

    @staticmethod
    def _to_msgcat_locale(code: str) -> str:
        """Normalize a locale code to msgcat style (``ll`` or ``ll_rr``).

        Args:
            code: Input locale code (e.g. ``de-DE``, ``pt_BR``).

        Returns:
            Lowercased region code used by msgcat.
        """
        parts = code.replace("-", "_").split("_")
        return parts[0].lower() if len(parts) == 1 else f"{parts[0].lower()}_{parts[1].lower()}"

    @staticmethod
    def __join(*args: Any) -> str:
        """Join format args for Tcl msgcat formatting.

        Args:
            *args: Positional values to forward to Tcl 'format'.

        Returns:
            String of brace-wrapped arguments joined by spaces.
        """
        new_args = []
        for arg in args:
            if isinstance(arg, str):
                stripped = str(arg).strip('"')
                new_args.append("{%s}" % stripped)
            else:
                new_args.append(str(arg))
        return " ".join(new_args)

    @staticmethod
    def _strip_ampersands(s: str) -> str:
        """Remove mnemonic ampersands from text.

        Converts single '&' markers to nothing and turns '&&' into a
        literal '&'. Useful for rendering toolkit-agnostic text.

        Args:
            s: Input string.

        Returns:
            Cleaned string with mnemonic indicators removed.
        """
        if not s or "&" not in s:
            return s
        out = []
        i = 0
        while i < len(s):
            if s[i] == "&":
                if i + 1 < len(s) and s[i + 1] == "&":
                    out.append("&")
                    i += 2
                else:
                    i += 1  # skip mnemonic marker
            else:
                out.append(s[i])
                i += 1
        return "".join(out)

    # -------------- public API (unchanged signatures) ---------------------

    @staticmethod
    def translate(src: str, *fmtargs: Any) -> str:
        """Translate a message id according to the active locale.

        Strategy:
        1) If a runtime override exists and formatting args are provided,
           use Tcl msgcat so legacy '%1$s' placeholders work.
        2) Otherwise use overrides (with Python '%' formatting when args
           are given).
        3) Next, try gettext; if Python '%' formatting fails, fall back
           to Tcl formatting.
        4) Finally, fall back entirely to Tcl msgcat.

        Args:
            src: Message id to translate.
            *fmtargs: Positional formatting values.

        Returns:
            Localized and formatted string.
        """
        from ttkbootstrap.runtime.app import get_default_root
        root = get_default_root()

        # Fast-path: if an override exists for this locale and formatting args were
        # provided, prefer Tcl msgcat formatting so positional specifiers like %1$s
        # work as in legacy behavior.
        cur = MessageCatalog._locale
        if fmtargs and cur in MessageCatalog._overrides and src in MessageCatalog._overrides[cur]:
            command = f"::msgcat::mc {{{src}}} {MessageCatalog.__join(*fmtargs)}"
            out = root.tk.eval(command)
            return MessageCatalog._strip_ampersands(out) if MessageCatalog._strip_amp else out

        # 1) overrides for current locale win first
        cur = MessageCatalog._locale
        if cur in MessageCatalog._overrides and src in MessageCatalog._overrides[cur]:
            s = MessageCatalog._overrides[cur][src]
            if MessageCatalog._strip_amp:
                s = MessageCatalog._strip_ampersands(s)
            # try Python formatting if args were passed; ignore on failure
            if fmtargs:
                try:
                    s = s % fmtargs
                    return s
                except Exception:
                    pass
            # no args or failed → return override as-is
            return s

        # 2) gettext translation (if inited)
        if MessageCatalog._inited and MessageCatalog._gt is not None:
            try:
                s = MessageCatalog._gt.gettext(src)
                # If gettext returns src unchanged, and we have no fmtargs,
                # we'll consider falling back to msgcat for consistency.
                if s != src:
                    if MessageCatalog._strip_amp:
                        s = MessageCatalog._strip_ampersands(s)
                    if fmtargs:
                        try:
                            return s % fmtargs
                        except Exception:
                            # fall through to Tcl formatting
                            pass
                    else:
                        return s
            except Exception:
                # ignore and fall back to msgcat
                pass

        # 3) Tcl msgcat fallback (preserves your current behavior exactly)
        command = f"::msgcat::mc {{{src}}}"
        if fmtargs:
            command = f"{command} {MessageCatalog.__join(*fmtargs)}"
        out = root.tk.eval(command)
        return MessageCatalog._strip_ampersands(out) if MessageCatalog._strip_amp else out

    @staticmethod
    def locale(newlocale: Optional[str] = None) -> str:
        """Get or set the current locale.

        Args:
            newlocale: If provided, switch both gettext and msgcat locales.

        Returns:
            The active normalized locale code (or Tcl's current code when
            queried).
        """
        root = get_default_root()
        if newlocale:
            # switch gettext + msgcat
            MessageCatalog._install_gettext(newlocale)
            MessageCatalog._sync_msgcat_locale(newlocale)
            # notify listeners (optional)
            try:
                if MessageCatalog._emit_event:
                    root.event_generate(MessageCatalog._event_name, when="tail")
            except Exception:
                pass
            return MessageCatalog._locale
        # query Tcl msgcat current locale
        return root.tk.eval("::msgcat::mclocale")

    @staticmethod
    def preferences() -> list[str]:
        """Return Tcl msgcat locale preferences (ordered)."""
        from ttkbootstrap.runtime.app import get_default_root
        root = get_default_root()
        items = root.tk.eval("::msgcat::mcpreferences").split(" ")
        return items[0:-1] if len(items) > 0 else []

    @staticmethod
    def load(dirname: Union[str, PathLike[str]]) -> int:
        """Load Tcl .msg catalogs from a directory.

        Args:
            dirname: Directory containing msgcat .msg files.

        Returns:
            Number of files loaded, as reported by Tcl.
        """
        msgs = Path(dirname).as_posix()
        root = get_default_root()
        return int(root.tk.eval(f"::msgcat::mcload [list {msgs}]"))

    @staticmethod
    def set(locale: str, src: str, translated: Optional[str] = None) -> None:
        """Define a single runtime translation and mirror it into msgcat.

        Args:
            locale: Target locale code.
            src: Message id.
            translated: Localized string.
        """
        loc = MessageCatalog._normalize_lang(locale)
        MessageCatalog._overrides.setdefault(loc, {})[src] = translated or ""
        root = get_default_root()
        root.tk.eval("::msgcat::mcset %s {%s} {%s}" % (MessageCatalog._to_msgcat_locale(locale), src, translated or ""))

    @staticmethod
    def set_many(locale: str, *args: str) -> int:
        """Bulk-define runtime translations and mirror into msgcat.

        Args:
            locale: Target locale code.
            *args: Alternating message ids and translations.

        Returns:
            Number of messages set, as reported by Tcl.
        """
        loc = MessageCatalog._normalize_lang(locale)
        # update Python overrides
        pairs = list(args)
        for i in range(0, len(pairs), 2):
            k = pairs[i]
            v = pairs[i + 1] if i + 1 < len(pairs) else ""
            MessageCatalog._overrides.setdefault(loc, {})[k] = v

        # update Tcl msgcat
        root = get_default_root()
        messages = " ".join(["{%s}" % x for x in args])
        out = f"::msgcat::mcmset {MessageCatalog._to_msgcat_locale(locale)} {{{messages}}}"
        return int(root.tk.eval(out))

    @staticmethod
    def max(*src: str) -> int:
        root = get_default_root()
        return int(root.tk.eval(f"::msgcat::mcmax {' '.join(src)}"))

