"""International number/date formatting and parsing utilities.

Provides locale-aware formatting using Babel and pragmatic parsing that
prefers `dateparser` with a `python-dateutil` fallback. This module is
independent of translation and complements MessageCatalog by handling
locale-sensitive values.
"""

from __future__ import annotations

import locale
import re
import warnings
from dataclasses import dataclass
from datetime import date, datetime, time
from typing import Any, Literal, Mapping, Optional, TypedDict, Union, cast

try:
    import dateparser  # type: ignore
except Exception:  # optional dependency
    dateparser = None  # type: ignore
from babel.core import Locale, UnknownLocaleError
from babel.dates import format_date, format_datetime, format_time, get_date_format
# Babel: formatting only (and parse_decimal for numbers)
from babel.numbers import (format_currency, format_decimal, format_percent, format_scientific, parse_decimal, get_territory_currencies)
# Parsing stack
from dateutil import parser as duparser


# ----------------------------
# Locale detection helper
# ----------------------------

def detect_locale(default: str = "en_US") -> str:
    """
    Return a Babel-friendly locale like 'de_DE' or 'en_US'.
    - Tries current process locale, then system default (if available).
    - Strips encoding suffixes (e.g. '.UTF-8').
    - Validates with Babel; falls back to `default` on failure.
    """
    lang: Optional[str]
    enc: Optional[str]

    # 1) Current process locale
    lang, enc = locale.getlocale()  # type: ignore[assignment]

    # 2) Fallback to system default if unset and API exists
    if not lang:
        get_def = getattr(locale, "getdefaultlocale", None)
        if callable(get_def):
            try:
                lang2, _enc2 = get_def()  # deprecated but present on 3.13
            except (ValueError, TypeError, locale.Error):
                lang2 = None
            if lang2:
                lang = lang2

    if not lang:
        return default

    # Normalize 'de_DE.UTF-8' -> 'de_DE'
    lang = lang.split(".", 1)[0]

    # 3) Validate for Babel
    try:
        Locale.parse(lang)
        return lang
    except (UnknownLocaleError, ValueError):
        return default


# ----------------------------
# DevExtreme-like format specs
# ----------------------------

NumberPreset = Literal[
    "fixedPoint",
    "decimal",
    "percent",
    "currency",
    "exponential",
    "thousands",
    "millions",
    "billions",
    "trillions",
    "largeNumber",
]

DatePreset = Literal[
    "longDate",
    "shortDate",
    "longTime",
    "shortTime",
    "longDateLongTime",
    "shortDateShortTime",
    "monthAndDay",
    "monthAndYear",
    "quarterAndYear",
    "millisecond",
    "second",
    "minute",
    "hour",
    "day",
    "dayOfWeek",
    "month",
    "quarter",
    "year",
]


class NumberFormatOptions(TypedDict, total=False):
    type: NumberPreset | Literal["custom"]
    precision: int
    currency: str
    pattern: str
    use_grouping: bool


NumberFormatSpec = Union[str, NumberFormatOptions]


class DateFormatOptions(TypedDict, total=False):
    type: DatePreset | Literal["custom"]
    pattern: str


DateFormatSpec = Union[str, DateFormatOptions]

# Loosen API: allow str | dict for convenience
LooseSpec = Union[str, Mapping[str, Any]]
FormatSpec = LooseSpec


# ----------------------------
# Compact number suffix config
# ----------------------------

@dataclass(frozen=True)
class Suffix:
    threshold: int
    symbol: str


SUFFIXES_EN = (
    Suffix(1_000_000_000_000, "T"),
    Suffix(1_000_000_000, "B"),
    Suffix(1_000_000, "M"),
    Suffix(1_000, "K"),
)
_SUFFIX_TO_FACTOR = {"K": 1_000, "M": 1_000_000, "B": 1_000_000_000, "T": 1_000_000_000_000}
_NUMBERISH = (int, float)


def _locale_to_languages(loc: str) -> list[str]:
    """
    'en_US' -> ['en']; 'pt_BR' -> ['pt']; 'fr' -> ['fr'].
    dateparser wants base languages, not 'de-DE'.
    """
    return [loc.replace("_", "-").split("-")[0].lower()]


