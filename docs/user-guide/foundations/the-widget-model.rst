The widget model
================

Everything you put on screen is a **widget** — a button, a label, a frame — and
they all follow the same handful of rules: every widget lives in a **tree** under a
parent, is configured through **options**, carries a set of **states**, and moves
through a **lifecycle** you manage. Learn these once and every widget behaves
predictably.

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

ttk keeps the familiar classic-tkinter ``state="disabled"`` option as a shortcut,
but underneath, **every ttk widget carries a set of state flags** —
``disabled``, ``active``, ``pressed``, ``focus``, ``selected``, ``readonly``,
``invalid`` — that you turn on and off. This flag set is the real model: it is what
lets a theme restyle a widget per state automatically.

Set a flag with ``state([...])``, clear it by prefixing ``!``, and test one with
``instate([...])``:

.. code-block:: python

   btn.state(["disabled"])            # turn on: greys out, stops responding
   btn.state(["!disabled"])           # turn off: back to normal

   if btn.instate(["disabled"]):      # test a flag
       ...

The same flags drive both behavior *and* appearance, which is why you never
hand-color a disabled or focused widget — the theme already maps every state.

The ``state="disabled"`` option is a coarse shortcut over these flags: it
understands only ``normal``/``disabled`` (and ``readonly`` on entry-style
widgets), so ``state([...])`` is the way to reach the rest (``active``,
``pressed``, ``invalid``, …). One caveat that follows from this: ``cget("state")``
reports only what the *option* was last set to, not the live flags — so after
``widget.state(["disabled"])`` it can still read ``"normal"``. To ask whether a
flag is set, use ``instate([...])``, never ``cget("state")``.

Lifecycle
---------

A widget passes through three stages: it is **created**, **displayed**, and
eventually **destroyed**.

**Creating** a widget places it in the tree but does not draw it. It exists right
away — you can configure and query it — yet it stays invisible until a geometry
manager maps it onto the screen:

.. code-block:: python

   btn = ttk.Button(app, text="Save")   # exists now, but nothing is drawn
   btn.winfo_ismapped()                 # -> False
   btn.pack()                           # display it
   btn.winfo_ismapped()                 # -> True

That gap is deliberate — you build a whole subtree, then lay it out. It is also
why a widget's **master is fixed at creation**: you cannot reparent a widget later.
To move one, destroy it and rebuild it under the new parent.

**Destroying** a widget removes it for good with ``destroy()``. The call
**cascades** — destroying a container destroys every widget under it, so tearing
down a screen is a single call on its frame. Afterward the widget is gone and its
methods raise ``TclError``, so guard with ``winfo_exists()`` when a widget might
already be destroyed:

.. code-block:: python

   panel.destroy()            # removes the panel and all of its children
   panel.winfo_exists()       # -> False
   # panel.configure(...)     # would raise TclError: invalid command name

**Cleaning up.** ``destroy()`` frees the widget, but not the things you attached
*around* it — a repeating ``after`` timer, a variable ``trace``, a binding on
another widget. Those keep firing into a widget that no longer exists. Release them
as the widget is torn down; the ``<Destroy>`` event fires for exactly this:

.. code-block:: python

   job = app.after(1000, tick)                       # a repeating timer
   widget.bind("<Destroy>", lambda e: app.after_cancel(job))

You rarely write this by hand: ttkbootstrap's shipped widgets already release their
own timers and traces on destroy, and :doc:`on_close
</user-guide/getting-started/app-structures>` gives the whole app a place to shut
down cleanly. Reach for ``<Destroy>`` cleanup only for long-lived resources you
create yourself. See :doc:`Events & callbacks
</user-guide/feature-guides/events>` for ``after`` and traces in depth.

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

   - :doc:`How a tkinter app runs </user-guide/foundations/how-a-tkinter-app-runs>`
     — the loop that drives callbacks.
   - :doc:`Events & callbacks </user-guide/feature-guides/events>` — ``after``
     timers, variable traces, and the ``<Destroy>`` event.
   - :doc:`Cursors </reference/cursors>` — the platform-dependent ``cursor``
     option.
