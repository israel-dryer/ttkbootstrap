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
from ttkbootstrap.constants import DEFAULT, PRIMARY


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

    ```python
    statespec("disabled selected")  # -> ("disabled", "selected")
    statespec("!selected")          # -> ("!selected",)
    ```
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
    """A ttk layout element: a name, layout options, and child `El`s.

    `layout()` lowers an `El` tree to ttk's nested `(name, {opts, "children":
    [...]})` form. Mirrors bootstack's `Element.spec()`, but takes children as a
    constructor `children=[...]` kwarg (unambiguous; reads as the tree it builds)
    rather than fluent positional parenting.

    ```python
    El("Radiobutton.padding", sticky=NSEW, children=[
        El(f"{ttkstyle}.indicator", side=LEFT),
        El("Radiobutton.focus", side=LEFT, children=[
            El("Radiobutton.label", sticky=NSEW)])])
    ```
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


def layout(style, ttkstyle, root):
    """Apply an `El` (or list of `El`s) as the layout for `ttkstyle`.

    Pure structural sugar over `style.layout(ttkstyle, [...])`.
    """
    roots = [root] if isinstance(root, El) else list(root)
    style.layout(ttkstyle, [element.spec() for element in roots])


def image_element(style, name, *, default, states=None, **options):
    """Create an image element with a validated, ordered state->image map.

    Wraps `style.element_create(name, "image", default, *statespecs, **options)`.
    `states` is an ordered dict `{state_string: image}`; ttk matches statespecs
    first-match-wins, so the dict's insertion order *is* the match order, made
    explicit. Each state string is validated by `statespec` (a typo raises
    instead of silently never matching). `options` (width, border, sticky, ...)
    pass through to `element_create`.

    ```python
    image_element(style, f"{ttkstyle}.indicator", default=on,
        states={"disabled selected": on_disabled, "disabled": disabled,
                "!selected": off},
        width=20, border=4, sticky=W)
    ```
    """
    args = [default]
    if states:
        for state_string, image in states.items():
            args.append((*statespec(state_string), image))
    style.element_create(name, "image", *args, **options)


def state_map(style, ttkstyle, **options):
    """Validated `style.map` analog.

    Each keyword is a ttk option (e.g. `foreground=`) whose value is an ordered
    dict `{state_string: value}` (or an iterable of `(state_string, value)`
    pairs). State strings are validated by `statespec`. Replaces bare
    `foreground=[("disabled", fg)]` lists.

    ```python
    state_map(style, ttkstyle, foreground={"disabled": disabled_fg})
    ```
    """
    mapping = {}
    for option, spec in options.items():
        items = spec.items() if isinstance(spec, dict) else spec
        mapping[option] = [(*statespec(state_string), value)
                           for state_string, value in items]
    style.map(ttkstyle, **mapping)


class StyleName:
    """Absorbs the colorname / orientation / `.TS->.S` name surgery builders repeat.

    From a ttk class token ("TScale", "TRadiobutton"), the requested colorname,
    and an optional orientation it derives the three names every builder opens
    with:

      .colorname  PRIMARY when the input is DEFAULT/"" (the per-widget default),
                  else the input unchanged.
      .ttkstyle   the full ttk style name ("Horizontal.TScale",
                  "info.Horizontal.TScale", "TRadiobutton", ...).
      .element    the element-name prefix with the class token's leading "T"
                  dropped ("info.Horizontal.TScale" -> "info.Horizontal.Scale"),
                  matching the old `h_ttkstyle.replace(".TS", ".S")` dance.

    ```python
    sn = StyleName("TScale", colorname, orient="Horizontal")
    sn.colorname    # PRIMARY when colorname was DEFAULT/"", else as given
    sn.ttkstyle     # "Horizontal.TScale" or "primary.Horizontal.TScale"
    sn.element      # "Horizontal.Scale"
    ```
    """

    __slots__ = ("colorname", "ttkstyle", "element")

    def __init__(self, ttkclass, colorname=DEFAULT, orient=None):
        is_default = colorname in (DEFAULT, "")
        self.colorname = PRIMARY if is_default else colorname

        orient_prefix = f"{orient}." if orient else ""
        if is_default:
            self.ttkstyle = f"{orient_prefix}{ttkclass}"
        else:
            self.ttkstyle = f"{colorname}.{orient_prefix}{ttkclass}"

        element_class = ttkclass[1:] if ttkclass.startswith("T") else ttkclass
        self.element = self.ttkstyle.replace(ttkclass, element_class)
