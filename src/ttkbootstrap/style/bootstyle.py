"""The bootstyle resolver and delivery API.

`Bootstyle` maps a `bootstyle`/`style` string to a built ttk style (reading the
`Keywords` grammar). `BootMixin`/`AutoStyleMixin` are the concrete-subclass
delivery path; `bootify`/`apply_bootstyle`/`enable_global_api` are the dynamic
and opt-in-global delivery primitives. Top layer of the `style` package.
"""
import difflib
import re
import warnings
from tkinter import Grid, Pack, Place, TclError, ttk

from ttkbootstrap.constants import (
    BOOTSTYLE_COLORS,
    BOOTSTYLE_MODIFIERS,
    BOOTSTYLE_INTERNAL_MODIFIERS,
    BOOTSTYLE_FAMILIES,
    BOOTSTYLE_ORIENTS,
    BOOTSTYLE_SURFACE_TOKENS,
    DEFAULT_SURFACE,
    NEUTRAL,
    NEUTRAL_FAMILIES,
    BootStyle,
    surface_segment,
)
from ttkbootstrap.internal.busy import BusyMixin
from ttkbootstrap.style import _compat
from ttkbootstrap.style.engine import Style
from ttkbootstrap.style.builders_ttk import StyleBuilderTTK
from ttkbootstrap.style.builders_tk import StyleBuilderTK
from ttkbootstrap.style.builders.registry import DEFAULT_VARIANT


class Keywords:
    """Static keyword lists and regex patterns used to parse
    ttkbootstrap "bootstyle" strings.

    Bootstyle strings contain space- or dash-separated tokens that may
    specify: a widget class (e.g. "button"), an orientation ("horizontal"
    or "vertical"), a color ("primary", "info", etc.), and optional
    type modifiers (e.g. "outline", "link", "inverse", "striped"). The
    constants and compiled regexes in this class centralize those token
    definitions for reuse by the bootstyle parsing helpers.

    This class is internal to the styling system and not intended to be
    instantiated.

    The token lists are sourced from the single vocabulary in
    `ttkbootstrap.constants`. The "type" slot spans both public modifiers
    (`outline`, `round`, ...) and the internal composite modifiers (`meter`,
    `date`, ...). The compiled patterns are retained for the orientation
    lookup and any back-compat callers; the primary parse path is the token
    classifier below.
    """

    COLORS = list(BOOTSTYLE_COLORS)
    ORIENTS = list(BOOTSTYLE_ORIENTS)
    TYPES = list(BOOTSTYLE_MODIFIERS) + list(BOOTSTYLE_INTERNAL_MODIFIERS)
    CLASSES = list(BOOTSTYLE_FAMILIES)
    # Longest-first alternation so a longer token wins over a substring it
    # contains (e.g. `labelframe` over `label`, `menubutton` over `button`).
    COLOR_PATTERN = re.compile("|".join(sorted(COLORS, key=len, reverse=True)))
    ORIENT_PATTERN = re.compile("|".join(ORIENTS))
    CLASS_PATTERN = re.compile("|".join(sorted(CLASSES, key=len, reverse=True)))
    TYPE_PATTERN = re.compile("|".join(sorted(TYPES, key=len, reverse=True)))


# --------------------------------------------------------------------------- #
# Bootstyle tokenizer (2.0 Workstream D)
#
# The pre-2.0 resolver `re.search`-ed the whole string for a color/type/class
# substring anywhere, which silently dropped unknown tokens and risked
# substring collisions. The tokenizer below splits the (normalized) string into
# tokens and classifies each against the closed vocabulary, so an unrecognized
# token fails loudly (warn by default, raise in strict mode) instead of being
# ignored.
# --------------------------------------------------------------------------- #
_COLORS = frozenset(BOOTSTYLE_COLORS)
_PUBLIC_MODIFIERS = frozenset(BOOTSTYLE_MODIFIERS)
_MODIFIERS = _PUBLIC_MODIFIERS | frozenset(BOOTSTYLE_INTERNAL_MODIFIERS)
_FAMILIES = frozenset(BOOTSTYLE_FAMILIES)
_ORIENTS = frozenset(BOOTSTYLE_ORIENTS)
# winfo_class inference matches the class name by substring; try longer family
# names first so `TLabelframe` resolves to `labelframe`, not `label`.
_FAMILIES_BY_LEN = tuple(sorted(BOOTSTYLE_FAMILIES, key=len, reverse=True))
# Suggestion pool for typos -- the tokens a user might reasonably have meant
# (exclude the internal composite modifiers, which are not user-facing).
_SUGGESTION_POOL = tuple(
    sorted(_COLORS | _PUBLIC_MODIFIERS | _FAMILIES | _ORIENTS)
)
# Tokens that carry no slot meaning: empty fragments and the "no bootstyle"
# sentinel the delivery paths pass when only a base style is wanted.
_SENTINELS = frozenset({"", "default"})
_TOKEN_SPLIT = re.compile(r"[-\s]+")

# Surface vocabulary (2.0 surface-color). A surface is a named neutral surface OR
# an accent color; it rides INSIDE the bootstyle string as an `@<surface>` token
# (e.g. "@primary success ghost") and, when non-default, prefixes the style name
# with an `@<surface>.` segment. `_SURFACE_FAMILIES` gates which families a recipe
# consumes surface for yet -- it grows one PR at a time as families are migrated;
# a surface for any other family is silently ignored. `frame` consumes a surface
# to fill itself with it (`@card`/`@chrome` -- a container that *is* a surface, so
# a sidebar or panel renders on the elevation scale); leaf widgets consume it to
# blend onto the surface they sit on. The token vocab lives once in constants
# (`BOOTSTYLE_SURFACE_TOKENS`).
_SURFACE_TOKENS = frozenset(BOOTSTYLE_SURFACE_TOKENS)
_SURFACE_FAMILIES = frozenset(
    {"button", "checkbutton", "radiobutton", "toggle", "label",
     "scale", "progressbar", "scrollbar", "frame"}
)


