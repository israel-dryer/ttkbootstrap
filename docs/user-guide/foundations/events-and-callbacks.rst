Events & callbacks
==================

A tkinter app spends almost all its time idle inside ``mainloop()``, waiting.
Your code runs in response to **events** — a button click, a keypress, a window
resize, a theme change. You connect an event to a **callback** (a function to
run) in one of three ways, from most to least specific: the ``command`` option,
``bind``, and virtual events.

``command`` — the built-in action
---------------------------------

Buttons, checkbuttons, and similar controls take a ``command`` option: a
callable to run when the widget is activated. This is the common case:

.. code-block:: python

   def save():
       print("saved")

   ttk.Button(app, text="Save", command=save, bootstyle="primary").pack()

``command`` takes the function itself — ``command=save``, not ``command=save()``
(the second calls it immediately and passes the result). To pass arguments, wrap
it in a ``lambda``:

.. code-block:: python

   ttk.Button(app, text="Delete", command=lambda: delete(item_id)).pack()

``bind`` — any event, any widget
--------------------------------

For events without a ``command`` option — mouse motion, individual keystrokes,
focus changes — use ``bind``. You give it an **event pattern** and a callback
that receives an **event object** describing what happened:

.. code-block:: python

   entry = ttk.Entry(app)
   entry.pack()

   def on_return(event):
       print("submitted:", event.widget.get())

   entry.bind("<Return>", on_return)

The callback takes one argument, the event. Its most useful attributes are
``event.widget`` (the widget the event fired on), ``event.x``/``event.y`` (cursor
position), and ``event.keysym`` (the key name). Common patterns include
``"<Button-1>"`` (left click), ``"<Double-Button-1>"``, ``"<KeyPress>"``, and
``"<Motion>"``.

Binding scope
-------------

``widget.bind`` attaches a callback to *one widget*. But every event actually
consults **four levels** of bindings in turn, and understanding them is what lets
you write shortcuts and shared behavior instead of wiring every widget by hand:

- **Instance** — ``widget.bind(pattern, callback)`` — this one widget only.
- **Class** — ``widget.bind_class("TEntry", pattern, callback)`` — every widget
  of that Tk class at once. This is the level a widget's *default* behavior lives
  at (what makes an ``Entry`` insert the character you type).
- **Toplevel** — bindings on the containing window, seen by any widget in it.
- **Application** — ``widget.bind_all(pattern, callback)`` — every widget in the
  program. The right tool for a global shortcut like ``<F1>`` or ``<Control-q>``.

A widget's class name for ``bind_class`` is ``widget.winfo_class()`` —
``"TEntry"``, ``"TButton"``, ``"Text"``, and so on.

The order events travel
~~~~~~~~~~~~~~~~~~~~~~~~~

When an event fires, tkinter walks those four levels **in order** and runs
*every* matching binding it finds. That order is the widget's **bindtags**:

.. code-block:: python

   entry.bindtags()
   # ('.!entry', 'TEntry', '.', 'all')
   #   instance    class   toplevel  application

Two consequences worth internalizing:

- Your **instance** binding runs *before* the **class** binding — which is why
  returning ``"break"`` from it can pre-empt the widget's default behavior (see
  `Stopping an event`_).
- A matching binding at *any* level fires, so one ``bind_all("<F1>", …)`` covers
  the whole application.

You can reorder or insert tags with ``widget.bindtags((...))`` for advanced
cases, but the default order serves almost everything.

Adding vs replacing
~~~~~~~~~~~~~~~~~~~~~

Within a single tag, binding a pattern **replaces** whatever callback was already
bound to that same pattern — a real footgun when two parts of your code each
assume they own the event:

.. code-block:: python

   widget.bind("<Button-1>", first)
   widget.bind("<Button-1>", second)             # first is silently gone
   widget.bind("<Button-1>", third, add="+")     # third runs alongside second

Pass ``add="+"`` to **add** a callback instead of replacing it; every bound
callback then fires, in the order added. Reach for it whenever a handler should
coexist with others — especially the app-wide events under `Generating events`_,
where each consumer must add its own handler without clobbering the rest.

``bind`` returns an id that ``unbind`` uses to remove a single callback again:

.. code-block:: python

   handler_id = widget.bind("<Motion>", track)
   widget.unbind("<Motion>", handler_id)

Stopping an event
-----------------

A widget's *class* binding implements its default behavior — a ``Text`` widget
inserting the character you typed, for instance. Because the instance binding
runs first, returning the string ``"break"`` from your callback halts the chain,
so the class binding never runs and the default is suppressed:

