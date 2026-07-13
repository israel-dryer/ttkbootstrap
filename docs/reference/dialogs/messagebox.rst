Messagebox
==========

``Messagebox`` shows a modal message dialog and returns which button the user
clicked. Every method is a **static method** — call it on the class, no instance
needed (``Messagebox.show_info("Saved.")``). Each blocks until the user responds
and returns the clicked button's text, or ``None`` if the dialog is closed.

Common parameters
-----------------

Every method takes ``message`` and ``title`` positionally, plus these
keyword-only options:

.. list-table::
   :header-rows: 1
   :widths: 18 16 66

   * - Option
     - Type
     - Description
   * - ``parent``
     - ``Widget``
     - The window to center over and block while open. Defaults to the
       application root.
   * - ``alert``
     - ``bool``
     - Ring the display bell when the dialog appears.
   * - ``position``
     - ``tuple``
     - An ``(x, y)`` top-left screen position. Centered on ``parent`` by default.
   * - ``buttons``
     - ``list``
     - Override the buttons — a list of labels, each optionally ``"label:bootstyle"``
       to color it (e.g. ``"OK:success"``). The label is also what the method
       returns.
   * - ``icon``
     - ``str``
     - A Bootstrap Icons glyph name shown beside the message.
   * - ``localize``
     - ``bool``
     - Translate the standard button labels through the message catalog. Default
       ``True``.

Methods
-------

.. py:staticmethod:: show_info(message, title=" ", *, parent=None, alert=False, position=None, buttons=None, icon=None, localize=True)
   :noindex:

   An informational message with an info icon and an **OK** button.

   :returns: the clicked button's text, or ``None``.

.. py:staticmethod:: show_warning(message, title=" ", *, parent=None, alert=True, position=None, buttons=None, icon=None, localize=True)
   :noindex:

   A warning message with a warning icon and an **OK** button. Rings the bell by
   default.

   :returns: the clicked button's text, or ``None``.

.. py:staticmethod:: show_error(message, title=" ", *, parent=None, alert=True, position=None, buttons=None, icon=None, localize=True)
   :noindex:

   An error message with an error icon and an **OK** button. Rings the bell by
   default.

   :returns: the clicked button's text, or ``None``.

.. py:staticmethod:: show_question(message, title=" ", *, parent=None, alert=False, position=None, buttons=None, icon=None, localize=True)
   :noindex:

   A message with a question icon and an **OK** button. Pass ``buttons`` for a
   different choice set.

   :returns: the clicked button's text, or ``None``.

.. py:staticmethod:: ok(message, title=" ", *, parent=None, alert=False, position=None, buttons=None, icon=None, localize=True)
   :noindex:

   A message with a single **OK** button.

   :returns: ``"OK"``, or ``None`` if closed.

.. py:staticmethod:: okcancel(message, title=" ", *, parent=None, alert=False, position=None, buttons=None, icon=None, localize=True)
   :noindex:

   A message with **OK** and **Cancel** buttons.

   :returns: ``"OK"`` or ``"Cancel"``, or ``None`` if closed.

.. py:staticmethod:: yesno(message, title=" ", *, parent=None, alert=False, position=None, buttons=None, icon=None, localize=True)
   :noindex:

   A message with **Yes** and **No** buttons.

   :returns: ``"Yes"`` or ``"No"``, or ``None`` if closed.

.. py:staticmethod:: yesnocancel(message, title=" ", *, parent=None, alert=False, position=None, buttons=None, icon=None, localize=True)
   :noindex:

   A message with **Yes**, **No**, and **Cancel** buttons.

   :returns: ``"Yes"``, ``"No"``, or ``"Cancel"``, or ``None`` if closed.

.. py:staticmethod:: retrycancel(message, title=" ", *, parent=None, alert=False, position=None, buttons=None, icon=None, localize=True)
   :noindex:

   A message with **Retry** and **Cancel** buttons.

   :returns: ``"Retry"`` or ``"Cancel"``, or ``None`` if closed.

See also
--------

- :doc:`Dialogs </user-guide/feature-guides/dialogs>` — how to use them, with
  examples.
- :doc:`Querybox </reference/dialogs/querybox>` — the input-and-picker facade.
- :doc:`MessageDialog </reference/dialogs/dialog-classes>` — the dialog class
  ``Messagebox`` builds, for full control.
