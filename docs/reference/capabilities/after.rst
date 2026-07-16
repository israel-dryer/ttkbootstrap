After
=====

Tkinter is single-threaded: long work blocks the event loop and freezes the UI.
The ``after`` methods schedule callbacks to run later *on* the event loop, which
is how you defer work, poll, or animate without threads. To run genuinely
blocking work off the main thread and marshal the result back, see
:doc:`Run background work </user-guide/how-to/threads>`.

The canonical upstream reference is the Tcl
`after <https://www.tcl-lang.org/man/tcl8.6/TclCmd/after.htm>`__ manual page
(Tcl 8.6).

.. py:method:: after(ms, func=None, *args)
   :noindex:

   Schedule ``func(*args)`` to run once, after ``ms`` milliseconds, on the event
   loop.

   :param int ms: delay in milliseconds.
   :param func: the callback; if omitted, ``after`` simply sleeps ``ms``.
   :param args: positional arguments passed to ``func``.
   :returns: an id that can be passed to ``after_cancel`` (when ``func`` is
      given).
   :rtype: str

.. py:method:: after_idle(func, *args)
   :noindex:

   Schedule ``func(*args)`` to run once the event loop next becomes idle (after
   pending events are processed).

   :param func: the callback.
   :param args: positional arguments passed to ``func``.
   :returns: an id that can be passed to ``after_cancel``.
   :rtype: str

.. py:method:: after_cancel(id)
   :noindex:

   Cancel a callback previously scheduled with ``after`` or ``after_idle``.

   :param id: the id returned by the scheduling call.
   :returns: ``None``.

.. py:method:: after_info(id=None)
   :noindex:

   Report the callbacks scheduled with ``after``/``after_idle`` that have not yet
   run — useful when tracking down a timer that outlives the widget it updates.

   :param id: an optional scheduling id to ask about.
   :returns: with no argument, the ids of all pending callbacks; with an ``id``,
      that callback's ``(script, type)``, where type is ``"timer"`` or
      ``"idle"``.
   :rtype: tuple