.. code-block:: python

   def tab_moves_focus(event):
       event.widget.tk_focusNext().focus()
       return "break"        # stop Text from inserting a literal tab

   text.bind("<Tab>", tab_moves_focus)

Virtual events
--------------

**Virtual events** are named, higher-level notifications written in double angle
brackets, ``<<Like this>>``. They fire when something meaningful happens rather
than for a raw input, and you bind them exactly like physical events.
ttkbootstrap emits two you will use:

- ``<<ThemeChanged>>`` — fires on every widget after the theme is switched. Bind
  it to recolor anything you drew yourself (a ``Canvas``, a custom asset):

  .. code-block:: python

     canvas.bind("<<ThemeChanged>>", lambda e: repaint(canvas))

- ``<<LocaleChanged>>`` — fires when the app's locale changes; this is what
  drives :class:`~ttkbootstrap.LocaleVar` (see
  :doc:`State & variables <state-and-variables>`).

.. admonition:: Prefer the callback helpers for theme changes

   For rebuilding a **custom style** after a theme switch, ttkbootstrap offers
   :func:`~ttkbootstrap.on_theme_change` and the ``@theme_aware`` decorator,
   which are easier than a raw ``<<ThemeChanged>>`` binding. See
   :doc:`Make your own style </user-guide/concepts/make-your-own-style>`.

Generating events
-----------------

You can fire an event yourself with ``event_generate`` — most usefully your own
**virtual events**. A virtual event lets one part of an app announce that
something happened without knowing who cares: a producer generates it, and any
number of consumers bind to it. That decouples components cleanly.

.. code-block:: python

   # a producer announces on the root — it calls no one directly
   def load_data():
       ...  # do the work
       app.event_generate("<<DataLoaded>>")

   # consumers register on the SAME widget, each with add="+" so they stack
   app.bind("<<DataLoaded>>", lambda e: status.configure(text="Loaded"), add="+")
   app.bind("<<DataLoaded>>", lambda e: table.refresh(), add="+")

The name in double brackets is all you need — a ``<<virtual>>`` event works the
moment you bind and generate it.

.. important::

   ``event_generate`` dispatches to **one** widget (and its ``bindtags``); it
   does not broadcast. Bind consumers on the same widget you generate on — the
   root makes a natural app-wide bus — or use ``bind_all`` for a truly global
   signal. Use ``add="+"`` so each consumer adds a handler rather than replacing
   the previous one.

To make a virtual event fire from the keyboard too, alias it to physical key
sequences with ``event_add``:

.. code-block:: python

   app.event_add("<<Save>>", "<Control-s>", "<Control-S>")
   app.bind("<<Save>>", lambda e: save())   # Ctrl-S now fires <<Save>>

.. note::

   ``event_generate`` accepts ``data="…"``, but tkinter does not surface it on
   the event the callback receives, so it cannot be read back. To pass
   information with a virtual event, store it where both sides can reach it. See
   :doc:`the event object </reference/events/event-object>`.

``after`` — scheduling a callback
---------------------------------

A callback can also be scheduled to run *later*, without blocking, with
``after`` — the loop-driven timer introduced in
:doc:`How a tkinter app runs </user-guide/foundations/how-a-tkinter-app-runs>`
(the tool for delays, polling, and animation; never ``time.sleep``, which
freezes ``mainloop``).

One event-specific caution worth its own note: a **repeating** ``after`` timer
keeps firing even after the widget it updates is destroyed, and then errors on
the dead widget. Keep the job id and cancel it when the widget goes away — a
``<Destroy>`` binding is the natural place:

.. code-block:: python

   job = app.after(1000, tick)
   widget.bind("<Destroy>", lambda e: app.after_cancel(job))

A worked example
----------------

A ``command`` starts a countdown that drives itself with ``after`` and updates a
label — no blocking, the window stays responsive throughout:

.. code-block:: python

   import ttkbootstrap as ttk

   app = ttk.App(title="Countdown")

   label = ttk.Label(app, text="10", font=("", 48), bootstyle="primary")
   label.pack(padx=40, pady=(20, 10))

   def countdown(n):
       label.configure(text=str(n))
       if n > 0:
           app.after(1000, countdown, n - 1)   # extra args are passed to the callback

   ttk.Button(app, text="Start", bootstyle="success",
              command=lambda: countdown(10)).pack(pady=(0, 20))

   app.mainloop()

.. seealso::

   For the complete catalog — every event type, modifier, key symbol, event
   attribute, and ``event_generate`` option — see the
   :doc:`Event reference </reference/events/index>`.
