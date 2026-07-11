Make your own style
===================

``bootstyle`` covers the looks the themes ship. When you need something it can't
name — a bespoke shape, your own element tree, a one-off tweak — 2.0 gives you a
public toolkit to build a ttk style yourself and apply it with ``style=``.

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

   image_element(style, "Pill.TButton.background", default=pill, border=14, sticky="nsew")
   state_map(style, "Pill.TButton", foreground={"disabled": style.colors.border})
   layout(style, "Pill.TButton", El(
       "Pill.TButton.background", sticky="nsew",
       children=[El("Button.label", side="left", expand=True)],
   ))

   ttk.Button(app, text="Go", style="Pill.TButton").pack(padx=20, pady=20)

   app.mainloop()

Because ``layout`` registers the name, ``style="Pill.TButton"`` resolves to what
you built. If you configure a style but never call ``layout`` on it, register it
yourself with ``register_style`` so ttkbootstrap doesn't re-resolve the name back
to the base.

Icons
-----

The same asset pipeline renders Bootstrap Icons glyphs. :class:`~ttkbootstrap.Icon`
returns a cached image name you can drop into any ``image=`` option:

.. code-block:: python

   from ttkbootstrap import Icon

   ttk.Button(app, text="Save", image=Icon("save", size=16, color="light"),
              compound="left").pack()

For an icon that follows the widget's foreground and state automatically, pass
the ``icon=`` keyword instead of building the image yourself:

.. code-block:: python

   ttk.Button(app, text="Save", icon="save", bootstyle="success").pack()

.. admonition:: Theme switches
   :class: note

   Custom styles are registered against the **active** theme and are not rebuilt
   automatically when you switch themes. Re-apply them after a
   ``theme_use``/``toggle_theme`` if you need them to survive a switch.
