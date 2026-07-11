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

.. note::

   This handler only sees exceptions raised **inside** the event loop — callbacks
   and ``after`` jobs. An exception raised during setup, before ``mainloop()``,
   propagates normally; wrap that code in your own ``try``/``except``.

``TclError``
------------

``TclError`` (from ``tkinter``) is the exception raised when the underlying Tcl
interpreter rejects an operation — a bad option value, an invalid widget path, a
color name it doesn't recognize, reading an empty clipboard. Catch it where such
a call is expected to fail:

.. code-block:: python

   from tkinter import TclError

   try:
       widget.configure(bootstyle="not-a-real-style")
   except TclError as err:
       ...

A common source is a numeric variable holding in-progress text: ``IntVar.get()``
raises ``TclError`` when the bound entry is empty or half-typed. Guard the read,
or validate the field instead — see
:doc:`Input validation </user-guide/feature-guides/validation>`.

.. seealso::

   The :doc:`Variables guide </user-guide/feature-guides/variables>` for the
   numeric-variable coercion gotcha, and
   :doc:`How a tkinter app runs </user-guide/foundations/how-a-tkinter-app-runs>`
   for the event loop that these callbacks run inside.
