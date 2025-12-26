from __future__ import annotations

import hashlib
import platform
import re
from dataclasses import dataclass
from tkinter import Misc, font as tkfont
from tkinter.font import Font as TkFont
from typing import Any, Literal, NamedTuple


# =============================================================================
# Token model
# =============================================================================

class FontSpec(NamedTuple):
    font: str
    size: int
    weight: Literal["normal", "bold"]
    underline: bool = False
    slant: Literal["roman", "italic"] = "roman"
    overstrike: bool = False


class FontTokenNames:
    # Base families
    caption = "caption"
    label = "label"
    body_sm = "body-sm"
    body = "body"
    body_lg = "body-lg"
    body_xl = "body-xl"

    heading_md = "heading-md"
    heading_lg = "heading-lg"
    heading_xl = "heading-xl"

    display_lg = "display-lg"
    display_xl = "display-xl"

    code = "code"
    hyperlink = "hyperlink"


class FontTokens(NamedTuple):
    caption: FontSpec
    label: FontSpec
    body_sm: FontSpec
    body: FontSpec
    body_lg: FontSpec
    body_xl: FontSpec

    heading_md: FontSpec
    heading_lg: FontSpec
    heading_xl: FontSpec

    display_lg: FontSpec
    display_xl: FontSpec

    code: FontSpec
    hyperlink: FontSpec


# =============================================================================
# Defaults
# =============================================================================

def _clamp_base_size(base_size: int) -> int:
    # keep sizes sane; your existing file had a similar constraint
    return max(8, min(int(base_size), 14))


def build_desktop_tokens(
    *,
    family: str | None = None,
    mono_family: str | None = None,
    base_size: int = 11,
) -> FontTokens:
    """
    Construct default typography tokens tuned for desktop UI.
    """
    base = _clamp_base_size(base_size)

    system = platform.system().lower()
    if system == "windows":
        default_ui = "Segoe UI"
        default_mono = "Cascadia Mono"
    elif system == "darwin":
        default_ui = "SF Pro Text"
        default_mono = "SF Mono"
    else:
        default_ui = "DejaVu Sans"
        default_mono = "DejaVu Sans Mono"

    ui = family or default_ui
    mono = mono_family or default_mono

    # Scale helpers
    def s(delta: int) -> int:
        return base + delta

    return FontTokens(
        caption=FontSpec(ui, s(-1), "normal"),
        label=FontSpec(ui, s(-2), "bold"),
        body_sm=FontSpec(ui, s(-1), "normal"),
        body=FontSpec(ui, s(0), "normal"),
        body_lg=FontSpec(ui, s(1), "normal"),
        body_xl=FontSpec(ui, s(2), "normal"),

        heading_md=FontSpec(ui, s(1), "bold"),
        heading_lg=FontSpec(ui, s(2), "bold"),
        heading_xl=FontSpec(ui, s(3), "bold"),

        display_lg=FontSpec(ui, s(4), "bold"),
        display_xl=FontSpec(ui, s(5), "bold"),

        code=FontSpec(mono, s(0), "normal"),
        hyperlink=FontSpec(ui, s(0), "normal", underline=True),
    )


DEFAULT_FONT_TOKENS = build_desktop_tokens()

FALLBACK_FONT = "TkDefaultFont"
FALLBACK_MONO = "TkFixedFont"


TK_FONT_OVERRIDES = {
    # Make Tk defaults align with desktop expectations / your token system
    "TkDefaultFont": FontTokenNames.body,
    "TkTextFont": FontTokenNames.body,
    "TkHeadingFont": FontTokenNames.heading_md,
    "TkCaptionFont": FontTokenNames.caption,
    "TkFixedFont": FontTokenNames.code,
}


# =============================================================================
# Typography registry (named fonts)
# =============================================================================

