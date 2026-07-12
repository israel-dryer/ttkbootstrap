Every widget — native, tk, or ttkbootstrap — inherits a common set of methods
from tkinter for configuration, lifecycle, focus, and introspection. They work
the same on all of them, so they're documented once here rather than repeated on
each widget's page.

.. rubric:: Configuration

.. list-table::
   :widths: 32 68

   * - ``configure(**options)``
     - Set one or more options after creation (alias ``config``). Called with a
       single option name, returns that option's spec instead.
   * - ``cget(option)``
     - Return the current value of one option.
   * - ``keys()``
     - List the option names the widget accepts.

.. rubric:: Lifecycle

.. list-table::
   :widths: 32 68

   * - ``destroy()``
     - Remove the widget and all its children, releasing their resources.
   * - ``after(ms, func=None, *args)``
     - Schedule ``func`` to run once after ``ms`` milliseconds; returns an id.
       With no ``func``, just delays. See :doc:`Run background work
       </user-guide/how-to/threads>`.
   * - ``after_cancel(id)``
     - Cancel a callback previously scheduled with ``after``.
   * - ``after_idle(func, *args)``
     - Run ``func`` once the event loop is next idle.
   * - ``update_idletasks()``
     - Process pending geometry/redraw work without handling user events —
       the usual way to force a repaint mid-task.
   * - ``update()``
     - Process **all** pending events, including user input. Use sparingly; it
       can re-enter your callbacks.

.. rubric:: Focus

.. list-table::
   :widths: 32 68

   * - ``focus_set()``
     - Give this widget the keyboard focus when its window next has focus.
   * - ``focus_get()``
     - Return the widget that currently has focus, or ``None``.
   * - ``focus_force()``
     - Take focus immediately, even stealing it from another window (avoid
       unless necessary).

.. rubric:: Introspection (``winfo``)

The ``winfo_*`` family reports live facts about the widget — size, position,
mapping, hierarchy. A few of the common ones:

.. list-table::
   :widths: 32 68

   * - ``winfo_children()``
     - The list of child widgets.
   * - ``winfo_width()`` / ``winfo_height()``
     - The current size in pixels (valid once the widget is mapped and laid
       out; before that they report ``1``).
   * - ``winfo_reqwidth()`` / ``winfo_reqheight()``
     - The size the widget *requests* from its geometry manager.
   * - ``winfo_x()`` / ``winfo_y()``
     - Position relative to the parent, in pixels.
   * - ``winfo_rootx()`` / ``winfo_rooty()``
     - Position relative to the whole screen.
   * - ``winfo_ismapped()``
     - Whether the widget is currently shown on screen.
   * - ``winfo_exists()``
     - Whether the widget still exists (has not been destroyed).
   * - ``winfo_toplevel()``
     - The top-level window containing the widget.

.. rubric:: Geometry and events

Placing a widget (``pack``, ``grid``, ``place``) and binding events (``bind``,
``event_generate``) are also inherited, and are covered in depth elsewhere:

- Geometry — :doc:`Arranging widgets </user-guide/foundations/arranging-widgets>`
  (and the fluent ``.pack()``/``.grid()``/``.place()`` that return the widget).
- Events — the :doc:`Events guide </user-guide/feature-guides/events>` and the
  :doc:`Event reference </reference/events/index>`.

.. note::

   ttk widgets (Button, Entry, Combobox, Treeview, …) add ``state(statespec)``
   and ``instate(statespec)`` for their interaction states. The classic tk
   widgets here (Text, Canvas, Listbox, Menu) don't — they use a ``state``
   *option* via ``configure(state=…)`` where applicable.
