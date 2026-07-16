Handle callback errors
======================

When an exception escapes a callback — a ``command=`` handler, a ``bind``
callback, an ``after`` job — tkinter does **not** crash the app. It catches the
exception, prints a traceback to the console, and keeps the event loop running.
That default keeps a typo from killing the whole UI, but it also means errors
pass silently for anyone not watching the terminal. This page shows how to take
over that handling, and how to deal with the one tkinter-specific exception,
``TclError``.

Catching every uncaught callback error
--------------------------------------

The root routes every uncaught callback exception through one method,
``report_callback_exception(exc, val, tb)``. Override it to log the error or show
the user a dialog instead of printing to a console they may never see:

.. code-block:: python

   import traceback
   import ttkbootstrap as ttk
   from ttkbootstrap import Messagebox

   app = ttk.App()

   def report_callback_exception(exc, val, tb):
       traceback.print_exception(exc, val, tb)          # still log it
       Messagebox.show_error(f"Something went wrong:\n{val}", "Error", parent=app)

   app.report_callback_exception = report_callback_exception

The three arguments are the standard ``sys.exc_info`` triple — exception type,
value, and traceback. This is your **safety net**, not a substitute for handling
expected failures where they happen; use it to make sure nothing fails
*invisibly*.

Set it on the root. Every window's callback errors route to the root's handler,
so one covers the whole app — and a handler set on a ``Toplevel`` is never
called at all.

.. note::

   This handler only sees exceptions raised inside a **callback** — a ``command=``
   handler, a ``bind`` callback, an ``after`` job. Straight-line setup code is not
   a callback, so an exception there propagates normally; wrap that code in your
   own ``try``/``except``.

.. warning::

   If a repeating ``after`` job is what's failing, showing a modal dialog from
   this handler queues one dialog per tick. Log instead, or stop the job before
   you show anything.

``TclError``
------------

``TclError`` (from ``tkinter``) is the exception raised when the underlying Tcl
interpreter rejects an operation — a bad option value, an invalid widget path, a
color name it doesn't recognize, reading an empty clipboard. Catch it where such
a call is expected to fail:

.. code-block:: python

   from tkinter import TclError

   try:
       text = app.clipboard_get()
   except TclError:
       text = ""          # the clipboard is empty, or holds something that isn't text

A common source is a numeric variable holding in-progress text: ``IntVar.get()``
raises ``TclError`` when the bound entry is empty or half-typed. Guard the read,
or validate the field instead — see
:doc:`Input validation </user-guide/feature-guides/validation>`.

.. note::

   An unrecognized ``bootstyle`` is **not** one of these cases. Rather than
   raising, an unknown token warns and is ignored, and the widget falls back to
   its plain style — so a misspelled ``bootstyle`` shows up as a widget that
   looks wrong, not as an exception you can catch.

.. seealso::

   - :doc:`Variables guide </user-guide/feature-guides/variables>` — the
     numeric-variable coercion gotcha.
   - :doc:`Copy and paste text <clipboard>` — the clipboard call guarded above.
   - :doc:`The bootstyle grammar </user-guide/foundations/bootstyle-grammar>` —
     the token vocabulary, and what an unknown token does.
   - :doc:`How a tkinter app runs </user-guide/foundations/how-a-tkinter-app-runs>`
     — the event loop that these callbacks run inside.
