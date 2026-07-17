Meter
=====

A **meter** shows an amount as a radial dial — a percentage used, a score, a
live reading. ``Meter`` is a ttkbootstrap widget (a real class with its own API,
imported as ``ttk.Meter``). This page covers showing and updating a value, the
full/semicircle shapes, the interactive dial, the striped look, then the
``bootstyle`` color.

.. image:: /_static/examples/meter-hero-light.png
   :class: tb-screenshot-light
   :width: 228px
   :alt: A meter reading 65 with a "storage used" subtext — light theme

.. image:: /_static/examples/meter-hero-dark.png
   :class: tb-screenshot-dark
   :width: 228px
   :alt: A meter reading 65 with a "storage used" subtext — dark theme

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

.. image:: /_static/examples/meter-types-light.png
   :class: tb-screenshot-light
   :width: 400px
   :alt: The same value as a full-circle ring and a semicircle gauge — light theme

.. image:: /_static/examples/meter-types-dark.png
   :class: tb-screenshot-dark
   :width: 400px
   :alt: The same value as a full-circle ring and a semicircle gauge — dark theme

An interactive dial
-------------------

Pass ``interactive=True`` to let the user **drag the arc** to set the value — the
meter becomes an input, not just a readout:

.. code-block:: python

   dial = Meter(app, amount_used=30, interactive=True, subtext="volume")
   dial.pack()

   dial.amount_used_var.get()           # read what the user set

.. image:: /_static/examples/meter-interactive-light.png
   :class: tb-screenshot-light
   :width: 228px
   :alt: An interactive volume dial reading 30 — light theme

.. image:: /_static/examples/meter-interactive-dark.png
   :class: tb-screenshot-dark
   :width: 228px
   :alt: An interactive volume dial reading 30 — dark theme

Striped
-------

``stripe_thickness`` breaks the arc into segments of that width, for a chunkier
progress look:

.. code-block:: python

   Meter(app, amount_used=65, stripe_thickness=10, bootstyle="info")

``wedge_size`` instead draws the indicator as a moving wedge over the base ring,
rather than a filled arc — a pointer look for a live reading.

.. image:: /_static/examples/meter-striped-light.png
   :class: tb-screenshot-light
   :width: 400px
   :alt: A striped meter beside a solid one — light theme

.. image:: /_static/examples/meter-striped-dark.png
   :class: tb-screenshot-dark
   :width: 400px
   :alt: A striped meter beside a solid one — dark theme

Color
-----

``bootstyle`` colors the indicator arc from the semantic palette:

.. code-block:: python

   Meter(app, amount_used=50, bootstyle="warning")

.. image:: /_static/examples/meter-colors-light.png
   :class: tb-screenshot-light
   :width: 668px
   :alt: A row of meters in primary, success, info, warning, and danger — light theme

.. image:: /_static/examples/meter-colors-dark.png
   :class: tb-screenshot-dark
   :width: 668px
   :alt: A row of meters in primary, success, info, warning, and danger — dark theme

Reference
---------

- :doc:`Meter API reference </reference/api/meter>` — every option and method.

.. seealso::

   - :doc:`Floodgauge <floodgauge>` — a linear progress indicator with a value.
   - :doc:`Progressbar <progressbar>` — a plain progress bar.
