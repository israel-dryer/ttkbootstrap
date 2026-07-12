.. rubric:: Configuration

.. list-table::
   :widths: 32 68

   * - ``configure(**options)``
     - Set one or more options after creation (alias ``config``). Called with a
       single option name, returns that option's spec.
   * - ``cget(option)``
     - Return the current value of one option.
   * - ``keys()``
     - List the option names the widget accepts.

.. rubric:: Geometry (placement)

Three managers place a widget in its parent. Each has a ``*_configure`` alias, a
``*_forget`` to unmap, and a ``*_info`` to read the settings back; in
ttkbootstrap ``pack``/``grid``/``place`` also return the widget. Choosing and
using them is covered in
:doc:`Arranging widgets </user-guide/foundations/arranging-widgets>`.

.. list-table::
   :widths: 32 68

   * - | ``pack(**options)``
       | ``pack_forget()``
       | ``pack_info()``
     - Stack the widget against a side of its parent.
   * - | ``grid(**options)``
       | ``grid_forget()``
       | ``grid_info()``
     - Place the widget in a row/column grid.
   * - | ``place(**options)``
       | ``place_forget()``
       | ``place_info()``
     - Position the widget by absolute or relative coordinates.
   * - ``winfo_manager()``
     - The name of the manager currently handling the widget (``"pack"``,
       ``"grid"``, ``"place"``, or ``""``).

.. rubric:: Events

Attach behavior to input. The event **sequence** syntax (``"<Button-1>"``,
``"<KeyPress-a>"``, virtual events like ``"<<Copy>>"``) and the callback's event
object are documented in the :doc:`Event reference </reference/events/index>`.

.. list-table::
   :widths: 32 68

   * - ``bind(sequence, func, add=None)``
     - Run ``func`` when ``sequence`` occurs on this widget. ``add="+"`` adds a
       handler instead of replacing.
   * - ``unbind(sequence, funcid=None)``
     - Remove a binding from this widget.
   * - | ``bind_class(name, sequence, func)``
       | ``unbind_class(name, sequence)``
     - Bind (or unbind) for every widget of a class rather than one instance.
   * - | ``bind_all(sequence, func)``
       | ``unbind_all(sequence)``
     - Bind (or unbind) application-wide.
   * - ``bindtags(tags=None)``
     - Get or set the ordered list of tags that decides which bindings fire.
   * - ``event_generate(sequence, **kw)``
     - Synthesize an event (real or virtual) as if it had happened.
   * - | ``event_add(virtual, *sequences)``
       | ``event_delete(virtual, *sequences)``
     - Define or remove the physical sequences that trigger a virtual event.

.. rubric:: Lifecycle and scheduling

.. list-table::
   :widths: 32 68

   * - ``destroy()``
     - Remove the widget and all its children, releasing their resources.
   * - ``after(ms, func=None, *args)``
     - Schedule ``func`` after ``ms`` milliseconds; returns an id. See
       :doc:`Run background work </user-guide/how-to/threads>`.
   * - ``after_cancel(id)``
     - Cancel a scheduled ``after`` callback.
   * - ``after_idle(func, *args)``
     - Run ``func`` once the event loop is next idle.
   * - ``update_idletasks()``
     - Process pending geometry/redraw work without handling user events — the
       usual way to force a repaint mid-task.
   * - ``update()``
     - Process **all** pending events, including user input. Use sparingly; it
       can re-enter your callbacks.
   * - | ``wait_variable(var)``
       | ``wait_window(window)``
       | ``wait_visibility(widget)``
     - Block locally until a variable changes, a window is destroyed, or a
       widget becomes visible (used to make a dialog modal).

.. rubric:: Focus and traversal

.. list-table::
   :widths: 32 68

   * - ``focus_set()``
     - Give this widget the keyboard focus when its window next has focus.
   * - ``focus_get()``
     - The widget that currently has focus, or ``None``.
   * - ``focus_force()``
     - Take focus immediately, even from another window (avoid unless
       necessary).
   * - | ``focus_displayof()``
       | ``focus_lastfor()``
     - The focused widget on this display; the widget that would get focus if
       this toplevel regained it.
   * - | ``tk_focusNext()``
       | ``tk_focusPrev()``
     - The next / previous widget in tab-traversal order.

.. rubric:: Stacking order

.. list-table::
   :widths: 32 68

   * - ``lift(aboveThis=None)``
     - Raise the widget above its siblings (or above a specific one). Alias
       ``tkraise``.
   * - ``lower(belowThis=None)``
     - Lower the widget below its siblings (or below a specific one).

.. rubric:: Modal grab

.. list-table::
   :widths: 32 68

   * - | ``grab_set()``
       | ``grab_set_global()``
     - Route all (application- or screen-wide) events to this widget — the basis
       of a modal dialog.
   * - ``grab_release()``
     - Release a grab.
   * - | ``grab_current()``
       | ``grab_status()``
     - The widget currently holding the grab; this widget's grab state.

.. rubric:: Clipboard and selection

.. list-table::
   :widths: 32 68

   * - | ``clipboard_clear()``
       | ``clipboard_append(text)``
     - Clear, then add text to, the system clipboard. See
       :doc:`Copy to the clipboard </user-guide/how-to/clipboard>`.
   * - ``clipboard_get()``
     - Return the clipboard's current text (raises if empty).
   * - | ``selection_get(**kw)``
       | ``selection_clear(**kw)``
     - Read or clear the current X selection.
   * - ``bell()``
     - Ring the system bell.

.. rubric:: Introspection

The ``winfo_*`` family reports live facts about the widget — the common ones are
below; the full set is in :doc:`Widget & screen info </reference/winfo>`.

.. list-table::
   :widths: 32 68

   * - ``winfo_children()``
     - The list of child widgets.
   * - | ``winfo_width()``
       | ``winfo_height()``
     - The current size in pixels (valid once mapped and laid out; ``1`` before
       that).
   * - | ``winfo_reqwidth()``
       | ``winfo_reqheight()``
     - The size the widget *requests* from its geometry manager.
   * - | ``winfo_x()``
       | ``winfo_y()``
     - Position relative to the parent, in pixels.
   * - | ``winfo_rootx()``
       | ``winfo_rooty()``
     - Position relative to the whole screen.
   * - ``winfo_pointerxy()``
     - The mouse pointer's position, relative to the screen.
   * - | ``winfo_ismapped()``
       | ``winfo_viewable()``
     - Whether the widget is placed; whether it is actually visible on screen.
   * - ``winfo_exists()``
     - Whether the widget still exists (has not been destroyed).
   * - ``winfo_class()``
     - The widget's Tk class name.
   * - ``winfo_toplevel()``
     - The top-level window containing the widget.
   * - ``winfo_geometry()``
     - The widget's geometry string, ``"widthxheight+x+y"``.
   * - ``winfo_containing(x, y)``
     - The widget at a screen coordinate.

.. note::

   ttk widgets (Button, Entry, Combobox, Treeview, …) add ``state(statespec)``
   and ``instate(statespec)`` for their interaction states. The classic tk
   widgets (Text, Canvas, Listbox, Menu) don't — they use a ``state`` *option*
   via ``configure(state=…)`` where applicable.
