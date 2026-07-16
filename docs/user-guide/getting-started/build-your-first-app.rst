Build your first app
====================

The :doc:`Quickstart <quickstart>` put a themed window on the screen. This
tutorial builds a small but *complete* application on top of it — a contact
book with a form, live input validation, and a searchable data table — so you
touch every part of a real ttkbootstrap app in one sitting: layout, widgets,
events, state, and styling.

We build it one piece at a time. Each step is runnable on its own, and each
links onward to the Foundations page that covers the idea in depth. The
:ref:`complete program <first-app-complete>` is at the end.

.. admonition:: 📷 Screenshot (placeholder)
   :class: screenshot-placeholder

   The finished contact book: a "New contact" form (name, email, category, and
   an **Add contact** button) above a searchable table listing the contacts,
   with a status line at the bottom.

What you need
-------------

ttkbootstrap installed (see :doc:`Installation <installation>`) and Python
3.10+. Everything here uses only ``ttkbootstrap`` — no other dependencies.

Step 1 — the application shell
------------------------------

Every ttkbootstrap app starts with a **root window** and ends with
``mainloop()``, the call that hands control to tkinter's event loop and keeps
the window alive. In between you build your interface.

We put the interface in a :class:`~ttkbootstrap.Frame` subclass rather than
piling widgets directly onto the root. A frame is a container; subclassing it
keeps the app's state and its widgets together in one object, which is how real
apps stay organized as they grow.

.. code-block:: python

   import ttkbootstrap as ttk
   from ttkbootstrap.constants import *


   class ContactBook(ttk.Frame):
       def __init__(self, master):
           super().__init__(master, padding=16)
           self.pack(fill=BOTH, expand=YES)

           ttk.Label(self, text="Contact Book", font="-size 16 -weight bold").pack()


   app = ttk.App(title="Contact Book", theme="bootstrap-light", size=(560, 520))
   ContactBook(app)
   app.mainloop()

- :class:`~ttkbootstrap.App` is the enhanced root — it creates the window *and*
  installs the theme in one step. (It is also exported as ``ttk.Window``; both
  name the same class.)
- ``padding=16`` insets the frame's contents so nothing hugs the window edge.
- ``pack(fill=BOTH, expand=YES)`` makes the frame grow to fill the window. We
  import ``*`` from :mod:`ttkbootstrap.constants` so anchors and fills read as
  ``BOTH``/``YES``/``W`` instead of string literals.

.. seealso::

   - :doc:`How a tkinter app runs </user-guide/foundations/how-a-tkinter-app-runs>`
     — the event loop and why ``mainloop()`` comes last.
   - :doc:`Structuring an app <app-structures>` — the root and single-root rule.

Step 2 — a form with ``grid``
-----------------------------

Forms are rows of *label + input*, so we lay them out with **grid** — the
geometry manager built for aligned rows and columns. Each widget names its
``row`` and ``column``; ``sticky`` says which edges it clings to inside its
cell.

Put this in a new method and call it from ``__init__``:

.. code-block:: python

   def _build_form(self):
       form = ttk.Labelframe(self, text="New contact", padding=12)
       form.pack(fill=X)
       form.columnconfigure(1, weight=1)          # let the input column stretch

       ttk.Label(form, text="Name").grid(row=0, column=0, sticky=W, padx=(0, 8), pady=4)
       ttk.Entry(form).grid(row=0, column=1, sticky=EW, pady=4)

       ttk.Label(form, text="Email").grid(row=1, column=0, sticky=W, padx=(0, 8), pady=4)
       ttk.Entry(form).grid(row=1, column=1, sticky=EW, pady=4)

       ttk.Label(form, text="Category").grid(row=2, column=0, sticky=W, padx=(0, 8), pady=4)
       category = ttk.Combobox(form, values=["Friend", "Family", "Work"], state="readonly")
       category.grid(row=2, column=1, sticky=EW, pady=4)

The two pieces that make a grid form behave:

- ``columnconfigure(1, weight=1)`` gives column 1 (the inputs) all the spare
  horizontal space, so the entries stretch with the window while the labels in
  column 0 stay their natural width.
- ``sticky=EW`` on the inputs makes them fill that space left-to-right;
  ``sticky=W`` left-aligns the labels.

``ttk.Labelframe`` is just a frame with a titled border — a tidy way to group
the form. The ``state="readonly"`` combobox lets the user pick a category but
not type a new one.

.. admonition:: 📷 Screenshot (placeholder)
   :class: screenshot-placeholder

   The "New contact" labelframe with aligned Name, Email, and Category rows; the
   entry and combobox stretch to the frame width.

