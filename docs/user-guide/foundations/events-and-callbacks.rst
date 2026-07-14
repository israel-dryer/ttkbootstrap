Events & callbacks
==================

A tkinter app spends almost all its time idle inside ``mainloop()``, waiting.
Your code runs in response to **events** — a button click, a keypress, a window
resize, a theme change. You connect an event to a **callback** (a function to
run), most often with the ``command`` option or with ``bind``.

.. note::

   This page covers the essentials. For the full binding system — binding scope
   and bindtags, sharing and stopping bindings, and defining and dispatching your
   own events — see the :doc:`Events guide </user-guide/feature-guides/events>`.

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
``"<Motion>"``. The :doc:`Event reference </reference/events/index>` lists them
all.

``after`` — run code later
--------------------------

To run a callback after a delay, or to drive a timer, use ``after`` — the
loop-driven scheduler introduced in
:doc:`How a tkinter app runs </user-guide/foundations/how-a-tkinter-app-runs>`
(never ``time.sleep``, which freezes ``mainloop``):

.. code-block:: python

   app.after(2000, lambda: status.configure(text="Ready"))   # in 2 seconds

Virtual events
--------------

Some notifications aren't raw input but *named* higher-level events, written in
double angle brackets — ``<<ThemeChanged>>``, ``<<LocaleChanged>>``. You bind
them exactly like physical events. For example, recolor something you drew
yourself whenever the theme switches:

.. code-block:: python

   canvas.bind("<<ThemeChanged>>", lambda e: repaint(canvas))

You can also define and fire your **own** virtual events to decouple parts of an
app — see the :doc:`Events guide </user-guide/feature-guides/events>`.

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

   - :doc:`Events guide </user-guide/feature-guides/events>` — binding scope,
     stopping events, and dispatching your own.
   - :doc:`Event reference </reference/events/index>` — the complete catalog.
