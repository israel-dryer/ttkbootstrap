"""User-defined custom theme storage for ttkbootstrap.

Two stores, both loaded at startup by the Style engine:

- ``USER_THEME_SPECS`` — the **2.0** store: each entry is a semantic-anchor
  ``Theme`` spec (accent anchors + ``neutral`` + ``light``/``dark``
  ``{background, foreground}`` blocks). ttkcreator writes here; the engine builds
  a ``Theme`` from each spec and registers its generated ``<name>-light`` /
  ``<name>-dark`` variants. This is the recommended way to persist a custom theme.

- ``USER_THEMES`` — the legacy 16-key dict store (pre-2.0). Still loaded (through
  the compat adapter, which keeps the authored accents/bg/fg and regenerates the
  plumbing), so existing custom themes keep working.

Example (2.0 spec):
    ```python
    from ttkbootstrap.themes.user import USER_THEME_SPECS

    USER_THEME_SPECS["mytheme"] = {
        "primary": "#2780e3", "success": "#3fb618", "info": "#9954bb",
        "warning": "#ff7518", "danger": "#ff0039",
        "secondary": None, "neutral": "#7e8081",
        "light": {"background": "#ffffff", "foreground": "#373a3c"},
        "dark": {"background": "#222222", "foreground": "#f8f9fa"},
    }
    ```

    Then ``ttk.App(theme="mytheme-light")`` (or ``-dark``).

Prefer authoring in your own code with the public ``Theme`` API directly:
    ```python
    import ttkbootstrap as ttk
    ttk.Theme(name="mytheme", primary="#2780e3", ...,
              light=dict(background="#ffffff", foreground="#373a3c")).register()
    ```
"""

#: 2.0 semantic-anchor theme specs: name -> Theme(**spec) keyword dict.
USER_THEME_SPECS = {}

#: Legacy 16-key theme dicts (pre-2.0), adapted on load.
USER_THEMES = {}