class Typography:
    """
    Named-font registry for tokenized typography.

    - Call Typography.init(root) once.
    - Token fonts become named Tk fonts (e.g. "body", "heading-lg"...)
    - Tk defaults are overridden (TkDefaultFont, etc.) to match tokens.
    """

    _root: Misc | None = None
    _fonts: FontTokens = DEFAULT_FONT_TOKENS
    _use_fallback: bool = False
    _named_fonts: dict[str, TkFont] = {}

    @classmethod
    def initialize(cls, root: Misc | None = None) -> None:
        if root is not None:
            cls._root = root
        cls._ensure_named_token_fonts()
        cls._override_tk_fonts()

    @classmethod
    def use_fonts(cls, fonts: FontTokens, *, fallback: bool = False) -> None:
        cls._fonts = fonts
        cls._use_fallback = bool(fallback)
        cls._ensure_named_token_fonts()
        cls._override_tk_fonts()

    @classmethod
    def set_global_family(cls, family: str) -> None:
        """
        Update all font tokens to use a single family (except monospace).
        """
        updated = {}
        for name, spec in cls._fonts._asdict().items():
            if name == "code":
                updated[name] = spec
            else:
                updated[name] = FontSpec(
                    family,
                    spec.size,
                    spec.weight,
                    spec.underline,
                    spec.slant,
                    spec.overstrike,
                )
        cls.use_fonts(FontTokens(**updated), fallback=True)

    @classmethod
    def get_token(cls, name: str) -> FontSpec:
        """
        Return the FontSpec for a token name.
        """
        # allow passing "body-sm" etc.
        # map token string to field name
        field = name.replace("-", "_")
        if hasattr(cls._fonts, field):
            return getattr(cls._fonts, field)
        raise KeyError(f"Unknown font token: {name}")

    @classmethod
    def token_names(cls) -> set[str]:
        return {
            v for k, v in FontTokenNames.__dict__.items()
            if not k.startswith("_") and isinstance(v, str)
        }

    @classmethod
    def get_named_token_font(cls, token_name: str) -> TkFont:
        """
        Return the named Tk font for a token.
        """
        if token_name not in cls._named_fonts:
            cls._ensure_named_token_fonts()
        # If it's still missing, try to resolve as Tk named font directly:
        return cls._named_fonts.get(token_name) or TkFont(name=token_name, exists=True)

    @classmethod
    def update_font_token(cls, name: str, **kwargs: Any) -> None:
        """
        Replace the given token with updated fields (NamedTuple-safe).
        """
        field = name.replace("-", "_")
        if not hasattr(cls._fonts, field):
            raise KeyError(f"Unknown font token: {name}")

        old: FontSpec = getattr(cls._fonts, field)
        new = old._replace(**kwargs)
        # rebuild the FontTokens instance
        data = cls._fonts._asdict()
        data[field] = new
        cls.use_fonts(FontTokens(**data), fallback=cls._use_fallback)

    @classmethod
    def _ensure_named_token_fonts(cls) -> None:
        """
        Create/update named Tk fonts for every token.
        """
        for token_name, spec in cls._iter_tokens():
            fallback = FALLBACK_MONO if token_name == FontTokenNames.code else FALLBACK_FONT

            family = spec.font if not cls._use_fallback else fallback

            if token_name in tkfont.names():
                f = tkfont.nametofont(token_name)
                f.configure(
                    family=family,
                    size=spec.size,
                    weight=spec.weight,
                    slant=spec.slant,
                    underline=bool(spec.underline),
                    overstrike=bool(spec.overstrike),
                )
            else:
                f = TkFont(
                    name=token_name,
                    family=family,
                    size=spec.size,
                    weight=spec.weight,
                    slant=spec.slant,
                    underline=bool(spec.underline),
                    overstrike=bool(spec.overstrike),
                )
            cls._named_fonts[token_name] = f

    @classmethod
    def _override_tk_fonts(cls) -> None:
        """
        Override Tk’s default named fonts to align with tokens.
        """
        for tk_name, token_name in TK_FONT_OVERRIDES.items():
            spec = cls.get_token(token_name)
            fallback = FALLBACK_MONO if token_name == FontTokenNames.code else FALLBACK_FONT
            family = spec.font if not cls._use_fallback else fallback

            if tk_name in tkfont.names():
                tkfont.nametofont(tk_name).configure(
                    family=family,
                    size=spec.size,
                    weight=spec.weight,
                    slant=spec.slant,
                )

    @classmethod
    def _iter_tokens(cls):
        d = cls._fonts._asdict()
        for field_name, spec in d.items():
            token_name = field_name.replace("_", "-")
            yield token_name, spec


# =============================================================================
# Public Font abstraction (token + modifiers -> named Tk font)
# =============================================================================

_BRACKET_RE = re.compile(r"\[([^]]+)]")


@dataclass(frozen=True)
class FontModifierSpec:
    token: str
    size: int | None = None          # absolute override
    size_delta: int = 0              # "+1"/"-1" after token
    weight: str | None = None        # "bold"|"normal"
    slant: str | None = None         # "italic"|"roman"
    underline: bool | None = None
    overstrike: bool | None = None

    def key(self) -> tuple:
        return (
            self.token,
            self.size,
            self.size_delta,
            self.weight,
            self.slant,
            self.underline,
            self.overstrike,
        )


_DERIVED_FONTS: dict[tuple, TkFont] = {}


def _hash(parts: Any) -> str:
    return hashlib.md5(repr(parts).encode("utf-8")).hexdigest()[:10]


