Make your own theme
===================

A theme is a handful of **semantic anchors** — the accent colors and a neutral
gray — plus a light and/or dark surface. Declare those, and ttkbootstrap derives
the full color set (borders, inputs, selections, hovers) for each mode.

Defining a theme
----------------

Build a :class:`~ttkbootstrap.Theme` from its anchors and register it. The five
accents are the mid-tone of each color; ``light``/``dark`` each give a background
and foreground. Registration needs a running app (a style must exist first):

.. code-block:: python

   import ttkbootstrap as ttk

   app = ttk.App()

   ttk.Theme(
       name="pulse",
       primary="#593196", success="#13b955", info="#009cdc",
       warning="#efa31d", danger="#fc3939",
       light=dict(background="#ffffff", foreground="#17141f"),
       dark=dict(background="#17141f", foreground="#e9ecef"),
   ).register()

   app.theme_use("pulse-light")   # registered as pulse-light and pulse-dark
   app.mainloop()

Registering a theme generates a ``<name>-light`` and ``<name>-dark`` variant for
whichever surfaces you declared, so it drops straight into
:doc:`light/dark switching <theming>` — ``app.toggle_theme()`` flips
``pulse-light`` ↔ ``pulse-dark``.

Re-branding a built-in
----------------------

To change just a color or two on an existing theme, derive from it with
``Theme.from_existing`` and override the anchors you care about:

.. code-block:: python

   from ttkbootstrap.themes.builtin import BOOTSTRAP

   ttk.Theme.from_existing(BOOTSTRAP, name="brand", primary="#ff6600").register()
   app.theme_use("brand-light")

The visual editor
-----------------

To design a theme interactively rather than by hand, run the bundled editor:

.. code-block:: bash

   python -m ttkcreator

Edit the accent anchors and the light/dark surfaces, preview against live
widgets, then **Export theme (.py)** -- you get a ``Theme(...).register()``
snippet (the same shape as above) to drop into your app. The editor doesn't
save into the library; your theme lives in your own code.