def _normalize_surface(surface, family, source, warn):
    """Normalize/validate a surface token to a canonical token or ``""``.

    Lowercases and trims; maps the default/empty surface to ``""`` (no prefix).
    An unrecognized token routes through the shared `_compat` strictness gate
    (warn-and-drop by default, raise in strict) exactly like an unknown bootstyle
    token -- but `warn` is False for the lenient already-built-style-name dialect,
    so a custom ``@brand.TLabel`` style name never warns/raises on the theme walk.
    A valid token for a family not yet surface-capable is dropped silently (the
    rollout gate). Returns the token to embed in the style name, or ``""``.
    """
    if not surface:
        return ""
    surface = str(surface).strip().lower()
    if not surface or surface == DEFAULT_SURFACE:
        return ""
    if surface not in _SURFACE_TOKENS:
        if warn:
            suggestions = difflib.get_close_matches(
                surface, sorted(_SURFACE_TOKENS), n=1
            )
            _compat.report_invalid("surface", surface, source, suggestions)
        return ""
    if family not in _SURFACE_FAMILIES:
        return ""
    return surface


def _classify_tokens(style_string, *, source=None, warn=False):
    """Split a bootstyle string and classify each token into a slot.

    Returns ``(color, modifier, base, orient, surface)`` -- the first token seen
    for each slot (matching the pre-2.0 leftmost-wins behavior). A ``@<surface>``
    token (2.0 surface-color) names the background the widget sits on; it is
    position-free and may appear anywhere in the string
    (``"@primary success ghost"``). When ``warn`` is true, an unrecognized token
    and a duplicate-slot token are reported through the `_compat` loud-failure
    path (warn by default, raise in strict mode). The surface token is only
    *extracted* here; it is validated by `_normalize_surface`.
    """
    source = style_string if source is None else source
    color = modifier = base = orient = surface = ""
    for token in _TOKEN_SPLIT.split(style_string.strip().lower()):
        if token in _SENTINELS:
            continue
        if token.startswith("@"):
            surf = token[1:]
            if not surf:
                continue  # a bare '@' carries no surface
            if warn and surface and surf != surface:
                _compat.report_invalid("surface", surf, source)
            surface = surface or surf
        elif token in _COLORS:
            if warn and color and token != color:
                _compat.report_invalid("color", token, source)
            color = color or token
        elif token in _MODIFIERS:
            if warn and modifier and token != modifier:
                _compat.report_invalid("modifier", token, source)
            modifier = modifier or token
        elif token in _FAMILIES:
            if warn and base and token != base:
                _compat.report_invalid("base-type", token, source)
            base = base or token
        elif token in _ORIENTS:
            orient = orient or token
        elif warn:
            suggestions = difflib.get_close_matches(
                token, _SUGGESTION_POOL, n=1
            )
            _compat.report_invalid("token", token, source, suggestions)
    return color, modifier, base, orient, surface


def _looks_like_style_name(style_string):
    """Return whether the input is an already-built ttk style name.

    The resolver accepts two dialects. A *bootstyle* is lowercase and dash/space
    separated (``"primary-outline"``). A built *ttk style name* always has a
    Title-cased class component, so it contains an uppercase letter and no dash
    or space (``"TFrame"``, ``"primary.Outline.TButton"``, ``"symbol.Link.
    TButton"``); a dotted string is always a style name. This lets the theme
    walk re-resolve a widget's dotted ``cget("style")`` (including a bare base
    like ``"TFrame"``) without misreading it as a mistyped bootstyle. A
    leading-``@`` string with no ``.`` is a bootstyle carrying only a surface
    token (``"@primaryy"``), not a built name -- so it stays on the loud
    bootstyle path and a typo'd surface is reported.
    """
    if "." in style_string:
        return True
    if style_string.startswith("@"):
        return False
    return (
        "-" not in style_string
        and " " not in style_string
        and any(ch.isupper() for ch in style_string)
    )


def _classify_style_name(name):
    """Classify the segments of an already-built dotted ttk style name.

    The resolver receives two input dialects: a dashed/spaced *bootstyle*
    (``"primary-outline"``) and an already-built *ttk style name*
    (``"primary.Outline.TButton"``, ``"symbol.Link.TButton"``). The latter
    arrives from the theme-walk repaint (a widget's current ``cget("style")``),
    from `Style.configure` subclassing a base style, and from user-supplied
    custom style names. Segments are split on ``.``; a leading ``@surface``
    segment is the surface-color prefix (2.0 surface-color); the class segment is
    title-cased with an optional ``T`` prefix, so ``TButton`` -> ``button`` but
    ``Treeview``/``Toggle`` map directly. Unknown segments (custom prefixes such
    as ``symbol``) are ignored *without* warning -- style names legitimately
    carry them, unlike a user's bootstyle.
    """
    color = modifier = base = orient = surface = ""
    for segment in name.split("."):
        seg = segment.strip().lower()
        if not seg or seg in _SENTINELS:
            continue
        if seg.startswith("@"):
            surface = surface or seg[1:]
        elif seg in _COLORS:
            color = color or seg
        elif seg in _MODIFIERS:
            modifier = modifier or seg
        elif seg in _ORIENTS:
            orient = orient or seg
        elif seg in _FAMILIES:
            base = base or seg
        elif seg.startswith("t") and seg[1:] in _FAMILIES:
            base = base or seg[1:]
        # else: an unknown custom segment -- ignore it silently
    return color, modifier, base, orient, surface


