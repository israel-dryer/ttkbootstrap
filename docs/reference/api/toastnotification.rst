ToastNotification
=================

``ToastNotification`` is a helper that ttkbootstrap ships
(``ttk.ToastNotification``) — a small, semi-transparent popup for temporary
alerts. It is **not a widget**: you construct it, then call
:py:meth:`show_toast` to display it. A toast either closes itself after
``duration`` milliseconds or waits to be clicked. Concurrent toasts anchored to
the same corner stack without overlapping. For screenshots and worked examples,
see the :doc:`ToastNotification catalog page </widgets/toast>`; this page is the
complete lookup reference.

Options
-------

All options are passed to the constructor.

.. list-table::
   :header-rows: 1
   :widths: 20 18 62

   * - Option
     - Type
     - Description
   * - ``title``
     - ``str``
     - The bold heading line of the toast.
   * - ``message``
     - ``str``
     - The body text of the toast.
   * - ``bootstyle``
     - ``str``
     - The color of the toast — one of ``primary``, ``secondary``, ``success``,
       ``info``, ``warning``, ``danger``, ``light``, ``dark``. Default
       ``"light"``.
   * - ``duration``
     - ``int``
     - Milliseconds to keep the toast visible. Default ``None`` (stays until
       clicked).
   * - ``alert``
     - ``bool``
     - Whether to ring the display bell when the toast appears. Default
       ``False``.
   * - ``icon``
     - ``str``
     - A Bootstrap-Icons glyph name (e.g. ``"bell-fill"``,
       ``"info-circle-fill"``) shown in the corner. Default ``None`` (a bell);
       pass ``""`` to remove it.
   * - ``position``
     - ``tuple``
     - An ``(x, y, anchor)`` tuple placing the toast — ``anchor`` is one of
       ``n``, ``e``, ``s``, ``w``, ``nw``, ``ne``, ``sw``, ``se``, and ``x``/``y``
       offset from it. Default ``None`` (OS-specific corner).

Methods
-------

.. py:method:: show_toast()
   :noindex:

   Create, position, and display the toast.

   :returns: the toast itself, usable as a dismiss handle.

.. py:method:: hide_toast()
   :noindex:

   Dismiss the toast immediately.

   :returns: ``None``.

See also
--------

- :doc:`ToastNotification catalog page </widgets/toast>` — usage, screenshots,
  and examples.