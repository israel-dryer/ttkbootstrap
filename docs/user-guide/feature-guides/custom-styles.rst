Custom styles
=============

``bootstyle`` covers the looks the themes ship. When you need something it can't
name — a bespoke shape, your own element tree, a one-off tweak — a public toolkit
lets you build a ttk style yourself and apply it with ``style=``.

Tweak an existing style
-----------------------

The simplest custom style is a named variant of a base one. ``style.configure``
a dotted name, then hand it to a widget with ``style=``; the name inherits from
its base class (``my.TButton`` → ``TButton``), so you only set what changes:

.. code-block:: python

   import ttkbootstrap as ttk

   app = ttk.App()

   app.style.configure("big.TButton", font=("Helvetica", 16), padding=12)
   ttk.Button(app, text="Big", style="big.TButton").pack()

   app.mainloop()

Build a style from scratch
--------------------------

.. admonition:: Advanced
   :class: caution

   This is an advanced feature. It works directly with ttk's own element and
   layout model — element trees, element options, and state specs — which this
   guide does not teach. The toolkit below makes that model easier to drive, but
   assumes you're comfortable with how ttk styling works. For the underlying
   concepts, see the `tkinter.ttk styling
   <https://docs.python.org/3/library/tkinter.ttk.html#ttk-styling>`__ reference.

For a genuinely new look, compose one from **assets**, **elements**, a **state
map**, and a **layout**. Each piece is a small toolkit call:

- :class:`~ttkbootstrap.Assets` renders cached images from recipes
  (``circle``, ``rounded_rect``, ``rect``, ``icon``) or an ``image`` draw
  callback. Sizes are logical UI units — DPI scaling is handled for you.
- ``image_element`` turns an image into a named ttk element (optionally
  state-keyed).
- ``state_map`` is a validated ``style.map`` — a typo in a state string raises
  instead of silently doing nothing.
- ``layout`` arranges elements into the widget's element tree with ``El`` nodes,
  and registers the style for you.

.. code-block:: python

   import ttkbootstrap as ttk
   from ttkbootstrap import Assets, El, layout, image_element, state_map

   app = ttk.App()
   style = app.style
   assets = Assets(style)

   pill = assets.rounded_rect(style.colors.primary, size=(80, 28), radius=14)

   image_element(
        style,
        "Pill.TButton.background",
        default=pill,
        border=14,
        sticky="nsew"
   )

   state_map(
        style,
        "Pill.TButton",
        foreground={"disabled": style.colors.border}
   )

   layout(style, "Pill.TButton",
            El("Pill.TButton.background", sticky="nsew", children=[
                El("Button.label", side="left", expand=True)])
   )

   ttk.Button(app, text="Go", style="Pill.TButton").pack()

   app.mainloop()

Because ``layout`` registers the name, ``style="Pill.TButton"`` resolves to what
you built. If you configure a style but never call ``layout`` on it, register it
yourself with ``register_style`` so ttkbootstrap doesn't re-resolve the name back
to the base.

Icons
-----

The same asset pipeline renders Bootstrap Icons glyphs. To put an icon *on a
widget* — the ``icon=`` keyword, the imperative ``apply_icon``, or the standalone
``Icon`` image — see the :doc:`Icons guide </user-guide/feature-guides/icons>`.

What belongs *here* is placing a glyph inside a style **layout** you build
yourself: ``icon_element`` creates a ttk image element whose per-state image is a
glyph, so a custom indicator (a checkbox, a toggle) can be drawn from the font
instead of a raster asset. Unlike ``image_element`` it takes glyph *names* (not
pre-rendered images), a required ``size=``, and an element name of the form
``<ttkstyle>.<element>`` — the glyph color follows that style's foreground. Give a
``default`` glyph plus a ``states`` map of state → glyph:

.. code-block:: python

   from ttkbootstrap import icon_element, layout, El

   icon_element(
       style,
       "Star.TCheckbutton.indicator",
       size=18,
       default={"name": "star", "color": "warning"},
       states={"selected": "star-fill"},
       sticky="w",
   )

   layout(style, "Star.TCheckbutton",
       El("Star.TCheckbutton.indicator", side="left", children=[
           El("Checkbutton.label", side="left", expand=True)])
   )

   ttk.Checkbutton(app, text="Favorite", style="Star.TCheckbutton").pack()

Creating theme-aware styles
---------------------------

A custom style is built against the **active** theme, so a theme switch repaints
the built-in widgets but leaves your style untouched — its colors go stale. Wrap
the build in ``@theme_aware`` and it re-runs after every switch, rebuilding
against the new theme's ``style.colors``:

.. code-block:: python

   from ttkbootstrap import theme_aware, Assets, El, layout, image_element

   @theme_aware        # runs once now, and again after every theme change
   def build_pill(style):
       fill = style.colors.primary
       pill = Assets(style).rounded_rect(fill, size=(80, 28), radius=14)
       image_element(
            style,
            "Pill.TButton.background",
            default=pill,
            border=14,
            sticky="nsew"
       )

       layout(style, "Pill.TButton",
            El("Pill.TButton.background", sticky="nsew", children=[
                El("Button.label", side="left", expand=True)])
       )

Now ``ttk.Button(app, style="Pill.TButton")`` stays correct through
``theme_use`` and ``toggle_theme``. ``theme_aware`` even works at module top
level, before the app exists — the build is queued and runs when the app is
created. Use ``on_theme_change(fn)`` for the plain-function form, and
``remove_theme_change_callback(fn)`` to unregister.

.. seealso::

   - :doc:`Styling reference </reference/styling>` — the ``Assets`` / ``El`` /
     ``layout`` / ``image_element`` / ``register_style`` API.
   - :doc:`Theming & Colors </user-guide/feature-guides/theming>` — the
     ``style.colors`` palette custom styles draw from.
   - :doc:`Icons </user-guide/feature-guides/icons>` — putting a glyph *on* a
     widget, rather than inside a style layout.
