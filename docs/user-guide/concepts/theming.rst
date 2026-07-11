Theming
=======

A **theme** decides what every ``bootstyle`` color actually renders as. Each
theme is built from a small set of **semantic anchors** — the accent colors
(``primary``, ``success``, ``info``, ``warning``, ``danger``) plus a neutral gray
— resolved against a light or dark surface. Pick a theme and the whole interface,
including your ``bootstyle`` widgets, recolors coherently.

Choosing a theme
----------------

Pass ``theme=`` to the app. The default is ``bootstrap-light``:

.. code-block:: python

   import ttkbootstrap as ttk

   app = ttk.App(theme="nord-light")

   ttk.Button(app, text="Primary", bootstyle="primary").pack()

   app.mainloop()

.. note::

   ``themename=`` is an accepted alias for ``theme=`` (the pre-2.0 spelling); use
   whichever you prefer.

Switching at runtime
--------------------

Switch themes on a live app through the style engine — every mounted widget
repaints:

.. code-block:: python

   app.style.theme_use("solarized-dark")   # switch
   app.style.theme_use()                    # -> the current theme name
   app.style.theme_names()                  # -> every registered theme name

Light and dark
--------------

Built-in themes come in ``<family>-light`` / ``<family>-dark`` pairs, so a family
has a matched light and dark surface. Flip between them without naming the
counterpart:

.. code-block:: python

   app.theme_mode          # "light" or "dark"
   app.toggle_theme_mode() # light <-> dark within the family, returns the new mode
   app.use_theme_mode("dark")

A toggle button is the common case:

.. code-block:: python

   import ttkbootstrap as ttk

   app = ttk.App(theme="nord-light")

   ttk.Button(app, text="Toggle theme",
              command=app.toggle_theme_mode, bootstyle="primary").pack()

   app.mainloop()

To pair themes from different families (say a light theme with an unrelated dark
one), set the pair explicitly with ``app.set_theme_modes(light=..., dark=...)`` or
``App(light_theme=..., dark_theme=...)``.

The built-in catalog
--------------------

ttkbootstrap ships **15 theme families** — ``bootstrap``, ``pydata``, ``nord``,
``solarized``, ``catppuccin``, ``gruvbox``, ``dracula``, ``tokyo-night``, ``one``,
``everforest``, ``vapor``, ``minty``, ``pulse``, ``united``, ``sandstone`` — each
with a light and dark variant, for **30 built-in themes**. List them live with
``app.style.theme_names()``.

.. admonition:: Coming from 1.x
   :class: note

   The pre-2.0 Bootswatch theme names (``"darkly"``, ``"cosmo"``, …) are no longer
   registered by default. Call :func:`~ttkbootstrap.install_legacy_themes` to
   register them all (it warns, and they are removed in 3.0), or just name one —
   ``App(themename="darkly")`` lazily registers that single theme with a warning.

The Theme model
---------------

Each theme is a semantic-anchor :class:`~ttkbootstrap.Theme` — a family described
by its accent anchors and its light/dark surfaces, from which ttkbootstrap
derives the full color set for each mode. To build your own, see
:doc:`Make your own theme <make-your-own-theme>`.
