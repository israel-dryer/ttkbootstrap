"""The bootstyle resolver and delivery API.

`Bootstyle` maps a `bootstyle`/`style` string to a built ttk style (reading the
`Keywords` grammar). `BootMixin`/`AutoStyleMixin` are the concrete-subclass
delivery path; `bootify`/`apply_bootstyle`/`enable_global_api` are the dynamic
and opt-in-global delivery primitives. Top layer of the `style` package. Split
out of the monolithic `style.py` in 2.0.
"""
import difflib
import re
from tkinter import TclError, ttk

from ttkbootstrap.constants import (
    BOOTSTYLE_COLORS,
    BOOTSTYLE_MODIFIERS,
    BOOTSTYLE_INTERNAL_MODIFIERS,
    BOOTSTYLE_FAMILIES,
    BOOTSTYLE_ORIENTS,
    BootStyle,
)
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

    As of 2.0 (Workstream D) the token lists are sourced from the single
    vocabulary in `ttkbootstrap.constants` -- this class no longer keeps a
    second copy. The "type" slot spans both public modifiers (`outline`,
    `round`, ...) and the internal composite modifiers (`meter`, `date`, ...).
    The compiled patterns are retained for the orientation lookup and any
    back-compat callers; the primary parse path is the token classifier below.
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


def _classify_tokens(style_string, *, source=None, warn=False):
    """Split a bootstyle string and classify each token into a slot.

    Returns ``(color, modifier, base, orient)`` -- the first token seen for each
    slot (matching the pre-2.0 leftmost-wins behavior). When ``warn`` is true,
    an unrecognized token and a duplicate-slot token are reported through the
    `_compat` loud-failure path (warn by default, raise in strict mode).
    """
    source = style_string if source is None else source
    color = modifier = base = orient = ""
    for token in _TOKEN_SPLIT.split(style_string.strip().lower()):
        if token in _SENTINELS:
            continue
        if token in _COLORS:
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
    return color, modifier, base, orient