def parse_font(value: str, *, default_token: str = FontTokenNames.body) -> FontModifierSpec:
    """
    Parse:
      "body[bold]"
      "heading-lg+1[italic][underline]"
      "[16][bold]"  -> default token + size/mods

    Brackets can contain:
      - size: 16, 16px
      - modifiers: bold, normal, italic, roman, underline, overstrike
      - comma/space separated lists: [bold, italic]
    """
    s = (value or "").strip()
    if not s:
        return FontModifierSpec(default_token)

    head = s.split("[", 1)[0].strip()
    mods = _BRACKET_RE.findall(s)

    token = default_token
    size_delta = 0

    if head:
        # allow token+delta like "body+1" or "body-2"
        m = re.match(r"^\s*([^+\-]+?)\s*([+-])\s*(\d+)\s*$", head)
        if m:
            token = m.group(1).strip() or default_token
            sign = m.group(2)
            n = int(m.group(3))
            size_delta = n if sign == "+" else -n
        else:
            token = head

    size: int | None = None
    weight: str | None = None
    slant: str | None = None
    underline: bool | None = None
    overstrike: bool | None = None

    for raw in mods:
        part = raw.strip()
        if not part:
            continue

        bits = [b.strip().lower() for b in re.split(r"[,\s]+", part) if b.strip()]
        for b in bits:
            if b.endswith("px") and b[:-2].isdigit():
                size = -int(b[:-2])
            elif b.isdigit():
                size = int(b)
            elif b in ("bold", "normal"):
                weight = b
            elif b in ("italic", "roman"):
                slant = b
            elif b == "underline":
                underline = True
            elif b in ("no-underline", "nounderline"):
                underline = False
            elif b in ("overstrike", "strike", "strikethrough"):
                overstrike = True
            elif b in ("no-overstrike", "no-strike", "nostrike"):
                overstrike = False

    return FontModifierSpec(
        token=token,
        size=size,
        size_delta=size_delta,
        weight=weight,
        slant=slant,
        underline=underline,
        overstrike=overstrike,
    )


def resolve_modifier_font(spec: FontModifierSpec) -> TkFont:
    """
    Resolve a modifier spec to a named, cached TkFont.
    """
    key = spec.key()
    cached = _DERIVED_FONTS.get(key)
    if cached is not None:
        return cached

    # If token exists in our system, prefer it; otherwise treat as Tk named font
    try:
        base = Typography.get_named_token_font(spec.token)
    except Exception:
        base = TkFont(name=spec.token, exists=True)

    actual = base.actual()

    cfg: dict[str, Any] = {
        "family": actual.get("family"),
        "size": actual.get("size"),
        "weight": actual.get("weight", "normal"),
        "slant": actual.get("slant", "roman"),
        "underline": int(actual.get("underline", 0) or 0),
        "overstrike": int(actual.get("overstrike", 0) or 0),
    }

    if spec.size is not None:
        cfg["size"] = spec.size
    if spec.size_delta:
        cfg["size"] = int(cfg.get("size") or 0) + spec.size_delta

    if spec.weight is not None:
        cfg["weight"] = spec.weight
    if spec.slant is not None:
        cfg["slant"] = spec.slant
    if spec.underline is not None:
        cfg["underline"] = 1 if spec.underline else 0
    if spec.overstrike is not None:
        cfg["overstrike"] = 1 if spec.overstrike else 0

    # If nothing changed, return base
    if (
        spec.size is None
        and spec.size_delta == 0
        and spec.weight is None
        and spec.slant is None
        and spec.underline is None
        and spec.overstrike is None
    ):
        _DERIVED_FONTS[key] = base
        return base

    name = f"ttkbootstrap.font.{_hash(key)}"
    try:
        f = TkFont(name=name, exists=True)
        f.configure(**cfg)
    except Exception:
        f = TkFont(name=name, **cfg)

    _DERIVED_FONTS[key] = f
    return f


class Font:
    """
    Public, reusable typography primitive.

    Works with the same inline syntax you already allow on widgets:
      Font("body[bold]")
      Font("heading-lg+1[italic]")
      Font("[16][bold]")            # default token + size/mods
      Font("Segoe UI[14][bold]")    # explicit family + mods

    Can be passed directly to Tk widgets:
      ttk.Label(..., font=Font("body[bold]"))

    Measurement helpers:
      Font(...).measure("text")
      Font(...).metrics(...)
    """

    __slots__ = ("spec", "_tkfont")

    def __init__(self, value: str, *, default_token: str = FontTokenNames.body):
        self.spec = parse_font(value, default_token=default_token)
        self._tkfont: TkFont | None = None

    @property
    def tkfont(self) -> TkFont:
        if self._tkfont is None:
            self._tkfont = resolve_modifier_font(self.spec)
        return self._tkfont

    @property
    def name(self) -> str:
        return str(self.tkfont)

    def measure(self, text: str) -> int:
        return int(self.tkfont.measure(text))

    def metrics(self, *args, **kwargs):
        return self.tkfont.metrics(*args, **kwargs)

    def actual(self, *args, **kwargs):
        return self.tkfont.actual(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


def get_font(value: str, *, default_token: str = FontTokenNames.body) -> Font:
    """
    Convenience factory:
      get_font("body[bold]")
    """
    return Font(value, default_token=default_token)
