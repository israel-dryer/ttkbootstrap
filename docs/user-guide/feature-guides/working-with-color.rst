Working with color
===================

The active theme resolves its palette to concrete hex values, and exposes them
through ``app.style.colors``. Read those colors whenever you draw your own
content — a ``Canvas``, a custom style, a chart — so it tracks the theme instead
of hard-coding hex.

Reading semantic colors
-----------------------

``style.colors`` gives attribute access to the theme's colors: the accents
(``primary``, ``secondary``, ``success``, ``info``, ``warning``, ``danger``,
``light``, ``dark``) and the interface roles (``bg``, ``fg``, ``selectbg``,
``selectfg``, ``border``, ``inputbg``, ``inputfg``, ``active``):

.. code-block:: python

   import ttkbootstrap as ttk

   app = ttk.App()
   c = app.style.colors

   canvas = ttk.Canvas(app, width=200, height=80, highlightthickness=0)
   canvas.create_rectangle(10, 10, 190, 70, fill=c.success, outline=c.border)
   canvas.pack()

   app.mainloop()

Each value is an ordinary hex string, so it drops into any tkinter color option.
``c.get(name)`` looks a color up by name and returns ``None`` if it isn't one —
handy when the name is dynamic.

Color ramps
-----------

Every color is also a **ramp**: index it with a stop from ``50`` (lightest) to
``950`` (darkest) to get a tint or shade, with the color itself as the ``500``
anchor. This is how you get an on-theme lighter or darker variant without color
math:

.. code-block:: python

   c.primary            # the theme's primary accent (also c.primary[500])
   c.primary[300]       # a lighter tint
   c.primary[700]       # a darker shade
   c.ramp("primary")    # the whole 50–950 ramp as a mapping

Because a ramp color is just a string, ``c.primary`` still behaves exactly like
its hex value everywhere else.

Deriving colors
---------------

For adjustments the ramp doesn't cover, the color utilities are exported at the
top level:

.. code-block:: python

   from ttkbootstrap import contrast_color, update_hsl_value, color_to_rgb

   contrast_color(c.primary, model="hex")          # "#000"/"#fff" — readable text over a fill
   update_hsl_value(c.primary, lum=70, inmodel="hex", outmodel="hex")  # lighten
   color_to_rgb(c.primary, "hex")                  # the primary as an (r, g, b) tuple

To simulate a translucent fill over a known background, blend it with
``make_transparent``:

.. code-block:: python

   c.make_transparent(0.2, c.primary, c.bg)   # 20% primary over the window bg

.. admonition:: Coming from 1.x
   :class: note

   The color helpers moved to ``ttkbootstrap.utils`` (and the top level). The old
   ``ttkbootstrap.colorutils`` import still works but warns and is removed in 3.0.