def _infer_family(widget):
    """Infer the widget family from its Tcl class (longest match wins)."""
    if widget is None:
        return ""
    try:
        widget_class = widget.winfo_class().lower()
    except Exception:
        return ""
    for family in _FAMILIES_BY_LEN:
        if family in widget_class:
            return family
    return ""


def _build_ttkstyle_name(color, modifier, orient, family, surface=""):
    """Assemble the dotted ttk style name from resolved slot tokens.

    Preserves the exact pre-2.0 casing: the color stays lowercase, the modifier
    and orientation are title-cased, and the family is title-cased with a ``T``
    prefix unless it already starts with ``t`` (``Treeview``, ``Toplevel``). A
    non-default `surface` (2.0 surface-color) prefixes an ``@<surface>.`` segment
    (lowercase); the default/empty surface adds nothing, so a surfaceless style
    name is byte-for-byte the pre-surface name.
    """
    surface = surface_segment(surface)
    color = f"{color}." if color else ""
    modifier = f"{modifier.title()}." if modifier else ""
    orient = f"{orient.title()}." if orient else ""
    if family.startswith("t"):
        family = family.title()
    else:
        family = f"T{family.title()}"
    return f"{surface}{color}{modifier}{orient}{family}"


class Bootstyle:
    """Helpers for parsing and applying ttkbootstrap "bootstyle" options.

    Bootstyle augments ttk widgets with a compact styling API that lets
    you configure color, orientation, and type with a single string (or
    tuple) such as "primary-outline", "success", or ("danger", "inverse").

    This class provides utilities to parse those tokens from strings and
    widget state, determine the target widget class and orientation, and
    resolve the requested color and variant. Its `update_ttk_widget_style`
    resolver is the engine shared by both api-delivery paths: the default
    `BootMixin` subclasses and the opt-in global patch (`enable_global_api`).

    Typical end users will not call these methods directly; they are used
    internally by the Style engine, the mixins, and the global patch.
    """
    @staticmethod
    def ttkstyle_widget_class(widget=None, string=""):
        """Find and return the widget class

        Parameters:

            widget (Widget):
                The widget object.

            string (str):
                A keyword string to parse.

        Returns:

            str:
                A widget class keyword.
        """
        # an explicit base-type token in the string wins; otherwise infer the
        # family from the widget's Tcl class
        _, _, base, _, _ = _classify_tokens(string)
        if base:
            return base
        return _infer_family(widget)

    @staticmethod
    def ttkstyle_widget_type(string):
        """Find and return the widget type.

        Parameters:

            string (str):
                A keyword string to parse.

        Returns:

            str:
                A widget type keyword.
        """
        _, modifier, _, _, _ = _classify_tokens(string)
        return modifier

    @staticmethod
    def ttkstyle_widget_orient(widget=None, string="", **kwargs):
        """Find and return widget orient, or default orient for widget if
        a widget with orientation.

        Parameters:

            widget (Widget):
                The widget object.

            string (str):
                A keyword string to parse.

            **kwargs:
                Optional keyword arguments passed in the widget constructor.

        Returns:

            str:
                A widget orientation keyword.
        """
        # string method (priority)
        match = re.search(Keywords.ORIENT_PATTERN, string)
        widget_orient = ""

        if match is not None:
            widget_orient = match.group(0)
            return widget_orient

        # orient from kwargs
        if "orient" in kwargs:
            _orient = kwargs.pop("orient")
            if _orient == "h":
                widget_orient = "horizontal"
            elif _orient == "v":
                widget_orient = "vertical"
            else:
                widget_orient = _orient
            return widget_orient

        # orient from settings
        if widget is None:
            return widget_orient
        try:
            widget_orient = str(widget.cget("orient"))
        except:
            pass

        return widget_orient

    @staticmethod
    def ttkstyle_widget_color(string):
        """Find and return widget color

        Parameters:

            string (str):
                A keyword string to parse.

        Returns:

            str:
                A color keyword.
        """
        color, _, _, _, _ = _classify_tokens(string)
        return color

    @staticmethod
    def ttkstyle_name(widget=None, string="", **kwargs):
        """Parse a string to build and return a ttkstyle name.

        Parameters:

            widget (Widget):
                The widget object.

            string (str):
                A keyword string to parse.

            **kwargs:
                Other keyword arguments to parse widget orientation.

        Returns:

            str:
                A ttk style name
        """
        style_string = _compat.normalize_bootstyle(string)
        color, modifier, _, orient, family, surface = (
            Bootstyle._parse_components(
                widget, style_string, warn=False, **kwargs
            )
        )
        return _build_ttkstyle_name(color, modifier, orient, family, surface)

    @staticmethod
    def _parse_components(widget, style_string, *, warn, **kwargs):
        """Resolve a bootstyle/style string to ``(color, modifier, base,
        orient, family, surface)``.

        A dotted input is an already-built ttk style name and is parsed
        leniently (`_classify_style_name`); a dashed/spaced input is a bootstyle
        and goes through the closed-vocab tokenizer, which fails loudly on
        unknown tokens when ``warn`` is set. ``family`` is the explicit base
        token if present, else inferred from the widget. ``surface`` (2.0
        surface-color) is carried in the string itself -- a ``@surface`` token in
        a bootstyle, or a ``@surface`` segment in an already-built style name (the
        theme-walk re-resolve). It is normalized/gated against the resolved family
        (`_normalize_surface`). The already-built-style-name dialect normalizes
        the surface *leniently* (``surface_warn=False``) so a custom ``@brand``
        prefix never warns/raises, matching the lenient handling of other unknown
        style-name segments.
        """
        if _looks_like_style_name(style_string):
            color, modifier, base, orient, surface = (
                _classify_style_name(style_string)
            )
            surface_warn = False
            if not orient:
                orient = Bootstyle.ttkstyle_widget_orient(
                    widget, "", **kwargs
                )
        else:
            color, modifier, base, _, surface = _classify_tokens(
                style_string, warn=warn
            )
            surface_warn = warn
            orient = Bootstyle.ttkstyle_widget_orient(
                widget, style_string, **kwargs
            )
        family = base or _infer_family(widget)
        surface = _normalize_surface(surface, family, style_string, surface_warn)
        return color, modifier, base, orient, family, surface

    @staticmethod
    def ttkstyle_method_name(widget=None, string=""):
        """Parse a string to build and return the name of the
        `StyleBuilderTTK` method that creates the ttk style for the
        target widget.

        Parameters:

            widget (Widget):
                The widget object to lookup.

            string (str):
                The keyword string to parse.

        Returns:

            str:
                The name of the update method used to update the widget.
        """
        style_string = "".join(string).lower()
        widget_type = Bootstyle.ttkstyle_widget_type(style_string)
        widget_class = Bootstyle.ttkstyle_widget_class(widget, style_string)

        if widget_type:
            widget_type = f"_{widget_type}"

        if widget_class:
            widget_class = f"_{widget_class}"

        if not widget_type and not widget_class:
            return ""
        else:
            method_name = f"create{widget_type}{widget_class}_style"
            return method_name

    @staticmethod
    def tkupdate_method_name(widget):
        """Lookup the tkinter style update method from the widget class

        Parameters:

            widget (Widget):
                The widget object to lookup.

        Returns:

            str:
                The name of the method used to update the widget object.
        """
        widget_class = Bootstyle.ttkstyle_widget_class(widget)

        if widget_class:
            widget_class = f"_{widget_class}"

        method_name = f"update{widget_class}_style"
        return method_name

    @staticmethod
    def override_ttk_widget_constructor(func):
        """Override widget constructors with bootstyle api options.

        Parameters:

            func (Callable):
                The widget class `__init__` method
        """

        def __init__(self, *args, **kwargs):

            # Blessed subclasses (BootMixin) own bootstyle resolution; when the
            # global API is also enabled, defer to the mixin to avoid
            # double-applying a style.
            if isinstance(self, BootMixin):
                func(self, *args, **kwargs)
                return

            # capture bootstyle and style arguments
            if "bootstyle" in kwargs:
                bootstyle = kwargs.pop("bootstyle")
            else:
                bootstyle = ""

            if "style" in kwargs:
                style = kwargs.pop("style") or ""
            else:
                style = ""

            # instantiate the widget
            func(self, *args, **kwargs)

            # must be called AFTER instantiation in order to use winfo_class
            #    in the `get_ttkstyle_name` method

            try:
                if style:
                    if Style.get_instance().style_exists_in_theme(style):
                        self.configure(style=style)
                    else:
                        ttkstyle = Bootstyle.update_ttk_widget_style(
                            self, style, **kwargs
                        )
                        self.configure(style=ttkstyle)
                elif bootstyle:
                    ttkstyle = Bootstyle.update_ttk_widget_style(
                        self, bootstyle, **kwargs
                    )
                    self.configure(style=ttkstyle)
                else:
                    ttkstyle = Bootstyle.update_ttk_widget_style(
                        self, "default", **kwargs
                    )
                    self.configure(style=ttkstyle)
                # Stamp the widget current so the next theme walk only repaints
                # it once the theme actually changes.
                Bootstyle.stamp_theme_version(self)
            except AttributeError:
                # Third-party widgets (e.g. tkcalendar.Calendar) override
                # configure() and may access instance attributes that are not
                # yet set when ttk.Frame.__init__ calls back into the
                # subclass configure before the subclass __init__ completes.
                pass

        return __init__

    @staticmethod
    def override_ttk_widget_configure(func):
        """Overrides the configure method on a ttk widget.

        Parameters:

            func (Callable):
                The widget class `configure` method
        """

        def configure(self, cnf=None, **kwargs):
            # Blessed subclasses (BootMixin) own bootstyle resolution; defer to
            # the mixin's configure when the global API is also enabled.
            if isinstance(self, BootMixin):
                return func(self, cnf, **kwargs)

            # get configuration
            if cnf in ("bootstyle", "style"):
                return self.cget("style")

            if cnf is not None:
                return func(self, cnf)

            # set configuration
            if "bootstyle" in kwargs:
                bootstyle = kwargs.pop("bootstyle")
            else:
                bootstyle = ""

            if "style" in kwargs:
                style = kwargs.get("style")
                ttkstyle = Bootstyle.update_ttk_widget_style(
                    self, style, **kwargs
                )
            elif bootstyle:
                ttkstyle = Bootstyle.update_ttk_widget_style(
                    self, bootstyle, **kwargs
                )
                kwargs.update(style=ttkstyle)

            # update widget configuration
            func(self, cnf, **kwargs)

        return configure

    @staticmethod
    def update_ttk_widget_style(
            widget: ttk.Widget = None, style_string: str = None, **kwargs
    ):
        """Update the ttk style or create if not existing.

        Parameters:

            widget (ttk.Widget):
                The widget instance being updated.

            style_string (str):
                The style string to evaluate. May be the `style`, `ttkstyle`
                or `bootstyle` argument depending on the context and scenario.
                A surface (2.0 surface-color) rides inside it as an `@<surface>`
                token (bootstyle) or `@<surface>.` segment (built style name);
                when non-default it prefixes the style name and is threaded to
                the builder.

            **kwargs:
                Other optional keyword arguments.

        Returns:

            str:
                The ttkstyle or empty string if there is none.
        """
        style: Style = Style.get_instance() or Style()

        # get existing widget style if not provided
        if style_string is None:
            style_string = widget.cget("style")

        # normalize legacy forms (tuple/list) to a canonical string. As of D2 all
        # first-party callers pass canonical strings, so a tuple/list here is
        # genuine external use and earns a DeprecationWarning (removed in 3.0).
        style_string = _compat.normalize_bootstyle(style_string, warn=True)

        # do nothing if the style has not been set
        if not style_string:
            return ""

        if style_string == '.':
            return '.'

        # parse once (loud-fail on unknown tokens for a bootstyle string; lenient
        # for an already-built ttk style name); build the ttk style name from
        # the resolved tokens rather than re-parsing the generated name.
        is_bootstyle = not _looks_like_style_name(style_string)
        color, modifier, _, orient, family, surface = (
            Bootstyle._parse_components(
                widget, style_string, warn=True, **kwargs
            )
        )
        variant = modifier or DEFAULT_VARIANT

        # `neutral` is a no-accent fill that only the button-family recipes
        # implement (constants.NEUTRAL_FAMILIES). For any other family it
        # resolves to a color the theme never defines (Colors.get("neutral")
        # -> None), which crashes the recipe mid-build. Treat it like an invalid
        # color for that family: fail loudly for a bootstyle string, then drop
        # the color and fall back to the family's default style.
        if color == NEUTRAL and family not in NEUTRAL_FAMILIES:
            if is_bootstyle:
                _compat.report_invalid("color", f"{NEUTRAL}-{family}", style_string)
            color = ""

        ttkstyle = _build_ttkstyle_name(color, modifier, orient, family, surface)

        # build style if not existing (example: theme changed)
        if not style.style_exists_in_theme(ttkstyle):
            builder: StyleBuilderTTK = style._get_builder()
            if not builder.build_style(variant, family, color, surface):
                if family in _FAMILIES and variant != DEFAULT_VARIANT:
                    # An invalid modifier for one of our own widgets
                    # (e.g. "outline-scale"): fail loudly for a bootstyle string,
                    # then fall back to the family's default style rather than
                    # returning the unusable raw fragment.
                    if is_bootstyle and modifier:
                        _compat.report_invalid(
                            "combination", f"{modifier}-{family}", style_string
                        )
                    ttkstyle = _build_ttkstyle_name(
                        color, "", orient, family, surface
                    )
                    if not style.style_exists_in_theme(ttkstyle) and (
                        not builder.build_style(
                            DEFAULT_VARIANT, family, color, surface
                        )
                    ):
                        return style_string
                else:
                    if is_bootstyle:
                        # A bootstyle on a widget whose class maps to no
                        # ttkbootstrap family (e.g. a bootified third-party
                        # widget with its own widget class): there is no
                        # recipe to build, and the raw fragment ("info") is
                        # not a ttk style name -- assigning it would crash
                        # with "Layout ... not found". Fail loudly (except
                        # for the implicit default resolve) and keep the
                        # widget's current style.
                        if style_string != "default":
                            widget_class = ""
                            try:
                                widget_class = widget.winfo_class()
                            except (AttributeError, TclError):
                                pass
                            _compat.report_invalid(
                                "family", widget_class or "<unknown>",
                                style_string,
                            )
                        try:
                            return str(widget.cget("style"))
                        except (AttributeError, TclError):
                            return ""
                    # An already-built style name from a third-party widget
                    # whose class maps to no ttkbootstrap builder: pass it
                    # through untouched.
                    return style_string

        # Graceful degrade (2.0 surface-color): if a surface was requested but the
        # surfaced style still isn't registered after the build -- a family listed
        # in `_SURFACE_FAMILIES` whose recipe did not emit `surface_prefix` -- fall
        # back to the plain style so the widget renders normally, not bare clam.
        if surface and not style.style_exists_in_theme(ttkstyle):
            builder = style._get_builder()
            plain = _build_ttkstyle_name(color, modifier, orient, family)
            if not style.style_exists_in_theme(plain):
                builder.build_style(variant, family, color)
            if style.style_exists_in_theme(plain):
                ttkstyle = plain

        # Repaint the combobox popdown. It is a Tcl-level toplevel that the
        # theme walk's winfo_children() DFS cannot reach, so it is refreshed
        # here instead -- the walk calls this method for every ttk widget on a
        # theme change, which keeps the popdown in sync without a subscription.
        try:
            if widget.winfo_class() == "TCombobox":
                builder: StyleBuilderTTK = style._get_builder()
                builder.update_combobox_popdown_style(widget)
        except (AttributeError, TclError):
            pass

        return ttkstyle

    @staticmethod
    def setup_ttkbootstrap_api():
        """Monkey-patch the stock tkinter/ttk widget classes with the
        bootstyle/autostyle api.

        This is the legacy *global* path and is not run at import time; the
        default api is delivered through concrete subclasses
        (`BootMixin`/`AutoStyleMixin`). Call `enable_global_api` to opt back
        into patching the stock classes (e.g. for code that creates vanilla
        ``tkinter.ttk`` widgets)."""
        from ttkbootstrap.widgets import TTK_WIDGETS
        from ttkbootstrap.widgets import TK_WIDGETS

        # TTK WIDGETS
        for widget in TTK_WIDGETS:
            try:
                # override widget constructor
                _init = Bootstyle.override_ttk_widget_constructor(
                    widget.__init__
                )
                widget.__init__ = _init

                # override configure method
                _configure = Bootstyle.override_ttk_widget_configure(
                    widget.configure
                )
                widget.configure = _configure
                widget.config = widget.configure

                # override get and set methods
                _orig_getitem = widget.__getitem
                _orig_setitem = widget.__setitem

                def __setitem(self, key, val):
                    if key in ("bootstyle", "style"):
                        return _configure(self, **{key: val})
                    return _orig_setitem(key, val)

                def __getitem(self, key):
                    if key in ("bootstyle", "style"):
                        return _configure(self, cnf=key)
                    return _orig_getitem(key)

                if (
                        widget.__name__ != "OptionMenu"
                ):  # this has it's own override
                    widget.__setitem__ = __setitem
                    widget.__getitem__ = __getitem
            except:
                # this may fail in python 3.6 for ttk widgets that do not exist
                #   in that version.
                continue

        # TK WIDGETS
        for widget in TK_WIDGETS:
            # override widget constructor
            _init = Bootstyle.override_tk_widget_constructor(widget.__init__)
            widget.__init__ = _init

        # Make the geometry managers fluent on every stock/native/third-party
        # widget too, matching `FluentGeometryMixin` (which only covers the
        # blessed subclasses).
        Bootstyle.patch_geometry_managers()

    @staticmethod
    def patch_geometry_managers():
        """Make tkinter's geometry managers return the widget (opt-in global).

        The global-API counterpart to `FluentGeometryMixin`: it patches the
        shared ``Pack``/``Grid``/``Place`` mixin methods that every tk and ttk
        widget inherits, so ``pack``/``grid``/``place`` return ``self`` on
        stock, native, and third-party widgets — not just the blessed
        subclasses. Idempotent: a patched method is tagged so a repeat call is
        a no-op.
        """
        for klass, configure_name in (
            (Pack, "pack_configure"),
            (Grid, "grid_configure"),
            (Place, "place_configure"),
        ):
            orig = klass.__dict__.get(configure_name)
            if orig is None or getattr(orig, "_tb_returns_self", False):
                continue

            def make_wrapper(orig):
                def wrapper(self, *args, **kwargs):
                    orig(self, *args, **kwargs)
                    return self
                wrapper._tb_returns_self = True
                return wrapper

            patched = make_wrapper(orig)
            setattr(klass, configure_name, patched)
            # pack/grid/place are class-body aliases of the *_configure methods
            setattr(klass, configure_name.split("_")[0], patched)

    @staticmethod
    def stamp_theme_version(widget):
        """Stamp a widget with the current theme version.

        Freshly built widgets are already painted for the active theme, so
        stamping them lets the next theme walk skip them until the theme
        actually changes. No-ops cleanly before a `Style` exists or for
        widgets that forbid new attributes.
        """
        style = Style.get_instance()
        if style is None:
            return
        try:
            widget._theme_version = style._theme_version
        except (AttributeError, TypeError):
            pass

    @staticmethod
    def update_tk_widget_style(widget):
        """Look up and call the appropriate style-update method for a
        legacy tk widget.

        Parameters:

            widget (tkinter.Widget):
                The tk widget instance to style.
        """
        try:
            style = Style.get_instance()
            method_name = Bootstyle.tkupdate_method_name(widget)
            builder = style._get_builder_tk()
            builder_method = getattr(StyleBuilderTK, method_name)
            builder_method(builder, widget)
        except:
            """Must pass here to prevent a failure when the user calls
            the `Style`method BEFORE an instance of `Tk` is instantiated.
            This will defer the update of the `Tk` background until the end
            of the `BootStyle` object instantiation (created by the `Style`
            method)"""
            pass

    @staticmethod
    def override_tk_widget_constructor(func):
        """Override widget constructors to apply default style for tk
        widgets.

        Parameters:

            func (Callable):
                The `__init__` method for this widget.
        """

        def __init__wrapper(self, *args, **kwargs):

            # Blessed subclasses (AutoStyleMixin) own autostyle handling; defer
            # to the mixin when the global API is also enabled.
            if isinstance(self, AutoStyleMixin):
                func(self, *args, **kwargs)
                return

            # check for autostyle flag
            if "autostyle" in kwargs:
                autostyle = kwargs.pop("autostyle")
            else:
                autostyle = True

            # instantiate the widget
            func(self, *args, **kwargs)

            if autostyle:
                Bootstyle.update_tk_widget_style(self)
                # Stamp the widget current so the next theme walk only
                # repaints it once the theme actually changes.
                Bootstyle.stamp_theme_version(self)
            else:
                # Opt out of theming entirely: the theme walk must skip this
                # widget on switch, matching the pre-2.0 behavior where an
                # unstyled widget never subscribed for repaints.
                self._tb_no_autostyle = True

        return __init__wrapper


