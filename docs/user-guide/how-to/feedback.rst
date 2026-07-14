Beep and show busy
==================

Two small built-in ways to tell the user something happened: a beep for
attention, and a busy state that blocks a window while it works.

Beep with ``bell``
------------------

``bell()`` rings the system alert sound — a quick way to flag an invalid action
or a finished job. Every widget has it:

.. code-block:: python

   app.bell()

It plays the platform's default alert; there is no volume or tone control. Use it
sparingly — a beep on every keystroke gets old fast.

Mark a window busy
------------------

For a slow operation you want to both **show a wait cursor** and **stop the user
clicking** meanwhile. ``tk_busy_hold`` does both: it covers the widget with a
transparent overlay that swallows mouse and keyboard input and shows a busy
cursor, until you release it with ``tk_busy_forget``:

.. code-block:: python

   app.tk_busy_hold(cursor="watch")
   app.update_idletasks()        # paint the overlay + cursor before blocking
   do_slow_work()
   app.tk_busy_forget()

The ``update_idletasks`` call matters: without it the overlay never gets a chance
to draw before the blocking work starts, so the user sees nothing.

Always release it — even on error — by pairing the calls with ``try``/
``finally``:

.. code-block:: python

   app.tk_busy_hold(cursor="watch")
   app.update_idletasks()
   try:
       do_slow_work()
   finally:
       app.tk_busy_forget()

``tk_busy_status()`` reports whether a widget is currently held busy:

.. code-block:: python

   if app.tk_busy_status():
       ...

.. note::

   ``tk_busy_hold`` differs from simply setting ``cursor="watch"``: besides the
   cursor, it **blocks input** to the widget and everything inside it. Set
   ``cursor=`` alone (see :doc:`Cursors </reference/cursors>`) when you only want
   to change the pointer without disabling the window.

.. note::

   The method is ``tk_busy_hold`` / ``tk_busy_forget`` / ``tk_busy_configure`` /
   ``tk_busy_status`` on every supported Python. Python 3.13 adds shorter
   ``busy_hold`` / ``busy_forget`` / … aliases for the same calls.

Long work still needs a thread
------------------------------

``tk_busy`` only helps for work short enough to block on briefly — while the main
loop is blocked, the busy overlay is the *only* thing the window can do, and it
cannot repaint or animate. For genuinely long work, run it on a background thread
and marshal results back with ``after``, so the UI stays responsive.

.. seealso::

   - :doc:`Cursors </reference/cursors>` — the pointer names.
   - :doc:`Windows guide </user-guide/feature-guides/windows>` — window-level
     behavior.
