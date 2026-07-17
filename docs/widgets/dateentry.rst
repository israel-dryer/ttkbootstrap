DateEntry
=========

A **date entry** is a text field with a calendar button — the user types a date or
picks one from a pop-up calendar. ``DateEntry`` is a ttkbootstrap widget (a real
class with its own API, imported as ``ttk.DateEntry``). This page covers reading
and setting the date, the format and calendar options, then the ``bootstyle``
color.

.. image:: /_static/examples/dateentry-open-light.png
   :class: tb-screenshot-light
   :width: 296px
   :alt: A date entry with its pop-up calendar open — light theme

.. image:: /_static/examples/dateentry-open-dark.png
   :class: tb-screenshot-dark
   :width: 296px
   :alt: A date entry with its pop-up calendar open — dark theme

Usage
-----

Create a ``DateEntry`` and read the chosen date with ``get_date()`` — it returns a
:class:`~datetime.datetime`. ``set_date()`` puts one in:

.. code-block:: python

   import ttkbootstrap as ttk
   from ttkbootstrap.widgets import DateEntry
   from datetime import datetime

   app = ttk.App()

   picker = DateEntry(app)
   picker.pack(padx=10, pady=10)

   def use_date():
       print(picker.get_date())          # -> a datetime

   ttk.Button(app, text="Use date", command=use_date, bootstyle="primary").pack()

   picker.set_date(datetime(2025, 6, 1)) # preselect

   app.mainloop()

The widget exposes its parts as ``picker.entry`` (the text field) and
``picker.button`` (the calendar button), and ``enable()`` / ``disable()`` toggle
interaction. The ``value`` property is a shorthand for get/set.

``get_date()`` parses the **live entry text**, so typed keyboard edits are honored,
and an unparseable entry is flagged ``invalid`` when the field loses focus. If the
text is empty or can't be parsed it falls back to the last date set — it does
**not** return ``None`` here, unlike the ``Querybox.get_date`` *dialog*, which
returns ``None`` on cancel.

To run code when the user picks from the calendar, bind ``<<DateEntrySelected>>``:

.. code-block:: python

   picker.bind("<<DateEntrySelected>>", lambda event: print(picker.get_date()))

Format and calendar
-------------------

``date_format`` is a ``strftime`` pattern for how the date reads in the field;
``start_date`` is the date the widget starts on; ``first_weekday`` sets the
leftmost column (``0`` = Monday … ``6`` = Sunday):

.. code-block:: python

   DateEntry(app, date_format="%Y-%m-%d", start_date=datetime(2025, 1, 1), first_weekday=6)

``start_date`` fills the field at construction and is the date ``get_date()``
falls back to when the field is empty; the displayed date after construction is
``value`` / ``set_date()``.

``show_outside_days=False`` hides the adjacent-month days the calendar uses to pad
the first and last weeks.

Color
-----

``bootstyle`` colors the entry border and the calendar accents from the semantic
palette:

.. code-block:: python

   DateEntry(app, bootstyle="success")

Reference
---------

- :doc:`DateEntry API reference </reference/api/dateentry>` — every option and
  method.

.. seealso::

   - :doc:`Dialogs guide </user-guide/feature-guides/dialogs>` — the date picker
     dialog (``Querybox.get_date``) for asking a date without a permanent field.
   - :doc:`Entry <entry>` — a plain single-line text field.
