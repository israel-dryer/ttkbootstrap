DateEntry
=========

``DateEntry`` is a composite widget that ttkbootstrap ships (``ttk.DateEntry``)
— an :doc:`Entry </widgets/entry>` paired with a button that opens a calendar
popup for picking a date. The chosen date is written back into the entry, and a
``<<DateEntrySelected>>`` virtual event fires. This page
is the complete lookup reference.

Each option can be passed to the constructor and changed later with
``configure()``.

Options
-------

.. list-table::
   :header-rows: 1
   :widths: 22 18 60

   * - Option
     - Type
     - Description
   * - ``bootstyle``
     - ``str``
     - The focus color of the entry and the color of the date button — one of
       ``primary``, ``secondary``, ``success``, ``info``, ``warning``,
       ``danger``, ``light``, ``dark``. Default ``"primary"``.
   * - ``date_format``
     - ``str``
     - The ``strftime`` format used to render the date in the entry. Default
       ``"%x"`` (the locale's date representation).
   * - ``first_weekday``
     - ``int``
     - The first day of the week in the popup: ``0`` = Monday … ``6`` = Sunday.
       Default ``6``.
   * - ``start_date``
     - ``datetime | date``
     - The date focused when the popup first opens. Default ``None`` (today).
   * - ``button_icon``
     - ``str``
     - The Bootstrap-Icons glyph shown on the button. Default
       ``"calendar-week"``.
   * - ``show_outside_days``
     - ``bool``
     - Whether the popup shows the leading/trailing days of adjacent months as
       muted, non-selectable labels. Default ``True``.
   * - ``raise_exception``
     - ``bool``
     - Whether an invalid typed date raises ``ValueError``. When ``False``, a
       bad string is ignored with a warning. Default ``False``.
   * - ``position``
     - ``tuple``
     - Optional ``(x, y)`` screen coordinates for the popup. Default ``None``
       (positioned near the widget).
   * - ``popup_title``
     - ``str``
     - Retained for API compatibility; not displayed, because the popup is
       borderless. Default ``"Select new date"``.

A ``width`` passed via ``**kwargs`` is applied to the entry field, not the
container frame.

Methods
-------

.. py:method:: get_date()
   :noindex:

   Return the currently selected date.

   :returns: the selected date, or ``None`` if the entry is empty / invalid.
   :rtype: datetime | None

.. py:method:: set_date(new_date)
   :noindex:

   Set the selected date and update the entry text.

   :param new_date: the date to display.
   :type new_date: datetime | date
   :returns: ``None``.

.. py:method:: enable()
   :noindex:

   Enable the entry and date button.

   :returns: ``None``.

.. py:method:: disable()
   :noindex:

   Disable the entry and date button.

   :returns: ``None``.

.. py:attribute:: value
   :noindex:

   The currently selected date (property; a synonym for :py:meth:`get_date`).

.. py:attribute:: enabled
   :noindex:

   Whether the date picker is currently enabled (read-only property).

Shared capabilities
-------------------

``DateEntry`` also has the methods every widget inherits — configuration,
placement, event binding, lifecycle, focus, and introspection. These are
documented under :doc:`Capabilities </reference/capabilities/index>`.

See also
--------

- :doc:`DateEntry catalog page </widgets/dateentry>` — usage, screenshots, and
  examples.
- :doc:`Entry </widgets/entry>` — the native ttk entry.