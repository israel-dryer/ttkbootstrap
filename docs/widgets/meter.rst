Meter
=====

A **meter** shows an amount as a radial dial — a percentage used, a score, a
live reading. ``Meter`` is a ttkbootstrap widget (a real class with its own API,
imported as ``ttk.Meter``). This page covers showing and updating a value, the
full/semicircle shapes, the interactive dial, the striped look, then the
``bootstyle`` color.

.. admonition:: 📷 Screenshot (placeholder)
   :class: screenshot-placeholder

   A meter reading 65% with a "storage used" subtext, in light and dark themes.

Usage
-----

``amount_used`` is the current value and ``amount_total`` the maximum (default
100); ``subtext`` labels it:

.. code-block:: python

   import ttkbootstrap as ttk
   from ttkbootstrap.widgets import Meter

   app = ttk.App()

   meter = Meter(app, amount_used=65, amount_total=100, subtext="storage used",
                 bootstyle="success")
   meter.pack(padx=16, pady=16)

   app.mainloop()

Read and change the value through ``amount_used_var`` (a variable that tracks the
dial), or with ``configure``; ``step`` nudges it by an amount:

.. code-block:: python

   meter.amount_used_var.get()          # -> the current value
   meter.value                           # -> the same, via the read/write property
   meter.configure(amount_used=80)      # set it
   meter.step(5)                        # advance by 5 (bounces at the ends)

``step`` **bounces** back when it reaches the minimum or maximum, reversing
direction rather than clamping — it's for a looping animation, not a plain
increment.

The center label
----------------

The big number is formatted by ``amount_format`` (a ``str.format`` template,
default ``"{:.0f}"``), and ``text_left`` / ``text_right`` flank it with a unit — a
``$`` prefix or a ``%`` suffix. ``amount_min`` shifts where the range starts, for a
dial that runs from something other than zero:

.. code-block:: python

   Meter(app, amount_used=42, amount_format="{:.1f}", text_right="%",
         amount_min=0, subtext="CPU")

Full or semicircle
------------------

``meter_type`` is ``"full"`` (the default, a complete ring) or ``"semi"`` (a
half-circle gauge):

.. code-block:: python

   Meter(app, amount_used=65, meter_type="semi")

.. admonition:: 📷 Screenshot (placeholder)
   :class: screenshot-placeholder

   The same value as a full-circle ring and a semicircle gauge, side by side.

An interactive dial
-------------------

Pass ``interactive=True`` to let the user **drag the arc** to set the value — the
meter becomes an input, not just a readout:

.. code-block:: python

   dial = Meter(app, amount_used=30, interactive=True, subtext="volume")
   dial.pack()

   dial.amount_used_var.get()           # read what the user set

.. admonition:: 📷 Screenshot (placeholder)
   :class: screenshot-placeholder

   An interactive meter with the handle mid-arc, being dragged to a new value.

Striped
-------

``stripe_thickness`` breaks the arc into segments of that width, for a chunkier
progress look:

.. code-block:: python

   Meter(app, amount_used=65, stripe_thickness=10, bootstyle="info")

``wedge_size`` instead draws the indicator as a moving wedge over the base ring,
rather than a filled arc — a pointer look for a live reading.

.. admonition:: 📷 Screenshot (placeholder)
   :class: screenshot-placeholder

   A meter whose indicator arc is broken into segments, beside a solid one.

Color
-----

``bootstyle`` colors the indicator arc from the semantic palette:

.. code-block:: python

   Meter(app, amount_used=50, bootstyle="warning")

.. admonition:: 📷 Screenshot (placeholder)
   :class: screenshot-placeholder

   A row of meters in primary, success, info, warning, and danger, in light and
   dark themes.

API & reference
---------------

For the complete option list and methods, see the
:doc:`Meter API reference </reference/api/meter>`.

.. seealso::

   :doc:`Floodgauge <floodgauge>` for a linear progress indicator with a value,
   and :doc:`Progressbar <progressbar>` for a plain bar.
