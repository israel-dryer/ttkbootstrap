DateEntry
=========

A **date entry** is a text field with a calendar button — the user types a date or
picks one from a pop-up calendar. ``DateEntry`` is a ttkbootstrap widget (a real
class with its own API, imported as ``ttk.DateEntry``). This page covers reading
and setting the date, the format and calendar options, then the ``bootstyle``
color.

.. admonition:: 📷 Screenshot (placeholder)
   :class: screenshot-placeholder

   A date entry closed, and with its pop-up calendar open, in light and dark
   themes.

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
interaction.

Format and calendar
-------------------

``date_format`` is a ``strftime`` pattern for how the date reads in the field;
``start_date`` sets which date (and month) the calendar opens on; ``first_weekday``
sets the leftmost column (``0`` = Monday … ``6`` = Sunday):

.. code-block:: python

   DateEntry(app, date_format="%Y-%m-%d", start_date=datetime(2025, 1, 1), first_weekday=6)

Color
-----

``bootstyle`` colors the entry border and the calendar accents from the semantic
palette:

.. code-block:: python

   DateEntry(app, bootstyle="success")

API & reference
---------------

For the complete option list and methods, see the
:doc:`DateEntry API reference </reference/api/dateentry>`.

.. seealso::

   The date **picker dialog** (``Querybox.get_date``) in the
   :doc:`Dialogs guide </user-guide/feature-guides/dialogs>` for asking a date
   without a permanent field, and :doc:`Entry <entry>` for a plain text field.