class IntlFormatter:
    """
    DevExtreme-like number/date/datetime formatter.
    - FORMAT with Babel (locale-aware).
    - PARSE dates/times with dateparser -> dateutil fallback.
    - PARSE numbers with Babel's parse_decimal (+ compact K/M/B/T).
    """

    def __init__(
            self,
            locale: str | None = None,
            *,
            day_first: bool = False,
            year_first: bool = False,
    ):
        """Create an IntlFormatter.

        Args:
            locale: Locale code like 'en_US' or 'de_DE'. If None, detect
                from the current process/system settings.
            day_first: Whether day precedes month when parsing dates (e.g., D/M/Y).
            year_first: Whether year precedes month/day when parsing dates (e.g., Y/M/D).
        """
        self.locale = locale or detect_locale()
        self.day_first = day_first
        self.year_first = year_first

    # ---------- Public API ----------
    def format(self, value: Any, spec: FormatSpec) -> str:
        """Format a number/date/time/datetime according to spec.

        Args:
            value: The value to format. Numbers, date, time, datetime are
                handled specially; anything else is converted with str().
            spec: Format specification. For numbers, a preset string like
                'decimal', 'percent', 'currency', 'largeNumber', or a dict
                with options (e.g., {'type': 'percent', 'precision': 2}).
                For dates/times, use presets like 'longDate', 'shortTime',
                or a CLDR pattern via {'type': 'custom', 'pattern': 'yyyy-MM-dd'}
                (or simply the pattern string).

        Returns:
            The formatted string.
        """
        if value is None:
            return ""
        if isinstance(value, _NUMBERISH):
            return self._format_number(float(value), spec)
        if isinstance(value, datetime):
            return self._format_datetime(value, spec)
        if isinstance(value, date):
            return self._format_date(value, spec)
        if isinstance(value, time):
            return self._format_time(value, spec)
        return str(value)

    def parse(self, text: str, spec: FormatSpec) -> Any:
        """Parse a string into a number/date/time/datetime per spec.

        Args:
            text: Input string to parse.
            spec: A number or temporal spec, same shape as for format().

        Returns:
            Parsed Python object (float, date, time, or datetime). Returns
            None for empty input.

        Raises:
            ValueError: If parsing fails for temporal values.
        """
        s = (text or "").strip()
        if s == "":
            return None
        if self._is_number_spec(spec):
            return self._parse_number(s, spec)
        return self._parse_temporal(s, spec)

    # ---------- Numbers ----------
    def _format_number(self, x: float, spec: LooseSpec) -> str:
        opt = self._normalize_number_spec(spec)

        if opt["type"] == "custom":
            pat = opt.get("pattern") or "#,##0.###"
            return format_decimal(x, format=pat, locale=self.locale)

        if opt["type"] in ("thousands", "millions", "billions", "trillions"):
            threshold = {
                "thousands": 1_000,
                "millions": 1_000_000,
                "billions": 1_000_000_000,
                "trillions": 1_000_000_000_000,
            }[opt["type"]]
            symbol = {1_000: "K", 1_000_000: "M", 1_000_000_000: "B", 1_000_000_000_000: "T"}[threshold]
            return self._format_with_suffix(x, threshold, symbol, opt.get("precision"))

        if opt["type"] == "largeNumber":
            return self._format_large_number(x, opt.get("precision"))

        pattern = self._build_pattern_from_options(opt) if opt["type"] in ("decimal", "fixedPoint") else None

        if opt["type"] in ("decimal", "fixedPoint"):
            return format_decimal(x, format=pattern, locale=self.locale)

        if opt["type"] == "percent":
            if opt.get("precision") is None:
                return format_percent(x, locale=self.locale)
            p = max(0, int(opt["precision"]))
            frac = "" if p == 0 else ("." + "0" * p)
            percent_pattern = f"#,##0{frac}%"
            return format_percent(x, format=percent_pattern, locale=self.locale)

        if opt["type"] == "currency":
            curr = opt.get("currency") or self._get_default_currency()
            prec = opt.get("precision")
            if prec is None:
                # Use locale default currency pattern (includes symbol & spacing)
                return format_currency(x, curr, locale=self.locale)
            # Build a currency pattern with required precision; symbol first is a sane default
            p = max(0, int(prec))
            frac = "" if p == 0 else ("." + "0" * p)
            currency_pattern = f"\\u00A4#,##0{frac}"
            return format_currency(x, curr, format=currency_pattern, locale=self.locale)

        if opt["type"] == "exponential":
            return format_scientific(x, locale=self.locale)

        return format_decimal(x, locale=self.locale)

    def _parse_number(self, s: str, spec: LooseSpec) -> float:
        opt = self._normalize_number_spec(spec)
        m = re.match(r"^\s*([\-+]?[\d.,Ee ]+)\s*([KMBT])?\s*%?\s*$", s, re.IGNORECASE)
        suffix = None
        core = s
        if m:
            core = m.group(1)
            suffix = m.group(2).upper() if m.group(2) else None

        if opt["type"] in ("currency", "percent"):
            core = re.sub(r"[^\d\-+.,Ee ]", "", core)

        if "E" in core.upper():
            if self._locale_decimal_mark_is_comma():
                core = core.replace(".", "").replace(",", ".")
            val = float(core)
        else:
            val = float(parse_decimal(core, locale=self.locale))

        if opt["type"] == "percent" and s.strip().endswith("%"):
            val /= 100.0
        if suffix:
            val *= _SUFFIX_TO_FACTOR[suffix]

        return val

    def _format_large_number(self, x: float, precision: Optional[int]) -> str:
        abs_x = abs(x)
        for suf in SUFFIXES_EN:
            if abs_x >= suf.threshold:
                return self._format_with_suffix(x, suf.threshold, suf.symbol, precision)
        return format_decimal(x, format=self._build_pattern(precision), locale=self.locale)

    def _format_with_suffix(self, x: float, threshold: int, symbol: str, precision: Optional[int]) -> str:
        scaled = x / threshold
        num = format_decimal(scaled, format=self._build_pattern(precision), locale=self.locale)
        return f"{num}{symbol}"

    @staticmethod
    def _build_pattern(precision: Optional[int]) -> Optional[str]:
        if precision is None:
            return "#,##0.###"
        p = max(0, int(precision))
        frac = "" if p == 0 else ("." + "0" * p)
        return f"#,##0{frac}"

    def _build_pattern_from_options(self, opt: NumberFormatOptions) -> Optional[str]:
        return self._build_pattern(opt.get("precision"))

    @staticmethod
    def _normalize_number_spec(spec: LooseSpec) -> NumberFormatOptions:
        if isinstance(spec, str):
            if any(ch in spec for ch in "#0"):
                return {"type": "custom", "pattern": spec}
            return {"type": cast(NumberPreset, spec)}
        return cast(NumberFormatOptions, dict(spec))

    @staticmethod
    def _is_number_spec(spec: LooseSpec) -> bool:
        if isinstance(spec, dict):
            t = spec.get("type")
            return t in {
                "fixedPoint", "decimal", "percent", "currency", "exponential",
                "thousands", "millions", "billions", "trillions", "largeNumber", "custom"
            }
        if isinstance(spec, str):
            return (
                    spec in {
                "fixedPoint", "decimal", "percent", "currency", "exponential",
                "thousands", "millions", "billions", "trillions", "largeNumber"
            } or any(ch in spec for ch in "#0")
            )
        return False

    def _locale_decimal_mark_is_comma(self) -> bool:
        return "," in format_decimal(1.1, locale=self.locale)

    def _get_default_currency(self) -> str:
        """
        Get the default currency for the current locale based on its territory.

        Returns:
            Currency code (e.g., 'JPY', 'USD', 'EUR') or 'USD' as fallback.
        """
        # Map common language codes to their primary territories when no territory is specified
        LANG_TO_TERRITORY = {
            'ja': 'JP',  'en': 'US',  'de': 'DE',  'fr': 'FR',  'es': 'ES',
            'it': 'IT',  'pt': 'BR',  'zh': 'CN',  'ko': 'KR',  'ru': 'RU',
            'ar': 'SA',  'nl': 'NL',  'sv': 'SE',  'pl': 'PL',  'tr': 'TR',
            'da': 'DK',  'fi': 'FI',  'no': 'NO',  'cs': 'CZ',  'hu': 'HU',
            'ro': 'RO',  'th': 'TH',  'vi': 'VN',  'id': 'ID',  'he': 'IL',
            'el': 'GR',  'uk': 'UA',  'bg': 'BG',  'hr': 'HR',  'sk': 'SK',
        }

        try:
            loc = Locale.parse(self.locale)

            # If no territory specified, infer from language
            if not loc.territory and loc.language:
                territory = LANG_TO_TERRITORY.get(loc.language)
                if territory:
                    currencies = get_territory_currencies(territory)
                    if currencies:
                        return currencies[0]

            # Try with the territory if present
            if loc.territory:
                currencies = get_territory_currencies(loc.territory)
                if currencies:
                    # Return the first (primary/official) currency
                    return currencies[0]
        except (UnknownLocaleError, ValueError):
            pass
        return "USD"  # fallback

    # ---------- Dates / Times ----------
    def _format_date(self, d: date, spec: LooseSpec) -> str:
        opt = self._normalize_date_spec(spec)
        t = opt["type"]
        if t == "custom": return format_date(d, format=opt["pattern"], locale=self.locale)
        if t == "longDate": return format_date(d, "long", self.locale)
        if t == "shortDate": return format_date(d, "short", self.locale)
        if t == "monthAndDay": return format_date(d, "MMMM d", self.locale)
        if t == "monthAndYear": return format_date(d, "MMMM y", self.locale)
        if t == "quarterAndYear": return format_date(d, "QQQ y", self.locale)
        if t == "day": return format_date(d, "d", self.locale)
        if t == "dayOfWeek": return format_date(d, "EEEE", self.locale)
        if t == "month": return format_date(d, "MMMM", self.locale)
        if t == "quarter": return format_date(d, "QQQ", self.locale)
        if t == "year": return format_date(d, "y", self.locale)
        if t in ("longTime", "shortTime"):
            return format_time(time(0, 0), "long" if t == "longTime" else "short", self.locale)
        if t in ("longDateLongTime", "shortDateShortTime"):
            return format_datetime(
                datetime.combine(d, time(0, 0)), "long" if t == "longDateLongTime" else "short", self.locale)
        return format_date(d, "short", self.locale)

    def _format_time(self, t: time, spec: LooseSpec) -> str:
        opt = self._normalize_date_spec(spec)
        typ = opt["type"]
        if typ == "custom": return format_time(t, format=opt["pattern"], locale=self.locale)
        if typ == "longTime": return format_time(t, "long", self.locale)
        if typ == "shortTime": return format_time(t, "short", self.locale)
        if typ == "hour": return format_time(t, "H", self.locale)
        if typ == "minute": return format_time(t, "m", self.locale)
        if typ == "second": return format_time(t, "s", self.locale)
        if typ == "millisecond": return format_datetime(datetime.combine(date.today(), t), "S", self.locale)
        if typ in ("longDate", "shortDate", "monthAndDay", "monthAndYear", "quarterAndYear", "day", "dayOfWeek",
                   "month", "quarter", "year"):
            return format_time(t, "short", self.locale)
        if typ in ("longDateLongTime", "shortDateShortTime"):
            return format_datetime(
                datetime.combine(date.today(), t), "long" if typ == "longDateLongTime" else "short", self.locale)
        return format_time(t, "short", self.locale)

    def _format_datetime(self, dt: datetime, spec: LooseSpec) -> str:
        opt = self._normalize_date_spec(spec)
        typ = opt["type"]
        if typ == "custom": return format_datetime(dt, format=opt["pattern"], locale=self.locale)
        if typ == "longDateLongTime": return format_datetime(dt, "long", self.locale)
        if typ == "shortDateShortTime": return format_datetime(dt, "short", self.locale)
        if typ == "longDate": return format_date(dt.date(), "long", self.locale)
        if typ == "shortDate": return format_date(dt.date(), "short", self.locale)
        if typ == "longTime": return format_time(dt.time(), "long", self.locale)
        if typ == "shortTime": return format_time(dt.time(), "short", self.locale)
        if typ == "monthAndDay": return format_date(dt.date(), "MMMM d", self.locale)
        if typ == "monthAndYear": return format_date(dt.date(), "MMMM y", self.locale)
        if typ == "quarterAndYear": return format_date(dt.date(), "QQQ y", self.locale)
        if typ == "millisecond": return format_datetime(dt, "SSS", self.locale)
        if typ == "second": return format_time(dt.time(), "s", self.locale)
        if typ == "minute": return format_time(dt.time(), "m", self.locale)
        if typ == "hour": return format_time(dt.time(), "H", self.locale)
        if typ == "day": return format_date(dt.date(), "d", self.locale)
        if typ == "dayOfWeek": return format_date(dt.date(), "EEEE", self.locale)
        if typ == "month": return format_date(dt.date(), "MMMM", self.locale)
        if typ == "quarter": return format_date(dt.date(), "QQQ", self.locale)
        if typ == "year": return format_date(dt.date(), "y", self.locale)
        return format_datetime(dt, "short", self.locale)

    # ---------- Temporal parsing ----------
    def _parse_temporal(self, s: str, spec: LooseSpec) -> Any:
        opt = self._normalize_date_spec(spec)
        t = opt["type"]

        if t == "millisecond" and re.fullmatch(r"\d{1,3}", s):
            ms = max(0, min(999, int(s)))
            return datetime.now().replace(microsecond=ms * 1000)

        languages = _locale_to_languages(self.locale)
        settings = {
            "PREFER_DAY_OF_MONTH": "first" if self.day_first else "current",
            "PREFER_DATES_FROM": "current_period",
            "RELATIVE_BASE": datetime.now(),
            "RETURN_AS_TIMEZONE_AWARE": False,
            "DATE_ORDER": self._date_order_from_locale(),
        }

        dp = None
        try:
            with warnings.catch_warnings():
                warnings.filterwarnings(
                    "ignore", category=DeprecationWarning,
                    message=r"Parsing dates involving a day of month without a year specified.*")
                dp = dateparser.parse(s, languages=languages, settings=settings)
        except ValueError:
            dp = None

        if dp is None:
            with warnings.catch_warnings():
                warnings.filterwarnings(
                    "ignore", category=DeprecationWarning,
                    message=r"Parsing dates involving a day of month without a year specified.*")
                dp = dateparser.parse(s, settings=settings)

        if dp is None:
            base = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            try:
                dp = duparser.parse(
                    s, dayfirst=self.day_first, yearfirst=self.year_first,
                    fuzzy=True, default=base)
            except Exception as e:
                raise ValueError(f"Could not parse temporal value: {s!r}") from e

        if t in ("longDate", "shortDate", "monthAndDay", "monthAndYear", "quarterAndYear", "day", "dayOfWeek", "month",
                 "quarter", "year"):
            return dp.date()
        if t in ("longTime", "shortTime", "second", "minute", "hour", "millisecond"):
            return dp.time().replace(microsecond=(dp.microsecond // 1000) * 1000)
        return dp

    @staticmethod
    def _normalize_date_spec(spec: LooseSpec) -> DateFormatOptions:
        if isinstance(spec, str):
            known = {
                "longDate", "shortDate", "longTime", "shortTime",
                "longDateLongTime", "shortDateShortTime",
                "monthAndDay", "monthAndYear", "quarterAndYear",
                "millisecond", "second", "minute", "hour",
                "day", "dayOfWeek", "month", "quarter", "year",
            }
            if spec in known:
                return {"type": cast(DatePreset, spec)}
            # Otherwise treat as CLDR custom pattern for formatting
            return {"type": "custom", "pattern": spec}
        return cast(DateFormatOptions, dict(spec))

    def _date_order_from_locale(self) -> str:
        """
        Infer DATE_ORDER for dateparser from the locale's short date pattern.
        Returns 'DMY', 'MDY', or 'YMD'.
        """
        try:
            pat = str(get_date_format("short", locale=self.locale))
            order: list[str] = []
            for ch in pat:
                if ch in "yMd":
                    if ch == "y" and "Y" not in order:
                        order.append("Y")
                    elif ch == "M" and "M" not in order:
                        order.append("M")
                    elif ch == "d" and "D" not in order:
                        order.append("D")
            joined = "".join(order)
            if joined.startswith("DMY"):
                return "DMY"
            if joined.startswith("MDY"):
                return "MDY"
            if joined.startswith("YMD"):
                return "YMD"
            return "MDY"  # fallback
        except (UnknownLocaleError, ValueError):
            return "MDY"


# -------------- optional quick demo --------------
if __name__ == "__main__":
    fmt = IntlFormatter()  # auto-detects system locale
    print(fmt.locale)

    # Numbers
    print(fmt.format(1234.56, "decimal"))
    print(fmt.format(0.42, {"type": "percent", "precision": 0}))
    print(fmt.format(1234.5, {"type": "currency", "currency": "EUR", "precision": 2}))
    print(fmt.format(1_234_000, "largeNumber"))
    print(fmt.parse("1.2M", "largeNumber"))

    # Dates/times
    print(fmt.format(date(2025, 9, 2), "longDate"))
    print(IntlFormatter(locale="de_DE", day_first=True).parse("15 juillet 2025", "longDate"))  # auto-detect FR text
    print(IntlFormatter(locale="fr_FR", day_first=True).parse("15 juillet 2025", "longDate"))
