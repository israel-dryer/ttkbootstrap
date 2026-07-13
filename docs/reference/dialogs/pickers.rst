Pickers
=======

These are the dialog classes behind :py:meth:`Querybox.get_date`,
:py:meth:`Querybox.get_color`, and :py:meth:`Querybox.get_font`. ``Querybox``
constructs them for you and hands back the result, but you can construct any of
them directly when you want more control over placement, styling, or lifecycle.

DatePickerDialog
----------------

A calendar popup for choosing a date. It opens near the parent widget, lets the
user page through months, and returns the selected day.

Options
~~~~~~~

Set these on the constructor —
``DatePickerDialog(parent=None, title=" ", first_weekday=6, start_date=None, bootstyle="primary", autoshow=True, show_outside_days=True)``.

.. list-table::
   :header-rows: 1
   :widths: 22 16 62

   * - Option
     - Type
     - Description
   * - ``parent``
     - ``Widget``
     - The window to position near and block. Defaults to the application root.
   * - ``title``
     - ``str``
     - The text shown on the window's title bar.
   * - ``first_weekday``
     - ``int``
     - The leftmost weekday column, ``0`` (Monday)–``6`` (Sunday). Default ``6``.
   * - ``start_date``
     - ``date``
     - The date shown selected initially. Defaults to today.
   * - ``bootstyle``
     - ``str``
     - The calendar's accent color. Default ``"primary"``.
   * - ``autoshow``
     - ``bool``
     - Display immediately on construction. Default ``True``; pass ``False`` to
       call :py:meth:`show` yourself.
   * - ``show_outside_days``
     - ``bool``
     - Show days spilling in from the adjacent months. Default ``True``.

Methods
~~~~~~~

.. py:method:: show(position=None, wait_for_result=True)
   :noindex:

   Display the dialog. Blocks until the user picks a date or cancels, then
   stores the outcome on :py:attr:`result`.

   :param position: An ``(x, y)`` top-left screen position. Positioned near
      ``parent`` by default.
   :param wait_for_result: Block until the dialog closes. Default ``True``.
   :returns: ``None`` — read :py:attr:`result` after it returns.

.. py:attribute:: result
   :noindex:

   The chosen ``datetime.date``, or ``None`` if cancelled.

FontDialog
----------

A font selector for choosing a family, size, weight, slant, and effects, with a
live preview of the current selection.

Options
~~~~~~~

Set these on the constructor —
``FontDialog(title="Font Selector", parent=None, default_font="TkDefaultFont")``.

.. list-table::
   :header-rows: 1
   :widths: 22 16 62

   * - Option
     - Type
     - Description
   * - ``title``
     - ``str``
     - The text shown on the window's title bar. Default ``"Font Selector"``.
   * - ``parent``
     - ``Widget``
     - The window to center over and block. Defaults to the application root.
   * - ``default_font``
     - ``str``
     - The named font shown selected initially. Default ``"TkDefaultFont"``.

Methods
~~~~~~~

.. py:method:: show(position=None, wait_for_result=True)
   :noindex:

   Display the dialog. Blocks until the user picks a font or cancels, then
   stores the outcome on :py:attr:`result`.

   :param position: An ``(x, y)`` top-left screen position. Centered on
      ``parent`` by default.
   :param wait_for_result: Block until the dialog closes. Default ``True``.
   :returns: ``None`` — read :py:attr:`result` after it returns.

.. py:attribute:: result
   :noindex:

   The chosen ``Font``, or ``None`` if cancelled.

ColorChooserDialog
------------------

A color picker with color-model sliders and a preview. The user can adjust the
sliders, enter a value, or reach the eyedropper (:py:class:`ColorDropperDialog`)
to sample a color from the screen.

Options
~~~~~~~

Set these on the constructor —
``ColorChooserDialog(parent=None, title="Color Chooser", initialcolor=None)``.

.. list-table::
   :header-rows: 1
   :widths: 22 16 62

   * - Option
     - Type
     - Description
   * - ``parent``
     - ``Widget``
     - The window to center over and block. Defaults to the application root.
   * - ``title``
     - ``str``
     - The text shown on the window's title bar. Default ``"Color Chooser"``.
   * - ``initialcolor``
     - ``str``
     - The color selected initially, a hex string like ``"#2b8cee"``.

Methods
~~~~~~~

.. py:method:: show(position=None, wait_for_result=True)
   :noindex:

   Display the dialog. Blocks until the user picks a color or cancels, then
   stores the outcome on :py:attr:`result`.

   :param position: An ``(x, y)`` top-left screen position. Centered on
      ``parent`` by default.
   :param wait_for_result: Block until the dialog closes. Default ``True``.
   :returns: ``None`` — read :py:attr:`result` after it returns.

.. py:attribute:: result
   :noindex:

   The chosen color, or ``None`` if cancelled.

ColorDropperDialog
------------------

An eyedropper that picks the color of any pixel on screen — the same dropper
reachable from :py:class:`ColorChooserDialog`. It takes over the screen so the
next click samples the color under the cursor.

Methods
~~~~~~~

The constructor takes no arguments — ``ColorDropperDialog()``.

.. py:method:: show()
   :noindex:

   Take over the screen; the next click picks the color under the cursor. A
   right-click or ``Escape`` cancels. The outcome is stored on
   :py:attr:`result`.

   :returns: ``None`` — read :py:attr:`result` after it returns.

.. py:attribute:: result
   :noindex:

   The picked color, or ``None`` if cancelled.

See also
--------

- :doc:`Querybox </reference/dialogs/querybox>` — the input-and-picker facade.
- :doc:`Dialogs </user-guide/feature-guides/dialogs>` — how to use them, with
  examples.
