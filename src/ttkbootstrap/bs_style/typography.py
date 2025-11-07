from __future__ import annotations

import platform
from tkinter import Misc, font
from tkinter.font import Font
from typing import Literal, NamedTuple


class FontSpec(NamedTuple):
    font: str
    size: int
    weight: Literal["normal", "bold"]


class FontTokenNames:
    display_xl = "display-xl"
    display_lg = "display-lg"
    heading_xl = "heading-xl"
    heading_lg = "heading-lg"
    heading_md = "heading-md"
    body_xl = "body-xl"
    body_lg = "body-lg"
    body = "body"
    body_sm = "body-sm"
    label = "label"
    caption = "caption"
    code = "code"


class FontTokens(NamedTuple):
    display_xl: FontSpec
    display_lg: FontSpec
    heading_xl: FontSpec
    heading_lg: FontSpec
    heading_md: FontSpec
    body_xl: FontSpec
    body_lg: FontSpec
    body: FontSpec
    body_sm: FontSpec
    label: FontSpec
    caption: FontSpec
    code: FontSpec


def system_fallback_font() -> str:
    # Tk on mac maps UI defaults to Helvetica; "San Francisco" isn't a real family name here.
    return {
        "Windows": "Segoe UI",
        "Darwin": "Helvetica",
    }.get(platform.system(), "Ubuntu")


def system_monospace_font() -> str:
    return {
        "Windows": "Consolas",
        "Darwin": "Menlo",
    }.get(platform.system(), "DejaVu Sans Mono")


FALLBACK_FONT = system_fallback_font()
FALLBACK_MONO = system_monospace_font()


def build_tokens_from_base(base_size: int, family: str | None = None, mono_family: str | None = None) -> FontTokens:
    """Build font tokens from a specific base size and optional font families.

    Args:
        base_size: Base font size (typically 9-14)
        family: Font family for UI elements (defaults to system fallback)
        mono_family: Font family for code (defaults to system monospace)

    Returns:
        FontTokens with computed size ramp
    """
    # Guard rails: keep within 8..14 for sanity
    base = max(8, min(int(base_size), 14))

    ui = family or FALLBACK_FONT
    mono = mono_family or FALLBACK_MONO

    return FontTokens(
        # Display / Headings: compact vs web
        display_xl=FontSpec(ui, base + 10, "bold"),
        display_lg=FontSpec(ui, base + 8, "bold"),
        heading_xl=FontSpec(ui, base + 6, "bold"),
        heading_lg=FontSpec(ui, base + 4, "bold"),
        heading_md=FontSpec(ui, base + 2, "bold"),
        # Body / Label / Caption
        body_xl=FontSpec(ui, base + 3, "normal"),
        body_lg=FontSpec(ui, base + 2, "normal"),
        body=FontSpec(ui, base + 1, "normal"),  # ≈ main text
        body_sm=FontSpec(ui, base, "normal"),
        label=FontSpec(ui, base, "bold"),
        caption=FontSpec(ui, base - 1, "normal"),
        # Code
        code=FontSpec(mono, base, "normal"),
    )


def build_desktop_tokens() -> FontTokens:
    """Build a desktop-appropriate ramp based on TkDefaultFont size."""
    base = font.nametofont("TkDefaultFont").cget("size")
    # Guard rails: keep within 8..14 for sanity if environment reports something odd
    base = max(8, min(int(base), 14))

    return build_tokens_from_base(base)


# Use a dynamic default set
DEFAULT_FONT_TOKENS = build_desktop_tokens()

TK_FONT_OVERRIDES = {
    # Make Tk defaults align with desktop expectations
    "TkDefaultFont": "body",
    "TkTextFont": "body",
    "TkHeadingFont": "heading-md",
    "TkCaptionFont": "caption",
    "TkFixedFont": "code",
}


class Typography:
    _fonts: FontTokens = DEFAULT_FONT_TOKENS
    _use_fallback: bool = False
    _root: Misc
    _named_fonts: dict[str, Font] = {}

    @classmethod
    def use_fonts(cls, fonts: FontTokens | None = None, *, fallback: bool = False) -> None:
        """Apply a complete font token set (or rebuild from Tk defaults)."""
        cls._fonts = fonts or build_desktop_tokens()
        cls._use_fallback = fallback
        cls._register_fonts()
        cls._override_tk_fonts()

    @classmethod
    def set_global_family(cls, family: str) -> None:
        """Update all font tokens to use a single family (except monospace)."""
        updated = {
            name: FontSpec(
                family if name != "code" else cls._fonts.code.font,
                spec.size,
                spec.weight)
            for name, spec in cls._fonts._asdict().items()
        }
        cls.use_fonts(FontTokens(**updated), fallback=True)

    @classmethod
    def update_font_token(cls, name: str, **kwargs) -> None:
        """Replace the given token with updated fields (NamedTuple-safe)."""
        attr = name.replace("-", "_")
        old = getattr(cls._fonts, attr)
        new_spec = old._replace(**kwargs)
        new_map = cls._fonts._asdict()
        new_map[attr] = new_spec
        cls._fonts = FontTokens(**new_map)  # <-- replace whole tuple
        cls._register_fonts()
        if name in TK_FONT_OVERRIDES.values():
            cls._override_tk_fonts()

    @classmethod
    def get_token(cls, name: str) -> FontSpec:
        attr = name.replace("-", "_")
        return getattr(cls._fonts, attr, cls._fonts.body)

    @classmethod
    def get_font(cls, name: str) -> Font:
        spec = cls.get_token(name)
        fallback = FALLBACK_MONO if name == "code" else FALLBACK_FONT
        return Font(
            name=name,
            family=spec.font if not cls._use_fallback else fallback,
            size=spec.size,
            weight=spec.weight,
        )

    @classmethod
    def all(cls) -> FontTokens:
        return cls._fonts

    @classmethod
    def initialize_from_appconfig(cls) -> None:
        """Initialize typography from AppConfig if font is set.

        If AppConfig.font is configured, this will rebuild the entire font token
        system using the specified family and size as the base. Otherwise, uses
        system defaults.

        Example:
            >>> AppConfig.set(font=("Arial", 11))
            >>> Typography.initialize_from_appconfig()
            # All typography tokens now use Arial with size ramp based on 11
        """
        from ttkbootstrap.appconfig import AppConfig

        if AppConfig.has('font'):
            family, size = AppConfig.get('font')
            # Build new token set with custom base
            tokens = build_tokens_from_base(size, family)
            cls.use_fonts(tokens)

    @classmethod
    def _register_fonts(cls) -> None:
        token_map = {k: v for k, v in FontTokenNames.__dict__.items() if not k.startswith("__")}
        for field_name in cls._fonts._fields:
            spec = getattr(cls._fonts, field_name)
            font_name = token_map.get(field_name, field_name)  # e.g., "body-lg"
            fallback = FALLBACK_MONO if field_name == "code" else FALLBACK_FONT
            f = Font(
                name=font_name,
                family=spec.font if not cls._use_fallback else fallback,
                size=spec.size,
                weight=spec.weight,
            )
            cls._named_fonts[font_name] = f

    @classmethod
    def _override_tk_fonts(cls) -> None:
        for tk_name, token_name in TK_FONT_OVERRIDES.items():
            spec = cls.get_token(token_name)
            fallback = FALLBACK_MONO if token_name == "code" else FALLBACK_FONT
            if tk_name in font.names():
                font.nametofont(tk_name).configure(
                    family=spec.font if not cls._use_fallback else fallback,
                    size=spec.size,
                    weight=spec.weight,
                )