_UNSET = object()  # sentinel: distinguish "icon kwarg omitted" from "icon=None"


class FluentGeometryMixin:
    """Mixin that makes the geometry managers return the widget.

    tkinter's ``pack``/``grid``/``place`` return ``None``; returning ``self``
    instead lets a widget be constructed and placed in a single expression::

        btn = ttk.Button(root, text="Save").pack(padx=10)

    ``pack``/``grid``/``place`` are tkinter aliases for the ``*_configure``
    methods, so overriding the configure variants (and re-aliasing) covers both
    call names. Shared by `BootMixin` (ttk) and `AutoStyleMixin` (tk).
    """

    def pack_configure(self, cnf={}, **kwargs):
        """Pack the widget, then return it for chaining."""
        super().pack_configure(cnf, **kwargs)
        return self

    def grid_configure(self, cnf={}, **kwargs):
        """Grid the widget, then return it for chaining."""
        super().grid_configure(cnf, **kwargs)
        return self

    def place_configure(self, cnf={}, **kwargs):
        """Place the widget, then return it for chaining."""
        super().place_configure(cnf, **kwargs)
        return self

    pack = pack_configure
    grid = grid_configure
    place = place_configure


class BootMixin(FluentGeometryMixin, BusyMixin):
    """Mixin that adds the ``bootstyle`` API to a ttk widget class.

    Concrete subclasses such as ``class Button(BootMixin, ttk.Button)`` are
    shipped and re-exported. Mixing this in front of any ttk-derived class
    gives that class:

    - a ``bootstyle=`` (and bare ``style=``) keyword on the constructor,
    - an ``icon=``/``icon_size=`` keyword for a theme-aware glyph (see
      `ttkbootstrap.apply_icon`) on the widgets that carry a label image,
    - ``configure``/``config`` that accept and report ``bootstyle``,
    - ``widget["bootstyle"]`` / ``widget["bootstyle"] = ...`` access.

    All resolution flows through `Bootstyle.update_ttk_widget_style`, so the
    mixin only changes *delivery* — not how a style string maps to a ttk
    style.
    """

    def __init__(self, *args, **kwargs):
        """Construct the widget, then resolve and apply its style and icon.

        Parameters:

            *args:
                Positional arguments forwarded to the wrapped ttk widget's
                constructor.

            **kwargs:
                Keyword arguments forwarded to the wrapped ttk widget's
                constructor. ``bootstyle``, ``style``, ``icon``, ``icon_size``,
                and ``icon_only`` are consumed here rather than forwarded.
        """
        # capture bootstyle, style, and icon arguments
        bootstyle = kwargs.pop("bootstyle", "")
        style = kwargs.pop("style", "") or ""
        icon = kwargs.pop("icon", None)
        # size defaults inside apply_icon (icon-only-aware); None = "not given"
        icon_size = kwargs.pop("icon_size", None)
        icon_only = kwargs.pop("icon_only", False)

        # instantiate the underlying ttk widget first so winfo_class() is
        # available to the resolver below
        super().__init__(*args, **kwargs)

        try:
            if style:
                if Style.get_instance().style_exists_in_theme(style):
                    super().configure(style=style)
                else:
                    ttkstyle = Bootstyle.update_ttk_widget_style(
                        self, style, **kwargs
                    )
                    super().configure(style=ttkstyle)
            elif bootstyle:
                ttkstyle = Bootstyle.update_ttk_widget_style(
                    self, bootstyle, **kwargs
                )
                super().configure(style=ttkstyle)
            else:
                ttkstyle = Bootstyle.update_ttk_widget_style(
                    self, "default", **kwargs
                )
                super().configure(style=ttkstyle)
            # Stamp the widget current so the next theme walk only repaints it
            # once the theme actually changes.
            Bootstyle.stamp_theme_version(self)
            # Apply a theme-aware icon last, so it derives from the resolved base
            # style (see ttkbootstrap.apply_icon).
            if icon:
                from ttkbootstrap.style.icons import apply_icon
                apply_icon(self, icon, size=icon_size, icon_only=icon_only)
            elif icon_only:
                warnings.warn(
                    "icon_only=True has no effect without icon=...; ignoring.",
                    UserWarning, stacklevel=2,
                )
        except AttributeError:
            # Third-party widgets (e.g. tkcalendar.Calendar) override
            # configure() and may touch instance attributes not yet set when
            # ttk.Frame.__init__ calls back into the subclass configure before
            # the subclass __init__ completes.
            pass

    def configure(self, cnf=None, **kwargs):
        """Get or set widget options, resolving ``bootstyle``/``style``/
        ``icon`` changes along the way.

        Parameters:

            cnf (str | dict | None):
                An option name to query, a dict of options to set, or
                ``None`` to set from ``**kwargs``.

            **kwargs:
                Options to set, including ``bootstyle``, ``style``, ``icon``,
                and ``icon_size``. A surface (2.0 surface-color) rides in the
                ``bootstyle``/``style`` string as an ``@<surface>`` token.
        """
        # query a single option
        if cnf in ("bootstyle", "style"):
            return self.cget("style")
        if cnf is not None:
            return super().configure(cnf)

        # capture icon changes; applied after the base style resolves below
        icon = kwargs.pop("icon", _UNSET)
        icon_size = kwargs.pop("icon_size", _UNSET)
        icon_only = kwargs.pop("icon_only", _UNSET)

        # set configuration
        bootstyle = kwargs.pop("bootstyle", "")
        base_changed = bool(bootstyle) or ("style" in kwargs)
        if "style" in kwargs:
            style = kwargs.get("style")
            Bootstyle.update_ttk_widget_style(self, style, **kwargs)
        elif bootstyle:
            ttkstyle = Bootstyle.update_ttk_widget_style(
                self, bootstyle, **kwargs
            )
            kwargs.update(style=ttkstyle)

        result = super().configure(cnf, **kwargs)

        # Icon handling. An explicit icon=/icon_size= applies or clears the glyph;
        # otherwise a base-style change under an existing icon re-derives it onto
        # the new base. The _tb_applying_icon guard skips the re-derive while
        # apply_icon is itself setting the derived style (avoids recursion).
        if icon is not _UNSET or icon_size is not _UNSET or icon_only is not _UNSET:
            from ttkbootstrap.style.icons import apply_icon
            existing = getattr(self, "_tb_icon", None)
            name = icon if icon is not _UNSET else (existing["name"] if existing else None)
            # size: explicit wins; else if icon_only was just toggled, re-default
            # (None -> apply_icon's icon-only-aware default); else keep the spec's.
            if icon_size is not _UNSET:
                size = icon_size
            elif icon_only is not _UNSET:
                size = None
            else:
                size = existing["size"] if existing else None
            states = existing["states"] if existing else None
            compound = existing["compound"] if existing else None
            only = (icon_only if icon_only is not _UNSET
                    else (existing.get("icon_only", False) if existing else False))
            apply_icon(self, name, size=size, states=states,
                       compound=compound, icon_only=only)
        elif (base_changed and getattr(self, "_tb_icon", None)
                and not getattr(self, "_tb_applying_icon", False)):
            from ttkbootstrap.style.icons import apply_icon
            spec = self._tb_icon
            apply_icon(self, spec["name"], size=spec["size"],
                       states=spec["states"], compound=spec["compound"],
                       icon_only=spec.get("icon_only", False))

        return result

    config = configure

    def __setitem__(self, key, value):
        if key in ("bootstyle", "style"):
            return self.configure(**{key: value})
        return super().__setitem__(key, value)

    def __getitem__(self, key):
        if key in ("bootstyle", "style"):
            return self.cget("style")
        return super().__getitem__(key)


