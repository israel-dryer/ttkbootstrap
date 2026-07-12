Lifecycle
=========

Methods that create pauses in, force work through, or tear down the event loop
for a widget — used to refresh the display mid-task, wait for something to
happen, or destroy a widget.

.. py:method:: destroy()
   :noindex:

   Destroy the widget and all of its descendants, unbinding their callbacks and
   releasing their resources. Referencing a destroyed widget afterward raises.

   :returns: ``None``.

.. py:method:: update_idletasks()
   :noindex:

   Process pending **idle** work — geometry recalculation and redraws — without
   handling user input. The safe way to force the display to catch up in the
   middle of a task.

   :returns: ``None``.

.. py:method:: update()
   :noindex:

   Process **all** pending events, including user input and redraws. Powerful but
   easy to misuse: it can re-enter your own callbacks. Prefer
   ``update_idletasks`` unless you truly need input processed.

   :returns: ``None``.

.. py:method:: wait_variable(name)
   :noindex:

   Enter a local event loop until the given variable is written. Alias:
   ``waitvar``.

   :param name: a tkinter variable (``StringVar``, ``IntVar``, …) to wait on.
   :returns: ``None``.

.. py:method:: wait_window(window=None)
   :noindex:

   Enter a local event loop until ``window`` is destroyed — the usual way to wait
   for a modal dialog to close.

   :param window: the widget to wait for; defaults to this widget.
   :returns: ``None``.

.. py:method:: wait_visibility(window=None)
   :noindex:

   Enter a local event loop until ``window`` becomes visible on screen.

   :param window: the widget to wait for; defaults to this widget.
   :returns: ``None``.

.. py:method:: bell(displayof=0)
   :noindex:

   Ring the system bell.

   :param displayof: ring on the display of the given widget, if provided.
   :returns: ``None``.
