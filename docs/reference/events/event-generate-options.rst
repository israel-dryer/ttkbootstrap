event_generate options
=======================

``widget.event_generate(sequence, **options)`` synthesizes an event and
dispatches it to ``widget``. The options fill in the fields the event would
normally carry; each mirrors a Tk ``-option`` with the **leading dash dropped**
(Tk ``-rootx`` → ``rootx=``). See
:doc:`Events & callbacks </user-guide/foundations/events-and-callbacks>` for how
to use it.

.. code-block:: python

   widget.event_generate("<Button-1>", x=10, y=20, when="now")
   widget.event_generate("<<DataLoaded>>")

Options
-------

.. list-table::
   :header-rows: 1
   :widths: 20 34 46

   * - Keyword
     - Applies to
     - Sets
   * - ``x``, ``y``
     - pointer & key events
     - Position relative to the target widget.
   * - ``rootx``, ``rooty``
     - pointer & key events
     - Position relative to the screen.
   * - ``button``
     - Button events
     - The button number.
   * - ``keysym``
     - key events
     - The :doc:`key symbol <modifiers-and-keys>` (overrides the detail).
   * - ``keycode``
     - key events
     - The hardware key code.
   * - ``delta``
     - MouseWheel
     - The wheel rotation amount.
   * - ``state``
     - pointer, key events
     - The modifier/button bitmask.
   * - ``width``, ``height``
     - Configure
     - The reported size.
   * - ``warp``
     - pointer & key events
     - If true, actually move the mouse pointer to the given position.
   * - ``data``
     - virtual events
     - User data. Accepted, but **not** readable on tkinter's event object —
       see :doc:`The event object <event-object>`.
   * - ``when``
     - all
     - When the event is processed (see below).

``when``
--------

.. list-table::
   :header-rows: 1
   :widths: 16 84

   * - Value
     - Effect
   * - ``now``
     - Process immediately, before ``event_generate`` returns (the default).
   * - ``tail``
     - Queue behind the events already waiting.
   * - ``head``
     - Queue ahead of all waiting events.
   * - ``mark``
     - Queue ahead of normal events but behind earlier ``mark`` events —
       preserves order across a burst of generated events.

.. note::

   The full Tk option set (``-above``, ``-borderwidth``, ``-count``,
   ``-detail``, ``-focus``, ``-mode``, ``-override``, ``-place``, ``-root``,
   ``-sendevent``, ``-serial``, ``-subwindow``, ``-time``) is also accepted with
   the dash dropped, for filling in fields of the more specialized event types.
