"""Public layout / element / statespec / name helpers for ttkbootstrap styles.

Small, composable helpers that absorb the boilerplate every style builder
repeats: the nested layout tuple/dict pyramids (`El` + `layout`), image element
state->image maps (`image_element`), `style.map` state maps (`state_map`), the
`!negation`/space-AND state grammar validation (`statespec`), and the
colorname/orientation/`.TS->.S` name surgery (`StyleName`).

They are thin wrappers, not a DSL: each does one mechanical job, holds no state
of its own, calls methods on the `Style` instance passed in, and composes freely
with raw `style.element_create`/`style.layout`/`style.map` calls. Top-level
imports are tkinter constants only -- no engine edge, so these stay leaves in
the package layering.
"""
from ttkbootstrap.constants import DEFAULT, PRIMARY, surface_segment


# The canonical ttk widget state tokens. `statespec`/`state_map` validate against
# this set so a typo ("diabled") fails loudly at style-build time instead of
# silently never matching. This is the loud-failure seam shared with Workstream D
# -- keep the token set here, in one place, for both to import.
TTK_STATES = frozenset({
    "active", "alternate", "background", "disabled", "focus", "hover",
    "invalid", "pressed", "readonly", "selected",
})


def statespec(spec):
    """Validate a ttk state string and split it into a tuple of tokens.

    Tokens are space-separated; each may be negated with a leading `!`
    ("!selected"). An unknown token raises `ValueError`.
    """
    tokens = tuple(spec.split())
    for token in tokens:
        base = token[1:] if token.startswith("!") else token
        if base not in TTK_STATES:
            raise ValueError(
                f"unknown widget state {token!r}; valid tokens are "
                f"{', '.join(sorted(TTK_STATES))} (optionally '!'-negated)"
            )
    return tokens


class El:
    """A ttk layout element: a name, layout options, and child elements.

    `layout()` lowers an `El` tree to ttk's nested `(name, {opts, "children":
    [...]})` form. Mirrors bootstack's `Element.spec()`, but takes children as a
    constructor `children=[...]` kwarg (unambiguous; reads as the tree it builds)
    rather than fluent positional parenting.
    """

    __slots__ = ("name", "options", "children")

    def __init__(self, name, *, side=None, sticky=None, expand=None,
                 border=None, children=None):
        self.name = name
        self.children = list(children) if children else []
        options = {}
        if side is not None:
            options["side"] = side
        if sticky is not None:
            options["sticky"] = sticky
        if expand is not None:
            options["expand"] = expand
        if border is not None:
            options["border"] = border
        self.options = options

    def spec(self):
        """Lower this element (and its subtree) to a ttk `(name, opts)` tuple."""
        options = dict(self.options)
        if self.children:
            options["children"] = [child.spec() for child in self.children]
        return (self.name, options)


def register_style(style, ttk_style):
    """Register a hand-built ttk style name with the ttkbootstrap engine.

    A custom style applied to a ttkbootstrap widget via `style="My.TButton"` is
    **silently re-resolved to its base style** unless the engine knows the name --
    `bootstyle` resolution only honors `style=` for a *registered* style. Building
    a style with the toolkit (`element_create`/`image_element`/`icon_element`/
    `map`) does not register it on its own; call this (or `layout()`, which calls
    it for you) so `style="<ttk_style>"` resolves to what you built.

    Registration is per *active* theme (it mirrors the built-in builders). A
    hand-built style is not auto-rebuilt on a theme switch, so re-build + re
    -register it if you change themes -- engine-managed theme-follow for custom
    styles is a separate effort.
    """
    style._register_ttkstyle(ttk_style)


def layout(style, ttk_style, root):
    """Apply an `El` (or list of `El`s) as the layout for `ttk_style`.

    Structural sugar over `style.layout(ttk_style, [...])`. Defining a layout is
    what gives a style its identity, so this also **registers** `ttk_style` with
    the engine (via `register_style`) -- a hand-built style whose terminal step is
    `layout()` resolves through `style="<ttk_style>"` with no extra step. (Built-in
    builders that also call `_register_ttkstyle` explicitly are unaffected --
    registration is an idempotent set add.)
    """
    roots = [root] if isinstance(root, El) else list(root)
    style.layout(ttk_style, [element.spec() for element in roots])
    register_style(style, ttk_style)


def image_element(style, name, *, default, states=None, **options):
    """Create an image element with a validated, ordered state->image map.

    Wraps `style.element_create(name, "image", default, *statespecs, **options)`.
    `states` is an ordered dict `{state_string: image}`; ttk matches statespecs
    first-match-wins, so the dict's insertion order *is* the match order, made
    explicit. Each state string is validated by `statespec` (a typo raises
    instead of silently never matching). `options` (width, border, sticky, ...)
    pass through to `element_create`.
    """
    args = [default]
    if states:
        for state_string, image in states.items():
            args.append((*statespec(state_string), image))
    style.element_create(name, "image", *args, **options)


def state_map(style, ttk_style, **options):
    """Validated `style.map` analog.

    Each keyword is a ttk option (e.g. `foreground=`) whose value is an ordered
    dict `{state_string: value}` (or an iterable of `(state_string, value)`
    pairs). State strings are validated by `statespec`. Replaces bare
    `foreground=[("disabled", fg)]` lists.
    """
    mapping = {}
    for option, spec in options.items():
        items = spec.items() if isinstance(spec, dict) else spec
        mapping[option] = [(*statespec(state_string), value)
                           for state_string, value in items]
    style.map(ttk_style, **mapping)


class StyleName:
    """Absorbs the colorname / orientation / `.TS->.S` name surgery builders repeat.

    From a ttk class token ("TScale", "TRadiobutton"), the requested colorname,
    and an optional orientation it derives the three names every builder opens
    with:

      .colorname  PRIMARY when the input is DEFAULT/"" (the per-widget default),
                  else the input unchanged.
      .ttk_style   the full ttk style name ("Horizontal.TScale",
                  "info.Horizontal.TScale", "TRadiobutton", ...).
      .element    the element-name prefix with the class token's leading "T"
                  dropped ("info.Horizontal.TScale" -> "info.Horizontal.Scale"),
                  matching the old `h_ttkstyle.replace(".TS", ".S")` dance.
    """

    __slots__ = ("colorname", "ttk_style", "element")

    def __init__(self, ttk_class, colorname=DEFAULT, orient=None, surface=""):
        is_default = colorname in (DEFAULT, "")
        self.colorname = PRIMARY if is_default else colorname

        prefix = surface_segment(surface)
        orient_prefix = f"{orient}." if orient else ""
        if is_default:
            self.ttk_style = f"{prefix}{orient_prefix}{ttk_class}"
        else:
            self.ttk_style = f"{prefix}{colorname}.{orient_prefix}{ttk_class}"

        element_class = ttk_class[1:] if ttk_class.startswith("T") else ttk_class
        self.element = self.ttk_style.replace(ttk_class, element_class)

    @property
    def ttkstyle(self):
        """Backward-compatible spelling of `ttk_style`."""
        return self.ttk_style