class AutoStyleMixin(FluentGeometryMixin, BusyMixin):
    """Mixin that auto-applies the theme to a legacy ``tk`` widget class.

    The tk counterpart to `BootMixin`. Legacy tk widgets have no ttk style;
    instead they are painted with the active theme's colors at construction
    via `Bootstyle.update_tk_widget_style`. Concrete subclasses such as
    ``class Canvas(AutoStyleMixin, tk.Canvas)`` are re-exported from
    ttkbootstrap.

    Passing ``autostyle=False`` opts the widget out of theming entirely: it
    keeps its native tk look and the theme walk skips it on switch (the
    ``_tb_no_autostyle`` flag).
    """

    def __init__(self, *args, **kwargs):
        """Construct the widget, then apply the active theme unless
        ``autostyle=False`` is passed.

        Parameters:

            *args:
                Positional arguments forwarded to the wrapped tk widget's
                constructor.

            **kwargs:
                Keyword arguments forwarded to the wrapped tk widget's
                constructor. ``autostyle`` (default ``True``) is consumed
                here rather than forwarded.
        """
        autostyle = kwargs.pop("autostyle", True)
        super().__init__(*args, **kwargs)
        if autostyle:
            Bootstyle.update_tk_widget_style(self)
            Bootstyle.stamp_theme_version(self)
        else:
            self._tb_no_autostyle = True


