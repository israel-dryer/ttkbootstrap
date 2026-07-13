Scale
=====

A **scale** is a slider for choosing a number from a continuous range by dragging
a handle. ``Scale`` is the native ``ttk.Scale``, styled with ``bootstyle=``. This
page covers binding its value, reacting as it moves, the orientation, then the
``bootstyle`` color.

.. admonition:: 📷 Screenshot (placeholder)
   :class: screenshot-placeholder

   A horizontal scale partway along its track in light and dark themes.

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

API & reference
---------------

``Scale`` is the native ``ttk.Scale`` — ttkbootstrap adds ``bootstyle=`` but no
other Python API. For its constructor and options (``from_``, ``to``,
``variable``, ``command``, ``orient``, ``length``, ``value``) see the
`tkinter.ttk.Scale <https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Scale>`__
reference.

.. seealso::

   the ``LabeledScale`` widget for a scale with a value label that tracks the
   handle, and :doc:`Spinbox <spinbox>` for a stepped numeric entry. Want to
   restyle the scale yourself? The
   :ref:`Scale's styling options <scale-styling>` and its
   companion :doc:`Custom styles </user-guide/feature-guides/custom-styles>` guide
   document the hand-styling surface.
