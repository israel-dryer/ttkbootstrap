How a tkinter app runs
======================

A tkinter program is **event-driven**. You build your widgets, then hand control
to tkinter's *event loop*, which waits for things to happen — a click, a
keystroke, a timer — and runs your code in response. Almost everything your app
does happens inside a callback the loop calls; understanding that loop is the
single most useful mental model in tkinter.

The main loop
-------------

Every app ends with one call to ``mainloop()``:

.. code-block:: python

   import ttkbootstrap as ttk

   app = ttk.App(title="Hello")
   ttk.Label(app, text="Hello, tkinter").pack(padx=20, pady=20)

   app.mainloop()          # <- hands control to the event loop

``mainloop()`` **blocks**: it runs until the window is closed, processing events
the whole time. Code written *after* ``mainloop()`` does not run until the app
exits, so it is almost always the last line. Call it **once**, on your single
``App`` root.

Until ``mainloop()`` runs, the window isn't drawn yet — which is why a widget's
*actual* size and position aren't known before then (``winfo_width()`` returns
``1``). Read ``winfo_reqwidth()`` for the requested size, which is valid
immediately; see :doc:`Widget & screen info </reference/winfo>`.

Your code runs in callbacks
---------------------------

You don't call your handlers — the loop does, when the matching event fires. The
two ways to register one are ``command=`` (for the widgets that take it) and
``bind`` (for any event on any widget):

.. code-block:: python

   def greet():
       print("clicked!")

   ttk.Button(app, text="Greet", command=greet).pack()

See :doc:`Events & callbacks </user-guide/foundations/events-and-callbacks>` for
the full binding story. The important idea here is the *flow*: build widgets →
enter the loop → the loop calls your callbacks → each returns → the loop waits
for the next event.

Don't block the loop
--------------------

Because your callbacks run **on** the event loop, a callback that takes a long
time freezes the whole UI — nothing redraws or responds until it returns:

.. code-block:: python

   def slow():
       data = crunch_numbers()      # takes 10 seconds -> UI frozen for 10 seconds

   ttk.Button(app, text="Go", command=slow)

The fix is never to do long work directly in a callback. Break it into small
steps scheduled with ``after`` (below), or run it on a background thread and send
the result back to the loop. For a quick "working…" state while a short step
blocks, see :doc:`Feedback: bell & busy </user-guide/how-to/feedback>`.

Scheduling with ``after``
-------------------------

``after(delay_ms, func, *args)`` asks the loop to call ``func`` later, without
blocking. It returns an id you can cancel with ``after_cancel``:

.. code-block:: python

   app.after(1000, lambda: print("one second later"))

   job = app.after(5000, cleanup)
   app.after_cancel(job)          # changed my mind

To repeat work — a clock, a poll, an animation frame — have the callback
**re-schedule itself**. That keeps each step short and the UI responsive between
them:

.. code-block:: python

   def tick():
       update_clock()
       app.after(1000, tick)      # run again in a second

   tick()                         # start the cycle

``after(0, func)`` runs ``func`` as soon as the loop is next idle — a handy way
to defer work until after the current callback returns.

Forcing the loop: ``update_idletasks`` vs ``update``
----------------------------------------------------

Sometimes you need pending work to happen *now*, mid-callback, instead of after
you return to the loop:

- ``update_idletasks()`` processes only the **idle** tasks — pending redraws and
  geometry recalculation. Use it to flush a visual change before a blocking step
  (e.g. show a busy cursor, or read a window's just-computed size).
- ``update()`` processes **all** pending events, including user input. It is a
  blunt instrument: because it re-enters the event loop, a stray click can fire
  another callback in the middle of your current one. Prefer ``after`` or a
  thread over using ``update()`` as a "wait."

.. warning::

   Reach for ``update_idletasks()`` when you just need the display to catch up;
   avoid ``update()`` unless you understand the re-entrancy it invites.

A running example
-----------------

A counter that increments once a second — entirely inside the loop, never
blocking it:

.. code-block:: python

   import ttkbootstrap as ttk

   app = ttk.App(title="Counter")
   count = ttk.IntVar(value=0)

   ttk.Label(app, textvariable=count, font="-size 24").pack(padx=40, pady=20)

   def tick():
       count.set(count.get() + 1)
       app.after(1000, tick)

   tick()
   app.mainloop()

.. seealso::

   :doc:`Events & callbacks </user-guide/foundations/events-and-callbacks>` for
   binding handlers, and :doc:`Widget & screen info </reference/winfo>` for why
   sizes aren't known until the loop runs.