def bootify(cls):
    """Return a ``bootstyle``-enabled subclass of any ttk widget class.

    Use this to wrap a third-party ttk-derived widget that ttkbootstrap does
    not ship a subclass for:

    ```python
    ThemedGadget = bootify(Gadget)
    gadget = ThemedGadget(root, bootstyle="info")
    ```

    The result is ``type(cls.__name__, (BootMixin, cls), {})`` — the same
    construction used for the widgets ttkbootstrap ships, so it gains the full
    ``bootstyle`` API without mutating the original class.

    How much of the vocabulary applies depends on the widget's ttk class:

    - A widget that keeps a **standard ttk class** (a subclass of
      ``ttk.Button``, ``ttk.Entry``, …) gets the full vocabulary — it behaves
      exactly like the corresponding ttkbootstrap widget.
    - A widget with its **own ttk class** has no ttkbootstrap style recipe: a
      bare color (``bootstyle="info"``) warns and leaves the widget's style
      unchanged. Name a base type explicitly (``bootstyle="info-frame"``) to
      borrow a standard recipe where the widget's elements support it.

    A composite widget's internals follow the active theme on their own
    (standard-class children resolve against the per-theme base styles), but
    the accent is not fanned out to them — which child should carry it is the
    widget's design, not something a wrapper can infer. To accent a specific
    internal, use `apply_bootstyle` on that child.
    """
    return type(cls.__name__, (BootMixin, cls), {})


