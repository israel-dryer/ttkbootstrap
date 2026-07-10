Meter
=====

A radial meter for showing the progress of a long-running operation or an amount
completed. It can also act as an interactive dial. ``Meter`` is a ttkbootstrap
widget — a real class with its own API.

.. Screenshots (light/dark pairs) are added in a later documentation slice.

Semantic styling
----------------

Set the indicator color with ``bootstyle=``:

.. code-block:: python

   import ttkbootstrap as ttk

   app = ttk.Window()

   meter = ttk.Meter(
       app,
       bootstyle="success",
       subtext="progress",
       amountused=65,
   )
   meter.pack(padx=16, pady=16)

   app.mainloop()

Common tasks
------------

- **Read or set the value** — the ``amountused`` option holds the current value;
  bind ``amountusedvar`` to drive it reactively.
- **Full or semicircle** — set ``metertype`` to ``"full"`` or ``"semi"``.
- **Striped indicator** — set ``stripethickness`` for a segmented arc.
- **Interactive dial** — pass ``interactive=True`` to let the user drag the arc.

API reference
-------------

For the complete option list and methods, see :class:`~ttkbootstrap.Meter` on
the :doc:`Widgets API page </reference/api/widgets>`. At a glance:

.. autosummary::
   :nosignatures:

   ~ttkbootstrap.Meter
