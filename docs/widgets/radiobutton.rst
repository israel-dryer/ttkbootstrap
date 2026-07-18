Radiobutton
===========

A **radiobutton** is one option in a mutually exclusive group — pick one and the
others clear. ``Radiobutton`` is the native ``ttk.Radiobutton``, styled with
``bootstyle=``. This page covers building a group, reacting to a choice, the
toolbutton look, then the ``bootstyle`` color and states.

.. image:: /_static/examples/radiobutton-hero-light.png
   :class: tb-screenshot-light
   :width: 297px
   :alt: A vertical radio group and a horizontal segmented toolbutton group — light theme

.. image:: /_static/examples/radiobutton-hero-dark.png
   :class: tb-screenshot-dark
   :width: 297px
   :alt: A vertical radio group and a horizontal segmented toolbutton group — dark theme

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

To run code when the user picks an option, pass ``command=`` — it fires when that
button is **invoked**: clicked, or activated with :kbd:`Space` while focused.

.. code-block:: python

   def on_choice():
       print("chose", size.get())

   ttk.Radiobutton(app, text="Small", variable=size, value="small", command=on_choice)

To react to the choice however it changes, trace the variable instead:

.. code-block:: python

   size.trace_add("write", lambda *_: print("size is now", size.get()))

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

.. image:: /_static/examples/radiobutton-toolbutton-light.png
   :class: tb-screenshot-light
   :width: 202px
   :alt: A three-segment toolbutton group with the middle option selected — light theme

.. image:: /_static/examples/radiobutton-toolbutton-dark.png
   :class: tb-screenshot-dark
   :width: 202px
   :alt: A three-segment toolbutton group with the middle option selected — dark theme

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

Reference
---------

``Radiobutton`` is the native ``ttk.Radiobutton``; ttkbootstrap adds only the
``bootstyle`` keyword.

- :doc:`Radiobutton API reference </reference/api/radiobutton>` — every option and
  method.
- :ref:`Radiobutton styling options <radiobutton-styling>` (and the
  :ref:`toolbutton style <button-styling>` for the segmented look) — restyle it
  yourself, with the :doc:`Custom styles </user-guide/feature-guides/custom-styles>`
  guide.

.. seealso::

   - :doc:`Checkbutton <checkbutton>` — an independent on/off toggle.
   - :doc:`Combobox <combobox>` — a dropdown when a visible group is too big.
