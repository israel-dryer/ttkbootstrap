Meter
=====

``Meter`` is a radial progress/dial widget that ttkbootstrap ships
(``ttk.Meter``). It shows a value as an arc — a full circle or a semicircle —
with a formatted center label, optional side and sub labels, and an optional
interactive mode that lets the user drag the value like a dial. This page is the complete lookup reference.

Every option below can be set in the constructor and changed at runtime with
``configure()`` (and read back with ``cget()``).

Options
-------

Each option can be passed to the constructor and changed later with
``configure()``.

.. list-table::
   :header-rows: 1
   :widths: 20 18 62

   * - Option
     - Type
     - Description
   * - ``bootstyle``
     - ``str``
     - The color of the indicator and center text — one of ``primary``,
       ``secondary``, ``success``, ``info``, ``warning``, ``danger``, ``light``,
       ``dark``. Default ``"default"``.
   * - ``amount_used``
     - ``int | float``
     - The current value, shown in the center label when ``show_text`` is true.
       Default ``0``.
   * - ``amount_min``
     - ``int | float``
     - The minimum of the range; may be negative. Default ``0``.
   * - ``amount_total``
     - ``int | float``
     - The maximum of the range. Default ``100``.
   * - ``amount_format``
     - ``str``
     - The format string for the center value. Fractional formats such as
       ``"{:.1f}"`` are honored — the value is stored as a float. Default
       ``"{:.0f}"``.
   * - ``step_size``
     - ``int | float``
     - How much :py:meth:`step` and interactive dragging change the value.
       Default ``1``.
   * - ``meter_type``
     - ``str``
     - ``"full"`` for a full circle or ``"semi"`` for a semicircle. Default
       ``"full"``.
   * - ``arc_range``
     - ``int``
     - The arc's sweep in degrees. Left unset, it follows ``meter_type``.
   * - ``arc_offset``
     - ``int``
     - The offset of the arc's starting position in degrees; ``0`` is at
       3 o'clock. Left unset, it follows ``meter_type``.
   * - ``meter_size``
     - ``int``
     - The logical side length of the (square) meter in screen units, scaled for
       high-DPI. Default ``200``.
   * - ``meter_thickness``
     - ``int``
     - The thickness of the indicator band. Default ``10``.
   * - ``wedge_size``
     - ``int``
     - If greater than ``0``, draws a fixed-length wedge centered on the current
       value instead of filling the arc up to it. Default ``0``.
   * - ``stripe_thickness``
     - ``int``
     - If greater than ``0``, renders the indicator as striped wedges of this
       thickness rather than a solid band. Default ``0``.
   * - ``show_text``
     - ``bool``
     - Whether to show the left, center, and right text labels. Default
       ``True``.
   * - ``text_left``
     - ``str``
     - A short string placed to the left of the center value (commonly ``"$"``).
   * - ``text_right``
     - ``str``
     - A short string placed to the right of the center value (commonly
       ``"%"``).
   * - ``text_font``
     - ``str | Font``
     - The font for the center value. Default ``"-size 20 -weight bold"``.
   * - ``subtext``
     - ``str``
     - Supplemental text shown below the center value.
   * - ``subtext_style``
     - ``str``
     - The ``bootstyle`` color of the subtext. Default is a theme-specific
       lighter shade.
   * - ``subtext_font``
     - ``str | Font``
     - The font for the subtext. Default ``"-size 10"``.
   * - ``interactive``
     - ``bool``
     - Whether the user can adjust the value by clicking and dragging the meter.
       Default ``False``.

The meter is a ``Frame`` subclass, so it also accepts the frame's own options —
``padding``, ``borderwidth``, ``relief``, ``width``, ``height``, ``cursor``,
``takefocus`` — applied to the surrounding container.

Methods
-------

.. py:method:: step(delta=1)
   :noindex:

   Increment (or decrement) the value by ``delta`` steps. The indicator bounces
   back at the minimum and maximum, reversing direction automatically.

   :param delta: the number of steps; positive increases, negative decreases.
   :returns: ``None``.

.. py:attribute:: value
   :noindex:

   The current meter value (read-only property; equivalent to
   ``cget("amount_used")``). To set it, use ``configure(amount_used=...)`` or
   the bound variable ``amount_used_var`` — a ``Variable`` you can share with
   other widgets to keep them in sync with the meter.

Shared capabilities
-------------------

``Meter`` also has the methods every widget inherits — configuration,
placement, event binding, lifecycle, focus, and introspection. These are
documented under :doc:`Capabilities </reference/capabilities/index>`.

See also
--------

- :doc:`Meter catalog page </widgets/meter>` — usage, screenshots, and examples.