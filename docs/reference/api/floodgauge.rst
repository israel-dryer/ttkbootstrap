Floodgauge
==========

``Floodgauge`` is a progress-bar variant that ttkbootstrap ships
(``ttk.Floodgauge``) — a filling bar with text drawn over it, useful for
showing progress with an inline label or percentage. It supports the same
``determinate`` and ``indeterminate`` modes as a progress bar. For screenshots
and worked examples, see the :doc:`Floodgauge catalog page </widgets/floodgauge>`;
this page is the complete lookup reference.

Each option can be passed to the constructor and changed later with
``configure()``.

Options
-------

.. list-table::
   :header-rows: 1
   :widths: 20 18 62

   * - Option
     - Type
     - Description
   * - ``bootstyle``
     - ``str``
     - The color of the bar and text — one of ``primary``, ``secondary``,
       ``success``, ``info``, ``warning``, ``danger``, ``light``, ``dark``.
       Default ``"primary"``.
   * - ``value``
     - ``int | float``
     - The current progress value. Default ``0``.
   * - ``maximum``
     - ``int | float``
     - The value at which the bar is full. Default ``100``.
   * - ``mode``
     - ``str``
     - ``"determinate"`` (the bar fills to ``value``) or ``"indeterminate"``
       (a block bounces back and forth). Default ``"determinate"``.
   * - ``text``
     - ``str``
     - Static text drawn over the bar. Default ``""``.
   * - ``mask``
     - ``str``
     - A template that overrides ``text`` and shows the live value, e.g.
       ``"{}% Complete"`` — the ``{}`` is replaced with the current ``value``.
   * - ``font``
     - ``str | tuple``
     - The font of the overlaid text. Default ``("Helvetica", 12)``.
   * - ``orient``
     - ``str``
     - ``"horizontal"`` or ``"vertical"``. Default ``"horizontal"``.
   * - ``length``
     - ``int``
     - The long dimension of the gauge in pixels. Default ``200``.
   * - ``thickness``
     - ``int``
     - The short dimension of the gauge in pixels. Default ``50``.

Methods
-------

.. py:method:: start(interval=None)
   :noindex:

   Begin the animation — a bouncing block in indeterminate mode, or an
   auto-increment in determinate mode.

   :param interval: milliseconds between steps (defaults to 20 ms
      indeterminate, 50 ms determinate).
   :returns: ``None``.

.. py:method:: stop()
   :noindex:

   Stop the animation started by :py:meth:`start`.

   :returns: ``None``.

.. py:method:: step(amount=1)
   :noindex:

   Increment the value by ``amount``, wrapping back to the minimum after
   passing ``maximum``.

   :param amount: the amount to add (default ``1``).
   :returns: ``None``.

.. py:attribute:: value
   :noindex:

   The current progress value (property; equivalent to ``cget("value")``). Set
   it with ``configure(value=...)``.

Shared capabilities
-------------------

``Floodgauge`` also has the methods every widget inherits — configuration,
placement, event binding, lifecycle, focus, and introspection. These are
documented under :doc:`Capabilities </reference/capabilities/index>`.

See also
--------

- :doc:`Floodgauge catalog page </widgets/floodgauge>` — usage, screenshots,
  and examples.
- :doc:`Progressbar </widgets/progressbar>` — the native ttk progress bar.