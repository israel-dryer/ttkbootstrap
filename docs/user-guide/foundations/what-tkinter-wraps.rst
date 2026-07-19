What tkinter wraps
==================

tkinter is not a GUI toolkit. It is a thin Python layer over one: **Tcl/Tk**, a
toolkit written in another language, with its own conventions. When you import
tkinter, a Tcl interpreter starts up inside your process, and every widget you
create becomes a command sent to it.

You never have to write Tcl, and this page will not teach it. But the seam
shows — in the names widgets carry, in the values you read back, and above all in
the error messages, which arrive in Tk's words rather than Python's. Once you can
see the seam, the parts of tkinter that look arbitrary stop being arbitrary.

A widget is a command with a path name
--------------------------------------

Tk identifies each widget by a **path name**: a dotted string spelling out its
position in the tree, exactly like a filesystem path. The root is ``.``, and each
child appends its own name. That is what ``str(widget)`` gives you:

.. code-block:: python

   app = ttk.App()
   toolbar = ttk.Frame(app)
   save = ttk.Button(toolbar, text="Save")

   str(save)          # '.!frame.!button'

Those ``!``-prefixed names are just what tkinter auto-generates when you don't
name a widget yourself. The path is not decoration — in Tcl the widget *is* a
command with that name, and your Python method calls are relayed to it:

.. code-block:: python

   save.cget("text")                          # 'Save'  -- the Python way
   app.tk.call(str(save), "cget", "-text")    # 'Save'  -- the same call, in Tcl

This one fact explains a family of error messages. Destroying a widget deletes
its command, so *using* the widget afterward isn't a Python error about a missing
attribute — it's Tcl telling you there is no such command:

.. code-block:: python

   save.destroy()
   save.cget("text")     # TclError: invalid command name ".!frame.!button"

Options carry a leading dash
----------------------------

In Tcl, options are written ``-text``, ``-width``. tkinter lets you write them as
Python keywords and adds the dash on the way through. It does not take it off
again on the way back, which is why the dash appears in errors for options you
wrote without one:

.. code-block:: python

   save.configure(text="Saved")       # you write this
   save.cget("nope")                  # TclError: unknown option "-nope"

Values are Tcl's, not Python's
------------------------------

Tcl's values are strings first, coerced as needed, and its idea of truth is
broader than Python's: ``"yes"``, ``"true"``, ``"1"`` and ``"on"`` are all true.
Values you read back come from Tk, so their types are Tk's — see
:ref:`What comes back <widget-model-what-comes-back>` in the widget model. When
you need to convert one, use the helpers that apply Tk's rules rather than
Python's, because ``"0"`` and ``"false"`` are non-empty strings and therefore
truthy to Python:

.. code-block:: python

   app.getboolean("no")     # False   -- bool("no") would be True

A variable is a named Tcl variable
----------------------------------

``StringVar`` and friends don't hold your value in Python. Each one creates a
variable *inside the interpreter* and holds its name:

.. code-block:: python

   name = ttk.StringVar(value="Ada")
   str(name)                  # 'PY_VAR0'

The widget and the variable are linked through that name, which is how a
``textvariable`` keeps an entry and your value in step without any code of yours
running. It also explains the classic footgun: let the Python object be garbage
collected and the Tcl variable goes with it, while the widget keeps pointing at a
name that no longer exists. See
:doc:`Object lifetime </user-guide/foundations/object-lifetime>`.

A callback is a registered command
----------------------------------

Tcl can't call a Python function directly. When you pass ``command=``, tkinter
registers your function as a Tcl command and hands Tk *that name*. Ask for it
back and the name is what you get:

.. code-block:: python

   save.configure(command=my_handler)
   save.cget("command")       # '...my_handler'  -- a Tcl command name

So ``cget`` is no way to recover a callback or a variable. Keep your own
reference to anything you need later.

Reading a TclError
------------------

``TclError`` is the interpreter reporting a problem in its own vocabulary. The
wording is Tk's, so it names Tcl things — commands, paths, dashed options — and
knowing the four seams above is usually enough to translate:

.. list-table::
   :header-rows: 1
   :widths: 46 54

   * - Message
     - What it means
   * - ``unknown option "-nope"``
     - The widget has no such option. You wrote ``nope``; the dash is Tcl's.
   * - | ``invalid command name ".!button"``
       | ``bad window path name ".!toplevel"``
     - The widget was destroyed — its command no longer exists. Guard with
       ``winfo_exists()`` if it might be gone.
   * - ``expected integer but got "abc"``
     - A value couldn't be coerced — often an ``IntVar`` read while the entry
       bound to it holds half-typed text.
   * - ``CLIPBOARD selection doesn't exist``
     - Nothing to read: the clipboard is empty or holds non-text.

:doc:`Handle callback errors </user-guide/how-to/error-handling>` covers catching
these.

One interpreter, one thread
---------------------------

The interpreter belongs to the thread that created it. That is the real reason
for the rule in :doc:`Run background work </user-guide/how-to/threads>`: a worker
thread must not touch widgets, because the interpreter they live in isn't
running there.

Reaching past tkinter
---------------------

``app.tk.call(...)`` sends a command straight to the interpreter, as the second
example on this page did. You should almost never need it — if a Tk feature has a
tkinter method, use the method. It's worth recognizing because you will meet it
in older code and in answers online, usually reaching for something tkinter
hadn't wrapped yet.

.. seealso::

   - :doc:`The widget model </user-guide/foundations/the-widget-model>` — the
     tree, options, and what reading one gives back.
   - :doc:`Object lifetime </user-guide/foundations/object-lifetime>` — the
     lifetime rule that follows from this seam: variables, images, and fonts.
   - :doc:`Variables guide </user-guide/feature-guides/variables>` — the named
     variables this page describes, and the one-owning-reference rule.
   - :doc:`Handle callback errors </user-guide/how-to/error-handling>` — catching
     ``TclError`` where it's expected.

Reference
---------

- :doc:`Interpreter </reference/capabilities/interpreter>` — the value-conversion
  helpers, ``register``, and the Tk version.
