Checkbutton
===========

A **checkbutton** is an on/off control bound to a variable. ``Checkbutton`` is the
native ``ttk.Checkbutton``, styled with ``bootstyle=``. This page covers binding
it, reacting to a toggle, the switch and toolbutton looks, non-boolean values,
then the ``bootstyle`` color and states.

.. image:: /_static/examples/checkbutton-hero-light.png
   :class: tb-screenshot-light
   :width: 281px
   :alt: A checkbox, a round toggle switch, and a toolbutton checkbutton, each on and off — light theme

.. image:: /_static/examples/checkbutton-hero-dark.png
   :class: tb-screenshot-dark
   :width: 281px
   :alt: A checkbox, a round toggle switch, and a toolbutton checkbutton, each on and off — dark theme

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

To run code when the user toggles it, pass ``command=`` — it fires when the
checkbutton is **invoked** (clicked, or activated with :kbd:`Space` while
focused), after the variable has updated, so it can read the new value:

.. code-block:: python

   def on_toggle():
       print("now", agree.get())

   ttk.Checkbutton(app, text="Notifications", variable=agree, command=on_toggle)

To react to the value however it changes, trace the variable instead:

.. code-block:: python

   agree.trace_add("write", lambda *_: print("now", agree.get()))

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

A toolbutton comes in three fills, quietest to boldest. ``ghost toolbutton`` is
transparent until checked, then shows a subtle wash — the least noisy option for
a flat toolbar where only the on button should stand out. ``outline toolbutton``
adds a colored border at rest, and plain ``toolbutton`` fills solid when checked.
Prefix any of them with a color:

.. code-block:: python

   ttk.Checkbutton(app, text="Bold", variable=agree, bootstyle="ghost toolbutton")
   ttk.Checkbutton(app, text="Bold", variable=agree, bootstyle="primary outline toolbutton")

.. image:: /_static/examples/checkbutton-looks-light.png
   :class: tb-screenshot-light
   :width: 294px
   :alt: A round toggle, a square toggle, and a toolbutton checkbutton, each on and off — light theme

.. image:: /_static/examples/checkbutton-looks-dark.png
   :class: tb-screenshot-dark
   :width: 294px
   :alt: A round toggle, a square toggle, and a toolbutton checkbutton, each on and off — dark theme

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

The widget keeps the ``selected`` state in sync with the variable (set whenever the
variable equals ``onvalue``), so ``instate`` mirrors what ``.get()`` reports.

The ``alternate`` state shows an indeterminate "mixed" mark — for a "select all"
that is only partly on:

.. code-block:: python

   check.state(["alternate"])
   check.state(["!alternate"])

.. note::

   A checkbutton created without ``variable=`` starts in the ``alternate`` state.
   Bind a ``variable=``, or clear it with ``check.state(["!alternate"])``, to start
   it unchecked.

Reference
---------

``Checkbutton`` is the native ``ttk.Checkbutton``; ttkbootstrap adds only the
``bootstyle`` keyword.

- :doc:`Checkbutton API reference </reference/api/checkbutton>` — every option and
  method.
- :ref:`Checkbutton styling options <checkbutton-styling>` — restyle it yourself
  (these cover the switch/toggle look too), with the
  :doc:`Custom styles </user-guide/feature-guides/custom-styles>` guide.

.. seealso::

   - :doc:`Radiobutton <radiobutton>` — a mutually exclusive group of choices.
