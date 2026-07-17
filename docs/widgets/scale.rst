Scale
=====

A **scale** is a slider for choosing a number from a continuous range by dragging
a handle. ``Scale`` is the native ``ttk.Scale``, styled with ``bootstyle=``. This
page covers binding its value, reacting as it moves, the orientation, then the
``bootstyle`` color.

.. image:: /_static/examples/scale-hero-light.png
   :class: tb-screenshot-light
   :width: 276px
   :alt: A horizontal scale partway along its track — light theme

.. image:: /_static/examples/scale-hero-dark.png
   :class: tb-screenshot-dark
   :width: 276px
   :alt: A horizontal scale partway along its track — dark theme

Usage
-----

Set the range with ``from_`` and ``to``, and bind the value to a variable — a
``DoubleVar`` (the scale's value is a float) or an ``IntVar``:

.. code-block:: python

   import ttkbootstrap as ttk

   app = ttk.App()

   volume = ttk.DoubleVar(value=30)
   ttk.Scale(app, from_=0, to=100, variable=volume).pack(fill="x", padx=10, pady=10)

   ttk.Button(app, text="Apply", command=lambda: print(volume.get()), bootstyle="primary").pack()

   app.mainloop()

Read the value with the variable's ``.get()`` (or the scale's own ``.get()``).
Like a :doc:`Spinbox <spinbox>`, ``from_`` has a trailing underscore because
``from`` is a Python keyword.

.. note::

   A scale's value is a **float**, even over an integer-looking range. Round it
   (``round(volume.get())``) or bind an ``IntVar`` if you need a whole number.

Setting the value from code
---------------------------

``scale.set(value)`` moves the handle and **clips** to the ``from_``/``to`` range.
Setting the bound variable directly does **not** clip — the handle can then show a
value past the ends — so prefer ``.set()`` (or clamp the value yourself) when the
source might be out of bounds:

.. code-block:: python

   scale.set(150)          # clipped to `to` (100)
   volume.set(150)         # NOT clipped — the handle overshoots the track

Unlike ``tk.Scale``, ``ttk.Scale`` has no ``resolution``, ``tickinterval``,
``showvalue``, or ``label`` options — use ``round()`` / an ``IntVar`` for stepping
and the ``LabeledScale`` widget for a value readout. ``scale.coords(value)``
returns the pixel position of a value along the trough (and ``scale.get(x, y)``
maps a pixel back to a value) — how ``LabeledScale`` parks its label over the
handle.

Reacting as it moves
--------------------

``command=`` runs continuously while the user drags — for a live preview. It
receives the new value (a string) as its argument:

.. code-block:: python

   def on_slide(value):
       print("volume", round(float(value)))

   ttk.Scale(app, from_=0, to=100, variable=volume, command=on_slide)

Orientation
-----------

``orient="vertical"`` stands the scale up (the default is ``"horizontal"``):

.. code-block:: python

   ttk.Scale(app, from_=100, to=0, orient="vertical", variable=volume)

Color
-----

``bootstyle`` colors the handle and the filled part of the track from the semantic
palette:

.. code-block:: python

   ttk.Scale(app, from_=0, to=100, variable=volume, bootstyle="info")

Reference
---------

``Scale`` is the native ``ttk.Scale``; ttkbootstrap adds only the ``bootstyle``
keyword.

- :doc:`Scale API reference </reference/api/scale>` — every option and method.
- :ref:`Scale styling options <scale-styling>` — restyle it yourself, with the
  :doc:`Custom styles </user-guide/feature-guides/custom-styles>` guide.

.. seealso::

   - :doc:`LabeledScale <labeledscale>` — a scale with a value label on the handle.
   - :doc:`Spinbox <spinbox>` — a stepped numeric entry.
