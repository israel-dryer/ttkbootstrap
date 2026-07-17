Dialog classes
==============

These are the dialog classes behind the :doc:`Messagebox </reference/dialogs/messagebox>`
and :doc:`Querybox </reference/dialogs/querybox>` facades. Use them directly when
you need full control over a dialog, or subclass ``Dialog`` to build your own.

Dialog
------

``Dialog`` is the base for custom dialogs. Subclass it and implement
:py:meth:`create_body` and :py:meth:`create_buttonbox`, set ``self._result``,
then call :py:meth:`show`; the outcome is read from :py:attr:`result` after
``show`` returns.

Options
~~~~~~~

Construct with ``Dialog(parent=None, title="", alert=False)``.

.. list-table::
   :header-rows: 1
   :widths: 22 16 62

   * - Option
     - Type
     - Description
   * - ``parent``
     - ``Widget``
     - The window to center over and block while open. Defaults to the
       application root.
   * - ``title``
     - ``str``
     - The text shown on the dialog's title bar.
   * - ``alert``
     - ``bool``
     - Ring the display bell when the dialog appears.

Methods
~~~~~~~

.. py:method:: show(position=None, wait_for_result=True)
   :noindex:

   Build and display the dialog modally.

   :param position: An ``(x, y)`` top-left screen position. Centered on
      ``parent`` by default.
   :param wait_for_result: Block until the dialog is closed. Default ``True``.
   :returns: ``None``. Read :py:attr:`result` after it returns.

.. py:method:: build()
   :noindex:

   Construct the dialog window and its body and button box. Called by
   :py:meth:`show`.

   :returns: ``None``.

.. py:method:: close()
   :noindex:

   Close the dialog and release its grab.

   :returns: ``None``.

.. py:method:: create_body(master)
   :noindex:

   Override hook. Subclasses build the dialog's body widgets here.

   :param master: The parent widget for the body content.
   :returns: ``None``.

.. py:method:: create_buttonbox(master)
   :noindex:

   Override hook. Subclasses build the button row here.

   :param master: The parent widget for the button box.
   :returns: ``None``.

.. py:attribute:: result
   :noindex:

   The dialog's outcome, set by the subclass. Read it after :py:meth:`show`
   returns.

MessageDialog
-------------

``MessageDialog`` is a configurable message dialog — the class
:doc:`Messagebox </reference/dialogs/messagebox>` builds. Use it directly for
custom button sets and colors.

Options
~~~~~~~

Construct with ``MessageDialog(message, title=" ", buttons=None, command=None,
width=50, parent=None, alert=False, default=None, padding=(20, 20), icon=None)``.

.. list-table::
   :header-rows: 1
   :widths: 22 16 62

   * - Option
     - Type
     - Description
   * - ``message``
     - ``str``
     - The message text.
   * - ``title``
     - ``str``
     - The text shown on the dialog's title bar.
   * - ``buttons``
     - ``list``
     - The button labels, each optionally ``"label:bootstyle"`` to color it
       (e.g. ``"OK:success"``). The clicked label becomes :py:attr:`result`.
   * - ``command``
     - ``callable``
     - A callback invoked when a button is pressed.
   * - ``width``
     - ``int``
     - The message wrap width in characters.
   * - ``parent``
     - ``Widget``
     - The window to center over and block while open.
   * - ``alert``
     - ``bool``
     - Ring the display bell when the dialog appears.
   * - ``default``
     - ``str``
     - The label of the button focused by default.
   * - ``padding``
     - ``int | tuple``
     - Padding around the content.
   * - ``icon``
     - ``str``
     - A Bootstrap Icons glyph name shown beside the message.

Methods
~~~~~~~

.. py:method:: show(position=None, wait_for_result=True)
   :noindex:

   Build and display the dialog modally.

   :param position: An ``(x, y)`` top-left screen position. Centered on
      ``parent`` by default.
   :param wait_for_result: Block until the dialog is closed. Default ``True``.
   :returns: ``None``. Read :py:attr:`result` after it returns.

.. py:attribute:: result
   :noindex:

   The clicked button's text, or ``None`` if the dialog is closed.

QueryDialog
-----------

``QueryDialog`` is a configurable input dialog — the class
:doc:`Querybox </reference/dialogs/querybox>` builds. It collects a typed value,
or a choice from a list.

Options
~~~~~~~

Construct with ``QueryDialog(prompt, title=" ", initialvalue="", minvalue=None,
maxvalue=None, width=65, datatype=str, padding=(20, 20), parent=None,
items=None)``.

.. list-table::
   :header-rows: 1
   :widths: 22 16 62

   * - Option
     - Type
     - Description
   * - ``prompt``
     - ``str``
     - The label shown above the input.
   * - ``title``
     - ``str``
     - The text shown on the dialog's title bar.
   * - ``initialvalue``
     - ``any``
     - The value the input starts with.
   * - ``minvalue``
     - ``any``
     - The smallest accepted value (numeric datatypes).
   * - ``maxvalue``
     - ``any``
     - The largest accepted value (numeric datatypes).
   * - ``width``
     - ``int``
     - The entry width in characters.
   * - ``datatype``
     - ``type``
     - The type the input is validated and cast to (``str``, ``int``,
       ``float``).
   * - ``padding``
     - ``int | tuple``
     - Padding around the content.
   * - ``parent``
     - ``Widget``
     - The window to center over and block while open.
   * - ``items``
     - ``list``
     - If given, the user chooses from this list instead of typing.

Methods
~~~~~~~

.. py:method:: show(position=None, wait_for_result=True)
   :noindex:

   Build and display the dialog modally.

   :param position: An ``(x, y)`` top-left screen position. Centered on
      ``parent`` by default.
   :param wait_for_result: Block until the dialog is closed. Default ``True``.
   :returns: ``None``. Read :py:attr:`result` after it returns.

.. py:attribute:: result
   :noindex:

   The entered or chosen value cast to ``datatype``, or ``None`` if cancelled.

.. py:method:: validate()
   :noindex:

   Called when the user submits, before the dialog closes. The default checks
   the ``datatype`` cast, the ``minvalue``/``maxvalue`` range, and membership
   in ``items``; override it in a subclass to add your own checks.

   :returns: ``True`` to accept and close; ``False`` to keep the dialog open.
   :rtype: bool

.. py:method:: apply()
   :noindex:

   Called after a validated submit closes the dialog (a no-op by default).
   Override it in a subclass to process the result.

   :returns: ``None``.

See also
--------

- :doc:`Dialogs </user-guide/feature-guides/dialogs>` — how to use them, with
  examples.
- :doc:`Messagebox </reference/dialogs/messagebox>` — the message-dialog facade.
- :doc:`Querybox </reference/dialogs/querybox>` — the input-and-picker facade.
