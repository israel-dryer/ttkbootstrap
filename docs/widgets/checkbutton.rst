Checkbutton
===========

A **checkbutton** is an on/off control bound to a variable. ``Checkbutton`` is the
native ``ttk.Checkbutton``, styled with ``bootstyle=``. This page covers binding
it, reacting to a toggle, the switch and toolbutton looks, non-boolean values,
then the ``bootstyle`` color and states.

.. admonition:: 📷 Screenshot (placeholder)
   :class: screenshot-placeholder

   A checkbox, a round toggle switch, and a toolbutton checkbutton — each shown
   on and off, in light and dark themes.

Usage
-----

Bind the checkbutton to a ``BooleanVar`` with ``variable=``. The variable is
``True`` when checked and ``False`` when not; read it with ``.get()``:

.. code-block:: python

   import ttkbootstrap as ttk

   app = ttk.App()

   agree = ttk.BooleanVar()
   ttk.Checkbutton(app, text="I agree", variable=agree).pack(padx=10, pady=10)

   ttk.Button(app, text="Continue", command=lambda: print(agree.get()), bootstyle="primary").pack()

   app.mainloop()

To run code the moment it is toggled, pass ``command=`` — it fires on each change,
after the variable has updated:

.. code-block:: python

   def on_toggle():
       print("now", agree.get())

   ttk.Checkbutton(app, text="Notifications", variable=agree, command=on_toggle)

Switch and toolbutton looks
---------------------------

The same control renders three ways — combine the look with a color. A
``round toggle`` or ``square toggle`` draws it as a **switch**, which reads better
than a checkbox for a settings on/off:

.. code-block:: python

   ttk.Checkbutton(app, text="Wi-Fi", variable=agree, bootstyle="round toggle")
   ttk.Checkbutton(app, text="Wi-Fi", variable=agree, bootstyle="square toggle")

``toolbutton`` draws it as a button that stays pressed while checked — for a
toolbar or a filter chip:

.. code-block:: python

   ttk.Checkbutton(app, text="Bold", variable=agree, bootstyle="toolbutton")

.. admonition:: 📷 Screenshot (placeholder)
   :class: screenshot-placeholder

   A round toggle, a square toggle, and a toolbutton checkbutton, each in its on
   and off state.

Non-boolean values
------------------

The value need not be a boolean. Bind a ``StringVar`` (or ``IntVar``) and set
``onvalue=`` / ``offvalue=`` to store your own values for the two states:

.. code-block:: python

   status = ttk.StringVar(value="off")
   ttk.Checkbutton(app, text="Active", variable=status, onvalue="on", offvalue="off")

Color
-----

``bootstyle`` sets the color of the check mark or toggle when it is **on**:

.. code-block:: python

   ttk.Checkbutton(app, text="Success", variable=agree, bootstyle="success")
   ttk.Checkbutton(app, text="Danger",  variable=agree, bootstyle="danger round toggle")

States
------

Toggle ``disabled`` to grey the control out and block clicks:

.. code-block:: python

   check.state(["disabled"])
   check.state(["!disabled"])

Read or change the value through the bound variable, or drive the widget directly
with ``invoke`` (toggle) and ``instate`` (read):

.. code-block:: python

   agree.get()                     # -> True / False
   agree.set(True)                 # check it

   check.invoke()                  # toggle it programmatically
   check.instate(["selected"])     # read the checked state directly

The ``alternate`` state shows an indeterminate "mixed" mark — for a "select all"
that is only partly on:

.. code-block:: python

   check.state(["alternate"])
   check.state(["!alternate"])

.. note::

   A checkbutton created without ``variable=`` starts in the ``alternate`` state.
   Bind a ``variable=``, or clear it with ``check.state(["!alternate"])``, to start
   it unchecked.

API & reference
---------------

``Checkbutton`` is the native ``ttk.Checkbutton`` — ttkbootstrap adds ``bootstyle=``
but no other Python API. For its constructor and options (``variable``, ``text``,
``command``, ``onvalue``, ``offvalue``, ``state``, …) see the
`tkinter.ttk.Checkbutton <https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Checkbutton>`__
reference.

.. seealso::

   :doc:`Radiobutton <radiobutton>` for a mutually exclusive group of choices.
   Want to restyle the checkbutton yourself? The
   :ref:`checkbutton's styling options <checkbutton-styling>` (which also cover
   the switch/toggle look) and its companion
   :doc:`Custom styles </user-guide/feature-guides/custom-styles>` guide document
   the hand-styling surface.
