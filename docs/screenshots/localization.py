"""Screenshot scenes for docs/user-guide/feature-guides/localization.rst.

The page teaches live switching with ``LocaleVar`` + ``set_locale``; these scenes
render the *visual result* (the English vs Español states) with static text. The
msgcat locale machinery loads per-locale ``.msg`` files that are unreliable in a
headless capture on the canonical box, and the shot only needs the rendered look.
"""

import ttkbootstrap as ttk


def _window(app, heading):
    ttk.Label(app, text=heading, font="TkHeadingFont").pack(padx=20, pady=(16, 8))
    ttk.Label(app, text="Language").pack()
    for label in ["English", "Español"]:
        ttk.Button(app, text=label).pack(pady=2, padx=20)
    app.mainloop()


def english():
    _window(ttk.App(title="Localization"), "Welcome")


def spanish():
    _window(ttk.App(title="Localization"), "Bienvenido")


SCENES = {
    "english": english,
    "spanish": spanish,
}
