Querybox
========

``Querybox`` prompts the user for a value and returns it. Every method is a
**static method** — call it on the class (``Querybox.get_string("Name?")``). Each
blocks until the user responds and returns the entered or chosen value, or
``None`` if the dialog is cancelled.

Two options are common to every method: ``parent`` (the window to center over and
block; defaults to the application root) and the keyword-only ``position`` (an
``(x, y)`` top-left screen position, centered on ``parent`` by default).

Text and number input
----------------------

.. py:staticmethod:: get_string(prompt="", title=" ", initialvalue=None, parent=None, *, position=None)
   :noindex:

   Ask for a line of text.

   :param prompt: the label shown above the entry.
   :param initialvalue: the value the entry starts with.
   :returns: the entered string, or ``None`` if cancelled.

.. py:staticmethod:: get_integer(prompt="", title=" ", initialvalue=None, minvalue=None, maxvalue=None, parent=None, *, position=None)
   :noindex:

   Ask for a whole number, rejecting non-integer or out-of-range input.

   :param minvalue: the smallest value accepted.
   :param maxvalue: the largest value accepted.
   :returns: the entered ``int``, or ``None`` if cancelled.

.. py:staticmethod:: get_float(prompt="", title=" ", initialvalue=None, minvalue=None, maxvalue=None, parent=None, *, position=None)
   :noindex:

   Ask for a decimal number, rejecting non-numeric or out-of-range input.

   :param minvalue: the smallest value accepted.
   :param maxvalue: the largest value accepted.
   :returns: the entered ``float``, or ``None`` if cancelled.

.. py:staticmethod:: get_item(prompt="", title=" ", initialvalue=None, items=None, parent=None, *, position=None)
   :noindex:

   Ask the user to choose one value from a list.

   :param items: the list of values to choose from.
   :param initialvalue: the value selected initially.
   :returns: the chosen item, or ``None`` if cancelled.

Pickers
-------

.. py:staticmethod:: get_date(parent=None, title=" ", first_weekday=6, start_date=None, bootstyle="primary", *, show_outside_days=True, position=None)
   :noindex:

   Open a calendar popup to pick a date (see :doc:`DatePickerDialog
   </reference/dialogs/pickers>`).

   :param first_weekday: the leftmost weekday column, ``0`` (Monday)–``6`` (Sunday).
   :param start_date: the date shown selected initially; defaults to today.
   :param bootstyle: the calendar's accent color.
   :param show_outside_days: show days spilling in from the adjacent months.
   :returns: the chosen ``datetime.date``, or ``None`` if cancelled.

.. py:staticmethod:: get_color(parent=None, title="Color Chooser", initialcolor=None, *, position=None)
   :noindex:

   Open the color chooser (see :doc:`ColorChooserDialog
   </reference/dialogs/pickers>`).

   :param initialcolor: the color selected initially (a hex string).
   :returns: the chosen color, or ``None`` if cancelled.

.. py:staticmethod:: get_font(parent=None, *, position=None)
   :noindex:

   Open the font selector (see :doc:`FontDialog </reference/dialogs/pickers>`).

   :returns: the chosen ``Font``, or ``None`` if cancelled.

Files
-----

These wrap :doc:`tkinter.filedialog </user-guide/how-to/index>`; extra keyword
arguments (``initialdir``, ``filetypes``, ``defaultextension``, …) pass straight
through. A cancelled dialog returns ``None``.

.. py:staticmethod:: get_open_filename(parent=None, **kwargs)
   :noindex:

   Choose one existing file to open.

   :returns: the file path, or ``None`` if cancelled.

.. py:staticmethod:: get_open_filenames(parent=None, **kwargs)
   :noindex:

   Choose one or more existing files to open.

   :returns: a tuple of file paths, or ``None`` if cancelled.

.. py:staticmethod:: get_save_filename(parent=None, **kwargs)
   :noindex:

   Choose a file path to save to (prompting to confirm an overwrite).

   :returns: the file path, or ``None`` if cancelled.

.. py:staticmethod:: get_directory(parent=None, **kwargs)
   :noindex:

   Choose a directory.

   :returns: the directory path, or ``None`` if cancelled.

See also
--------

- :doc:`Dialogs </user-guide/feature-guides/dialogs>` — how to use them, with
  examples.
- :doc:`Messagebox </reference/dialogs/messagebox>` — the message-dialog facade.
- :doc:`Pickers </reference/dialogs/pickers>` — the date, color, and font dialog
  classes these build.