.. seealso::

   :doc:`Layout with grid </user-guide/foundations/layout-with-grid>` builds a
   responsive form step by step — cells, sticky, padding, weight, and spanning.

Step 3 — hold the data with variables
--------------------------------------

Right now the entries hold text, but our code has no handle on it. We bind each
input to a **variable** — a ``StringVar`` — with ``textvariable=``. The variable
and the widget stay in sync automatically: read the variable to get what the
user typed, ``set`` it to change what the widget shows.

Create the variables in ``__init__`` (before building the form) and attach them:

.. code-block:: python

   # in __init__, before self._build_form()
   self.name = ttk.StringVar()
   self.email = ttk.StringVar()
   self.category = ttk.StringVar(value="Friend")

.. code-block:: python

   # in _build_form, add textvariable= to each input
   ttk.Entry(form, textvariable=self.name).grid(row=0, column=1, sticky=EW, pady=4)
   ...
   ttk.Entry(form, textvariable=self.email).grid(row=1, column=1, sticky=EW, pady=4)
   ...
   category = ttk.Combobox(form, textvariable=self.category,
                           values=["Friend", "Family", "Work"], state="readonly")
   category.grid(row=2, column=1, sticky=EW, pady=4)

Giving ``category`` an initial ``value`` preselects "Friend" in the combobox.

.. seealso::

   :doc:`Variables & reactivity </user-guide/foundations/state-and-variables>`
   and the :doc:`Variables </user-guide/feature-guides/variables>` feature guide
   for tracing changes and the other variable types.

Step 4 — validate the email
---------------------------

A contact book with malformed emails is not much use. ttkbootstrap ships a small
validation framework: attach a rule to an input and a failing value flags the
widget with a ``danger``-red border until it becomes valid again.

Keep a reference to the email entry so we can attach a rule to it:

