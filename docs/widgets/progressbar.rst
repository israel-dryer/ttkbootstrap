Progressbar
===========

A **progressbar** shows how far along a task is — either a known fraction
(*determinate*) or just that work is happening (*indeterminate*). ``Progressbar``
is the native ``ttk.Progressbar``, styled with ``bootstyle=``. This page covers
both modes, driving the value, the striped and vertical looks, then the
``bootstyle`` color.

.. image:: /_static/examples/progressbar-hero-light.png
   :class: tb-screenshot-light
   :width: 316px
   :alt: A determinate bar partway across and an indeterminate bar — light theme

.. image:: /_static/examples/progressbar-hero-dark.png
   :class: tb-screenshot-dark
   :width: 316px
   :alt: A determinate bar partway across and an indeterminate bar — dark theme

Determinate: a known amount
---------------------------

The default mode. ``maximum`` is the full value and ``value`` is the current
progress; bind ``variable=`` to drive it from your code as the work advances:

.. code-block:: python

   import ttkbootstrap as ttk

   app = ttk.App()

   progress = ttk.IntVar(value=0)
   ttk.Progressbar(app, variable=progress, maximum=100, bootstyle="success").pack(fill="x", padx=10, pady=10)

   progress.set(65)                  # jump to 65%

   app.mainloop()

``bar.step(amount)`` advances the value by ``amount`` (default ``1.0``) without a
variable — handy in a loop that processes items. If you set both ``variable=`` and
``value=``, the variable wins and ``value`` is ignored.

Indeterminate: work is happening
--------------------------------

When you can't measure progress, use ``mode="indeterminate"`` — a block bounces
back and forth. ``start()`` begins the animation and ``stop()`` ends it:

.. code-block:: python

   spinner = ttk.Progressbar(app, mode="indeterminate", bootstyle="info")
   spinner.pack(fill="x", padx=10)

   spinner.start()                   # animate while a task runs…
   spinner.stop()                    # …then stop

``start(interval)`` steps every ``interval`` milliseconds (default 50). In
indeterminate mode the value wraps around ``maximum``, so ``maximum`` sets the
length of one bounce cycle — raise it to slow the sweep.

Striped and vertical
--------------------

A ``striped`` variant gives the bar a segmented arc; ``orient="vertical"`` stands
it up (drive its height with the same ``value``):

.. code-block:: python

   ttk.Progressbar(app, value=60, maximum=100, bootstyle="success striped")
   ttk.Progressbar(app, value=60, maximum=100, orient="vertical")

Color
-----

``bootstyle`` colors the bar from the semantic palette:

.. code-block:: python

   ttk.Progressbar(app, value=50, bootstyle="warning")

Reference
---------

``Progressbar`` is the native ``ttk.Progressbar``; ttkbootstrap adds only the
``bootstyle`` keyword.

- :doc:`Progressbar API reference </reference/api/progressbar>` — every option and
  method.
- :ref:`Progressbar styling options <progressbar-styling>` — restyle it yourself,
  with the :doc:`Custom styles </user-guide/feature-guides/custom-styles>` guide.

.. seealso::

   - :doc:`Floodgauge <floodgauge>` — a progress bar that shows its value as text.
   - :doc:`Meter <meter>` — a radial progress indicator.
