The widget model
================

Everything you put on screen is a **widget** — a button, a label, a frame — and
they all follow the same three rules: every widget lives in a **tree** under a
parent, every widget is configured through **options**, and ttk widgets carry a
set of **states**. Learn these once and every widget behaves predictably.

The widget tree
---------------

A widget's **first argument is its parent** (its *master*). The ``App`` root sits
at the top; frames and other containers nest under it; leaf widgets like buttons
and labels sit inside those. That parent-child chain is the widget tree:

.. code-block:: python

   import ttkbootstrap as ttk

   app = ttk.App()                       # the root
   toolbar = ttk.Frame(app)              # a container under the root
   ttk.Button(toolbar, text="Save")      # a button under the toolbar
   toolbar.pack()

The tree decides three things: where a widget can be *placed* (only inside its
parent — see :doc:`Arranging widgets </user-guide/foundations/arranging-widgets>`),
what it *inherits* (the theme, and options like a cursor), and its *lifetime* —
destroying a widget destroys everything under it. You can walk the tree with
``widget.master`` (the parent) and ``widget.winfo_children()`` (the children);
``winfo_class()`` reports the widget's Tk class (``"TButton"``). See
:doc:`Widget & screen info </reference/winfo>` for the full introspection set.

Options configure a widget
--------------------------

Every widget is customized through **options** — ``text``, ``width``, ``image``,
``cursor``, and so on. Set them as keyword arguments when you create the widget,
and read or change them afterward:

.. code-block:: python

   btn = ttk.Button(app, text="Save", width=12)   # set at creation

   btn.configure(text="Saved")     # change later (config is an alias)
   btn["width"] = 8                # index syntax does the same

   print(btn.cget("text"))         # read -> "Saved"
   print(btn["text"])              # read, index syntax -> "Saved"

``configure()`` with no arguments returns *every* option the widget supports —
a quick way to discover what you can set. For the full, per-widget option list,
each widget's page in the :doc:`Widgets catalog </widgets/index>` and the
:doc:`Widgets reference </reference/api/index>` are the place to look.

.. note::

   ``bootstyle`` is just another option. Everything you already know about
   setting options applies — ``ttk.Button(app, text="Save", bootstyle="success")``
   or ``btn.configure(bootstyle="success")``. That's the whole styling API; see
   :doc:`Styling with bootstyle </user-guide/foundations/bootstyle-grammar>`.

States (the ttk way)
--------------------

Coming from classic tkinter you might expect a ``state="disabled"`` option. **ttk
widgets work differently**: they carry a set of **state flags** —
``disabled``, ``active``, ``pressed``, ``focus``, ``selected``, ``readonly``,
``invalid`` — that you turn on and off. This is what lets a theme restyle a
widget per state automatically.

Set a flag with ``state([...])``, clear it by prefixing ``!``, and test one with
``instate([...])``:

.. code-block:: python

   btn.state(["disabled"])            # turn on: greys out, stops responding
   btn.state(["!disabled"])           # turn off: back to normal

   if btn.instate(["disabled"]):      # test a flag
       ...

The same flags drive both behavior *and* appearance, which is why you never
hand-color a disabled or focused widget — the theme already maps every state.

Putting it together
-------------------

A small tree, configured, with a state toggled:

.. code-block:: python

   import ttkbootstrap as ttk

   app = ttk.App(title="Widget model")

   panel = ttk.Frame(app, padding=10)
   panel.pack()

   name = ttk.Entry(panel, width=24)
   name.pack(pady=(0, 8))

   save = ttk.Button(panel, text="Save", bootstyle="success")
   save.pack()

   save.state(["disabled"])                 # start disabled
   name.bind("<KeyRelease>",
             lambda e: save.state(["!disabled" if name.get() else "disabled"]))

   app.mainloop()

.. admonition:: 📷 Screenshot (placeholder)
   :class: screenshot-placeholder

   The Save button in both states — greyed-out (disabled) with the entry empty,
   and solid green (enabled) once text is typed.

.. seealso::

   :doc:`How a tkinter app runs </user-guide/foundations/how-a-tkinter-app-runs>`
   for the loop that drives callbacks, and :doc:`Cursors </reference/cursors>` for
   the platform-dependent ``cursor`` option.
