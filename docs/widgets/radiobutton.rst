Radiobutton
===========

A **radiobutton** is one option in a mutually exclusive group — pick one and the
others clear. ``Radiobutton`` is the native ``ttk.Radiobutton``, styled with
``bootstyle=``. This page covers building a group, reacting to a choice, the
toolbutton look, then the ``bootstyle`` color and states.

.. admonition:: 📷 Screenshot (placeholder)
   :class: screenshot-placeholder

   A vertical radio group and a horizontal toolbutton (segmented) group, in light
   and dark themes.

Usage
-----

A group is several radiobuttons that **share one variable**, each with a distinct
``value=``. The shared variable holds the selected value; setting it selects the
matching button and clears the rest:

.. code-block:: python

   import ttkbootstrap as ttk

   app = ttk.App()

   size = ttk.StringVar(value="medium")

   for label in ["small", "medium", "large"]:
       ttk.Radiobutton(app, text=label.title(), variable=size, value=label).pack(anchor="w", padx=10)

   ttk.Button(app, text="Order", command=lambda: print(size.get()), bootstyle="primary").pack(pady=10)

   app.mainloop()

Giving the variable an initial ``value`` (``"medium"`` above) preselects that
button.

Reacting to a choice
--------------------

To run code the moment the selection changes, pass ``command=`` — it fires on the
button that becomes selected:

.. code-block:: python

   def on_choice():
       print("chose", size.get())

   ttk.Radiobutton(app, text="Small", variable=size, value="small", command=on_choice)

The toolbutton look
-------------------

``toolbutton`` draws the group as **segmented buttons** — a connected row where the
selected option stays pressed. Pack them side by side for a compact single-choice
control:

.. code-block:: python

   from ttkbootstrap.constants import *

   view = ttk.StringVar(value="list")
   group = ttk.Frame(app)
   group.pack()

   for label in ["list", "grid", "columns"]:
       ttk.Radiobutton(group, text=label.title(), variable=view, value=label,
                       bootstyle="toolbutton").pack(side=LEFT)

.. admonition:: 📷 Screenshot (placeholder)
   :class: screenshot-placeholder

   A three-segment toolbutton group with the middle option selected.

Color
-----

``bootstyle`` sets the color of the selected indicator (or the pressed segment for
``toolbutton``):

.. code-block:: python

   ttk.Radiobutton(app, text="Info", variable=size, value="s", bootstyle="info")
   ttk.Radiobutton(app, text="On", variable=view, value="x", bootstyle="success toolbutton")

States
------

Toggle the ``disabled`` state to grey a button out and block it; which button is
selected follows the shared variable, so you change the selection by setting the
variable, not a state:

.. code-block:: python

   radio.state(["disabled"])           # greyed out, not clickable
   radio.state(["!disabled"])          # re-enable

   size.set("large")                   # select a button by its value
   radio.invoke()                      # select this button programmatically

A radiobutton created without an explicit ``variable=`` starts in the
indeterminate ``alternate`` state — its default variable is unset, so it looks
unselected, the same mixed state a :doc:`Checkbutton <checkbutton>` shows. Bind a
variable and set it to a button's ``value`` to select that button and clear the
rest.

.. note::

   The shared ``variable=`` is what links a group — selecting one button clears
   the others. Give **each group its own variable**. Radiobuttons created *without*
   an explicit ``variable=`` don't become independent: they all fall back to the
   same built-in default variable and interfere as one accidental group.

API & reference
---------------

``Radiobutton`` is the native ``ttk.Radiobutton`` — ttkbootstrap adds ``bootstyle=``
but no other Python API. For its constructor and options (``variable``, ``value``,
``text``, ``command``, ``state``, …) see the
`tkinter.ttk.Radiobutton <https://docs.python.org/3/library/tkinter.ttk.html#tkinter.ttk.Radiobutton>`__
reference.

.. seealso::

   :doc:`Checkbutton <checkbutton>` for an independent on/off toggle, and
   :doc:`Combobox <combobox>` when a dropdown fits better than a visible group.
   Want to restyle the radiobutton yourself? The
   :ref:`radiobutton's styling options <radiobutton-styling>` (and the
   :ref:`toolbutton style <button-styling>` for the segmented look) and its
   companion :doc:`Custom styles </user-guide/feature-guides/custom-styles>`
   guide document the hand-styling surface.
