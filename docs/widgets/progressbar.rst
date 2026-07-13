Progressbar
===========

A **progressbar** shows how far along a task is — either a known fraction
(*determinate*) or just that work is happening (*indeterminate*). ``Progressbar``
is the native ``ttk.Progressbar``, styled with ``bootstyle=``. This page covers
both modes, driving the value, the striped and vertical looks, then the
``bootstyle`` color.

.. admonition:: 📷 Screenshot (placeholder)
   :class: screenshot-placeholder

   A determinate bar partway across and an indeterminate bar, in light and dark
   themes.

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

``bar.step(amount)`` advances the value by ``amount`` (default 1) without a
variable — handy in a loop that processes items.

Indeterminate: work is happening
--------------------------------

When you can't measure progress, use ``mode="indeterminate"`` — a block bounces
back and forth. ``start()`` begins the animation and ``stop()`` ends it:

.. code-block:: python

   spinner = ttk.Progressbar(app, mode="indeterminate", bootstyle="info")
   spinner.pack(fill="x", padx=10)

   spinner.start()                   # animate while a task runs…
   spinner.stop()                    # …then stop

``start()`` takes an optional interval in milliseconds between steps.

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

API & reference
---------------

``Progressbar`` is the native ``ttk.Progressbar`` — ttkbootstrap adds ``bootstyle=``
but no other Python API. For its constructor and options (``mode``, ``maximum``,
``value``, ``variable``, ``orient``, ``length``) and the ``start`` / ``stop`` /
``step`` methods, see the
`tkinter.ttk.Progressbar <https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Progressbar>`__
reference.

.. seealso::

   the ``Floodgauge`` widget for a progress indicator that also shows a
   value/label, and :doc:`Meter <meter>` for a radial one. Want to restyle the
   progressbar yourself? The
   :ref:`Progressbar's styling options <progressbar-styling>`
   and its companion :doc:`Custom styles </user-guide/feature-guides/custom-styles>`
   guide document the hand-styling surface.