def _looks_like_style_name(style_string):
    """Return whether the input is an already-built ttk style name.

    The resolver accepts two dialects. A *bootstyle* is lowercase and dash/space
    separated (``"primary-outline"``). A built *ttk style name* always has a
    Title-cased class component, so it contains an uppercase letter and no dash
    or space (``"TFrame"``, ``"primary.Outline.TButton"``, ``"symbol.Link.
    TButton"``); a dotted string is always a style name. This lets the theme
    walk re-resolve a widget's dotted ``cget("style")`` (including a bare base
    like ``"TFrame"``) without misreading it as a mistyped bootstyle.
    """
    if "." in style_string:
        return True
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
    custom style names. Segments are split on ``.``; the class segment is
    title-cased with an optional ``T`` prefix, so ``TButton`` -> ``button`` but
    ``Treeview``/``Toggle`` map directly. Unknown segments (custom prefixes such
    as ``symbol``) are ignored *without* warning -- style names legitimately
    carry them, unlike a user's bootstyle.
    """
    color = modifier = base = orient = ""
    for segment in name.split("."):
        seg = segment.strip().lower()
        if not seg or seg in _SENTINELS:
            continue
        if seg in _COLORS:
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
    return color, modifier, base, orient


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


def _build_ttkstyle_name(color, modifier, orient, family):
    """Assemble the dotted ttk style name from resolved slot tokens.

    Preserves the exact pre-2.0 casing: the color stays lowercase, the modifier
    and orientation are title-cased, and the family is title-cased with a ``T``
    prefix unless it already starts with ``t`` (``Treeview``, ``Toplevel``).
    """
    color = f"{color}." if color else ""
    modifier = f"{modifier.title()}." if modifier else ""
    orient = f"{orient.title()}." if orient else ""
    if family.startswith("t"):
        family = family.title()
    else:
        family = f"T{family.title()}"
    return f"{color}{modifier}{orient}{family}"


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
        _, _, base, _ = _classify_tokens(string)
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
        _, modifier, _, _ = _classify_tokens(string)
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
        color, _, _, _ = _classify_tokens(string)
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
        color, modifier, _, orient, family = Bootstyle._parse_components(
            widget, style_string, warn=False, **kwargs
        )
        return _build_ttkstyle_name(color, modifier, orient, family)

    @staticmethod
    def _parse_components(widget, style_string, *, warn, **kwargs):
        """Resolve a bootstyle/style string to ``(color, modifier, base,
        orient, family)``.

        A dotted input is an already-built ttk style name and is parsed
        leniently (`_classify_style_name`); a dashed/spaced input is a bootstyle
        and goes through the closed-vocab tokenizer, which fails loudly on
        unknown tokens when ``warn`` is set. ``family`` is the explicit base
        token if present, else inferred from the widget.
        """
        if _looks_like_style_name(style_string):
            color, modifier, base, orient = _classify_style_name(style_string)
            if not orient:
                orient = Bootstyle.ttkstyle_widget_orient(
                    widget, "", **kwargs
                )
        else:
            color, modifier, base, _ = _classify_tokens(
                style_string, warn=warn
            )
            orient = Bootstyle.ttkstyle_widget_orient(
                widget, style_string, **kwargs
            )
        family = base or _infer_family(widget)
        return color, modifier, base, orient, family

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
                The style string to evalulate. May be the `style`, `ttkstyle`
                or `bootstyle` argument depending on the context and scenario.

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
        color, modifier, _, orient, family = Bootstyle._parse_components(
            widget, style_string, warn=True, **kwargs
        )
        variant = modifier or DEFAULT_VARIANT
        ttkstyle = _build_ttkstyle_name(color, modifier, orient, family)

        # build style if not existing (example: theme changed)
        if not style.style_exists_in_theme(ttkstyle):
            builder: StyleBuilderTTK = style._get_builder()
            if not builder.build_style(variant, family, color):
                if family in _FAMILIES and variant != DEFAULT_VARIANT:
                    # An invalid modifier for one of our own widgets
                    # (e.g. "outline-scale"): fail loudly for a bootstyle string,
                    # then fall back to the family's default style rather than
                    # returning the unusable raw fragment.
                    if is_bootstyle and modifier:
                        _compat.report_invalid(
                            "combination", f"{modifier}-{family}", style_string
                        )
                    ttkstyle = _build_ttkstyle_name(color, "", orient, family)
                    if not style.style_exists_in_theme(ttkstyle) and (
                        not builder.build_style(DEFAULT_VARIANT, family, color)
                    ):
                        return style_string
                else:
                    # A third-party widget whose class maps to no ttkbootstrap
                    # builder: pass its style through untouched.
                    return style_string

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

        As of 2.0 this is the legacy *global* path and is no longer run at
        import time; the default api is delivered through concrete subclasses
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
        """Lookup the widget name and call the appropriate update
        method

        Parameters:

            widget (object):
                The tcl/tk name given by `tkinter.Widget.winfo_name()`
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


