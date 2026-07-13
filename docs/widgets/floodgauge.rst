Floodgauge
==========

A **floodgauge** is a progress bar that shows its value *as text across the bar* —
a percentage, a count, a status word. ``Floodgauge`` is a ttkbootstrap widget (a
real class with its own API, imported as ``ttk.Floodgauge``). This page covers
driving the value and its label, the indeterminate mode, the orientation, then the
``bootstyle`` color.

.. admonition:: 📷 Screenshot (placeholder)
   :class: screenshot-placeholder

   A floodgauge filled to 75% with "75% complete" shown across it, in light and
   dark themes.

Usage
-----

``value`` and ``maximum`` set the fill, and ``mask`` formats the value into the
label — a ``str.format`` template where ``{}`` is the current value. Bind a
variable to drive it as work advances:

.. code-block:: python

   import ttkbootstrap as ttk
   from ttkbootstrap.widgets import Floodgauge

   app = ttk.App()

   progress = ttk.IntVar(value=0)
   gauge = Floodgauge(app, variable=progress, maximum=100, mask="{}% complete",
                      bootstyle="info")
   gauge.pack(fill="x", padx=10, pady=10)

   progress.set(75)                     # the bar fills and the label updates

   app.mainloop()

For a fixed caption instead of the value, pass ``text`` instead of ``mask``.

Indeterminate mode
------------------

When you can't measure progress, set ``mode="indeterminate"`` and animate it with
``start()`` / ``stop()`` (``step`` advances it manually):

.. code-block:: python

   gauge = Floodgauge(app, mode="indeterminate", text="Working…", bootstyle="info")
   gauge.pack(fill="x")

   gauge.start()                        # animate while a task runs…
   gauge.stop()                         # …then stop

Orientation
-----------

``orient="vertical"`` stands the gauge up (the default is ``"horizontal"``):

.. code-block:: python

   Floodgauge(app, value=60, maximum=100, orient="vertical", mask="{}%")

Color
-----

``bootstyle`` colors the bar and its text from the semantic palette:

.. code-block:: python

   Floodgauge(app, value=50, maximum=100, mask="{}%", bootstyle="success")

API & reference
---------------

For the complete option list and methods, see the
:doc:`Floodgauge API reference </reference/api/floodgauge>`.

.. seealso::

   :doc:`Progressbar <progressbar>` for a plain bar without the value label, and
   :doc:`Meter <meter>` for a radial indicator.