def apply_bootstyle(widget, bootstyle: BootStyle | str) -> str:
    """Apply a bootstyle to an existing widget instance, no class mutation.

    For per-instance styling of a widget whose class was never wrapped (for
    example a plain ``tkinter.ttk`` widget): resolves the bootstyle to a ttk
    style, assigns it, and stamps the widget current for the theme walk.

    ```python
    from tkinter import ttk
    b = ttk.Button(root, text="Save")
    apply_bootstyle(b, "success")
    ```

    The same widget-class rules as `bootify` apply: a widget with its own ttk
    class has no style recipe, so a bare color warns and leaves the style
    unchanged — name a base type explicitly (``"info-frame"``) to borrow a
    standard recipe.

    Returns the resolved ttk style name.
    """
    ttkstyle = Bootstyle.update_ttk_widget_style(widget, bootstyle)
    widget.configure(style=ttkstyle)
    Bootstyle.stamp_theme_version(widget)
    return ttkstyle


_global_api_installed = False


def enable_global_api():
    """Re-apply the legacy global monkey-patch (opt-in).

    By default the styling API is delivered through concrete subclasses
    (`BootMixin`/`AutoStyleMixin`), so importing ttkbootstrap does not mutate
    the stock ``tkinter``/``tkinter.ttk`` classes. Call this once if you have
    code that creates *vanilla* ttk/tk widgets (e.g. ``from tkinter import
    ttk; ttk.Button(..., bootstyle=...)``) and want the ``bootstyle``/
    ``autostyle`` keywords on them anyway. It also makes ``pack``/``grid``/
    ``place`` return the widget on every widget (see
    `Bootstyle.patch_geometry_managers`), extending `FluentGeometryMixin`
    beyond the blessed subclasses.

    Idempotent. The installed wrappers defer to `BootMixin`/`AutoStyleMixin`
    instances (the blessed subclasses), so enabling the global API never
    double-resolves a style for a widget that already carries a mixin.
    """
    global _global_api_installed
    if _global_api_installed:
        return
    Bootstyle.setup_ttkbootstrap_api()
    _global_api_installed = True