class BootMixin:
    """Mixin that adds the ``bootstyle`` API to a ttk widget class.

    This is the 2.0 delivery vehicle for the styling API. Instead of
    monkey-patching ttk widget classes at import time, ttkbootstrap ships
    concrete subclasses such as ``class Button(BootMixin, ttk.Button)`` and
    re-exports them. Mixing this in front of any ttk-derived class gives that
    class:

    - a ``bootstyle=`` (and bare ``style=``) keyword on the constructor,
    - an ``icon=``/``icon_size=`` keyword for a theme-aware glyph (see
      `ttkbootstrap.apply_icon`) on the widgets that carry a label image,
    - ``configure``/``config`` that accept and report ``bootstyle``,
    - ``widget["bootstyle"]`` / ``widget["bootstyle"] = ...`` access.

    All resolution flows through the unchanged `Bootstyle.update_ttk_widget_style`
    engine, so the mixin only changes *delivery* — not how a style string maps
    to a ttk style. Because the accessors are real methods that use ``super()``
    (not closures captured in a loop), the late-binding bug of the old
    monkey-patch is gone.
    """

    def __init__(self, *args, **kwargs):
        # capture bootstyle, style, and icon arguments
        bootstyle = kwargs.pop("bootstyle", "")
        style = kwargs.pop("style", "") or ""
        icon = kwargs.pop("icon", None)
        icon_size = kwargs.pop("icon_size", 16)

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
                apply_icon(self, icon, size=icon_size)
        except AttributeError:
            # Third-party widgets (e.g. tkcalendar.Calendar) override
            # configure() and may touch instance attributes not yet set when
            # ttk.Frame.__init__ calls back into the subclass configure before
            # the subclass __init__ completes.
            pass

    def configure(self, cnf=None, **kwargs):
        # query a single option
        if cnf in ("bootstyle", "style"):
            return self.cget("style")
        if cnf is not None:
            return super().configure(cnf)

        # capture icon changes; applied after the base style resolves below
        icon = kwargs.pop("icon", _UNSET)
        icon_size = kwargs.pop("icon_size", _UNSET)

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
        if icon is not _UNSET or icon_size is not _UNSET:
            from ttkbootstrap.style.icons import apply_icon
            existing = getattr(self, "_tb_icon", None)
            name = icon if icon is not _UNSET else (existing["name"] if existing else None)
            size = icon_size if icon_size is not _UNSET else (existing["size"] if existing else 16)
            states = existing["states"] if existing else None
            compound = existing["compound"] if existing else None
            apply_icon(self, name, size=size, states=states, compound=compound)
        elif (base_changed and getattr(self, "_tb_icon", None)
                and not getattr(self, "_tb_applying_icon", False)):
            from ttkbootstrap.style.icons import apply_icon
            spec = self._tb_icon
            apply_icon(self, spec["name"], size=spec["size"],
                       states=spec["states"], compound=spec["compound"])

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


class AutoStyleMixin:
    """Mixin that auto-applies the theme to a legacy ``tk`` widget class.

    The tk counterpart to `BootMixin`. Legacy tk widgets have no ttk style;
    instead they are painted with the active theme's colors at construction
    via `Bootstyle.update_tk_widget_style`. Concrete subclasses such as
    ``class Canvas(AutoStyleMixin, tk.Canvas)`` are re-exported from
    ttkbootstrap.

    Passing ``autostyle=False`` opts the widget out of theming entirely: it
    keeps its native tk look and the theme walk skips it on switch (the
    ``_tb_no_autostyle`` flag), matching the pre-2.0 behavior where an
    unstyled widget never subscribed for repaints.
    """

    def __init__(self, *args, **kwargs):
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
    not ship a blessed subclass for:

    ```python
    ThemedCalendar = bootify(tkcalendar.Calendar)
    cal = ThemedCalendar(root, bootstyle="info")
    ```

    The result is ``type(cls.__name__, (BootMixin, cls), {})`` — i.e. the same
    construction used for the built-in blessed widgets, so it gains the full
    ``bootstyle`` API without mutating the original class.
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

    Returns the resolved ttk style name.
    """
    ttkstyle = Bootstyle.update_ttk_widget_style(widget, bootstyle)
    widget.configure(style=ttkstyle)
    Bootstyle.stamp_theme_version(widget)
    return ttkstyle


_global_api_installed = False


def enable_global_api():
    """Re-apply the legacy global monkey-patch (opt-in).

    In 2.0 the default styling API is delivered through concrete subclasses
    (`BootMixin`/`AutoStyleMixin`), so importing ttkbootstrap no longer mutates
    the stock ``tkinter``/``tkinter.ttk`` classes. Call this once if you have
    code that creates *vanilla* ttk/tk widgets (e.g. ``from tkinter import
    ttk; ttk.Button(..., bootstyle=...)``) and want the ``bootstyle``/
    ``autostyle`` keywords on them anyway.

    Idempotent. The installed wrappers defer to `BootMixin`/`AutoStyleMixin`
    instances (the blessed subclasses), so enabling the global API never
    double-resolves a style for a widget that already carries a mixin.
    """
    global _global_api_installed
    if _global_api_installed:
        return
    Bootstyle.setup_ttkbootstrap_api()
    _global_api_installed = True