.. code-block:: python

   # in _build_form, replace the plain email Entry line:
   email_entry = ttk.Entry(form, textvariable=self.email)
   email_entry.grid(row=1, column=1, sticky=EW, pady=4)
   ttk.Validation.regex(email_entry, r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

:meth:`~ttkbootstrap.Validation.regex` passes when the contents match the
pattern (here: *something* ``@`` *something* ``.`` *something*). By default the
rule fires on **focus-out**, so the field flags only after the user leaves it —
not on every keystroke.

.. admonition:: 📷 Screenshot (placeholder)
   :class: screenshot-placeholder

   The email entry showing a ``danger``-red border after an invalid address
   loses focus, beside a valid one with the normal border.

.. seealso::

   :doc:`Input validation </user-guide/feature-guides/validation>` for the full
   rule set, custom rules, and controlling *when* rules run.

Step 5 — show the contacts in a table
--------------------------------------

Contacts need somewhere to live. :class:`~ttkbootstrap.widgets.Tableview` is
ttkbootstrap's data table — a themed grid with sorting, an optional search bar,
and column controls built in. We give it column headings and start it empty:

.. code-block:: python

   def _build_table(self):
       self.table = ttk.Tableview(
           self,
           coldata=["Name", "Email", "Category"],
           rowdata=[],
           searchable=True,
           bootstyle="primary",
           height=8,
       )
       self.table.pack(fill=BOTH, expand=YES, pady=(16, 8))

- ``coldata`` is the list of column headings; ``rowdata=[]`` starts with no
  rows.
- ``searchable=True`` adds the search bar above the table — press **Enter** in
  it to filter.
- ``fill=BOTH, expand=YES`` lets the table soak up the space below the form as
  the window resizes.

.. seealso::

   The :doc:`Tableview widget page </widgets/tableview>` for its full API —
   pagination, column configuration, exporting, and programmatic selection.

Step 6 — wire the button to a callback
--------------------------------------

The last piece connects the form to the table. A button runs a **callback** —
the function you pass as ``command=`` — when clicked. Ours reads the variables,
adds a row, and resets the form.

Add the button to the form, and the method it calls:

.. code-block:: python

   # at the end of _build_form:
   add_button = ttk.Button(form, text="Add contact", bootstyle="success",
                           command=self.add_contact)
   add_button.grid(row=3, column=1, sticky=E, pady=(8, 0))

.. code-block:: python

   def add_contact(self):
       name = self.name.get().strip()
       email = self.email.get().strip()
       if not name or not email:
           self.status.configure(text="Name and email are required.", bootstyle="danger")
           return
       self.table.insert_row(values=[name, email, self.category.get()])
       count = len(self.table.get_rows())
       self.status.configure(text=f"{count} contact(s).", bootstyle="secondary")
       self.name.set("")
       self.email.set("")

Notice how the pieces come together: we ``get()`` the variables we bound in
step 3, guard against empty input, :meth:`~ttkbootstrap.widgets.Tableview.insert_row`
into the table from step 5 (it refreshes the view for us), then ``set("")`` to
clear the entries for the next contact. ``command=self.add_contact`` passes the
method itself — no parentheses; tkinter calls it for you on each click.

The status line is a label at the bottom of the app; add a method to build it
and call it from ``__init__``:

.. code-block:: python

   def _build_status(self):
       self.status = ttk.Label(self, text="No contacts yet.", bootstyle="secondary")
       self.status.pack(fill=X)

.. seealso::

   :doc:`Events & callbacks </user-guide/foundations/events-and-callbacks>`
   for ``command`` vs ``bind``, the event object, and ``after``.

A note on styling
-----------------

We styled as we went, with ``bootstyle=`` — ``"success"`` for the Add button,
``"primary"`` for the table's accents, ``"secondary"``/``"danger"`` on the
status label to signal calm vs. error. ``bootstyle`` describes *intent* (a
color and, optionally, a variant), never a literal color, so the whole app
re-themes when you change ``theme`` on the ``App``. Try
``theme="bootstrap-dark"`` — every widget follows.

.. seealso::

   :doc:`Styling with bootstyle </user-guide/foundations/bootstyle-grammar>`
   for the full grammar and the reference table of every keyword.

.. _first-app-complete:

The complete app
----------------

.. code-block:: python

   import ttkbootstrap as ttk
   from ttkbootstrap.constants import *


   class ContactBook(ttk.Frame):
       def __init__(self, master):
           super().__init__(master, padding=16)
           self.pack(fill=BOTH, expand=YES)

           self.name = ttk.StringVar()
           self.email = ttk.StringVar()
           self.category = ttk.StringVar(value="Friend")

           self._build_form()
           self._build_table()
           self._build_status()

       def _build_form(self):
           form = ttk.Labelframe(self, text="New contact", padding=12)
           form.pack(fill=X)
           form.columnconfigure(1, weight=1)

           ttk.Label(form, text="Name").grid(row=0, column=0, sticky=W, padx=(0, 8), pady=4)
           ttk.Entry(form, textvariable=self.name).grid(row=0, column=1, sticky=EW, pady=4)

           ttk.Label(form, text="Email").grid(row=1, column=0, sticky=W, padx=(0, 8), pady=4)
           email_entry = ttk.Entry(form, textvariable=self.email)
           email_entry.grid(row=1, column=1, sticky=EW, pady=4)
           ttk.Validation.regex(email_entry, r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

           ttk.Label(form, text="Category").grid(row=2, column=0, sticky=W, padx=(0, 8), pady=4)
           category = ttk.Combobox(form, textvariable=self.category,
                                   values=["Friend", "Family", "Work"], state="readonly")
           category.grid(row=2, column=1, sticky=EW, pady=4)

           add_button = ttk.Button(form, text="Add contact", bootstyle="success",
                                   command=self.add_contact)
           add_button.grid(row=3, column=1, sticky=E, pady=(8, 0))

       def _build_table(self):
           self.table = ttk.Tableview(
               self,
               coldata=["Name", "Email", "Category"],
               rowdata=[],
               searchable=True,
               bootstyle="primary",
               height=8,
           )
           self.table.pack(fill=BOTH, expand=YES, pady=(16, 8))

       def _build_status(self):
           self.status = ttk.Label(self, text="No contacts yet.", bootstyle="secondary")
           self.status.pack(fill=X)

       def add_contact(self):
           name = self.name.get().strip()
           email = self.email.get().strip()
           if not name or not email:
               self.status.configure(text="Name and email are required.", bootstyle="danger")
               return
           self.table.insert_row(values=[name, email, self.category.get()])
           count = len(self.table.get_rows())
           self.status.configure(text=f"{count} contact(s).", bootstyle="secondary")
           self.name.set("")
           self.email.set("")


   app = ttk.App(title="Contact Book", theme="bootstrap-light", size=(560, 520))
   ContactBook(app)
   app.mainloop()

Where to go next
----------------

You have now used every layer of a ttkbootstrap app. To go deeper:

- **Structure** — :doc:`Structuring an app <app-structures>` for the root, the
  single-root rule, and larger app skeletons.
- **Layout** — :doc:`Layout with grid </user-guide/foundations/layout-with-grid>`
  and :doc:`Layout with pack </user-guide/foundations/layout-with-pack>`.
- **Data** — the :doc:`Variables </user-guide/feature-guides/variables>` and
  :doc:`Events </user-guide/feature-guides/events>` feature guides.
- **Styling** — :doc:`Styling with bootstyle </user-guide/foundations/bootstyle-grammar>`
  and the :doc:`Theming & Colors </user-guide/feature-guides/theming>` guide.
