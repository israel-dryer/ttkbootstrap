Typography
==========

Text in a tkinter app is styled through the **standard Tk named fonts** — a
handful of fonts (``TkDefaultFont``, ``TkTextFont``, ``TkFixedFont``, …) that
every interpreter ships and every widget reads by default. There is no separate
ttkbootstrap font vocabulary: change a named font and every widget that uses it
restyles at once. This guide covers the one-liner for the whole app, per-font
tweaks, and registering your own named fonts.

The named fonts
---------------

A **named font** is a font registered under a name in the interpreter. Widgets
reference it by that name rather than carrying their own copy, so reconfiguring
the name updates every widget that uses it — no interception, no per-widget
loop. These are the fonts ttkbootstrap manages:

.. list-table::
   :header-rows: 1
   :widths: 34 18 48

   * - Named font
     - Kind
     - Used by
   * - ``TkDefaultFont``
     - proportional
     - Most widgets — buttons, labels, entries; the general UI font.
   * - ``TkTextFont``
     - proportional
     - Text-entry widgets (``Entry``, ``Text``, ``Spinbox``).
   * - ``TkHeadingFont``
     - proportional
     - Column headings and other emphasis.
   * - ``TkMenuFont``
     - proportional
     - Menu items.
   * - ``TkCaptionFont`` / ``TkSmallCaptionFont``
     - proportional
     - Window and dialog captions.
   * - ``TkIconFont`` / ``TkTooltipFont``
     - proportional
     - Icon labels and tooltips.
   * - ``TkFixedFont``
     - monospace
     - Code and console-style text.

You can hand any of these to a widget's ``font=`` option directly — it works on
stock tkinter widgets too:

.. code-block:: python

   ttk.Label(app, text="Section", font="TkHeadingFont").pack()

.. note::

   Some named fonts (``TkTooltipFont``, ``TkIconFont``, ``TkSmallCaptionFont``)
   are absent on some platforms. The helpers below skip any that the current
   interpreter does not define, so you never have to guard for them yourself.

Setting the global family
-------------------------

The headline one-liner retints every proportional named font in a single call.
Because widgets read those fonts, it restyles the whole app:

.. code-block:: python

   import ttkbootstrap as ttk

   ttk.set_global_family("Segoe UI")

   app = ttk.App()
   ttk.Button(app, text="Save", bootstyle="primary").pack(padx=20, pady=20)
   app.mainloop()

:func:`~ttkbootstrap.set_global_family` rides the **deferred-config seam**: call
it at the top of a file *before* the root exists — as above — and the setting is
queued and applied when ``App()`` comes up. If a root already exists, it applies
live.

The monospace font (``TkFixedFont``) is left alone unless you ask for it with
``mono_family``:

.. code-block:: python

   ttk.set_global_family("Inter", mono_family="Cascadia Code")

.. admonition:: 📷 Screenshot (placeholder)
   :class: screenshot-placeholder

   The same small window rendered with the default family and with a custom
   ``set_global_family`` family side by side, showing the whole UI restyled.

Building a type system
----------------------

Past the global family, most apps want a few deliberate **roles** — a larger
heading, a smaller caption — and the named fonts are where you set them, once, at
startup. Use the :class:`~ttkbootstrap.Fonts` namespace, whose methods operate on
the live root, so call them after ``App()`` exists (a pre-root call raises a clear
"too early" error rather than spawning a stray root — for the top-of-file case use
the module-level ``set_global_family`` above).

**Adjust a built-in role.** ``Fonts.configure`` changes one named font in place —
``family``, ``size``, ``weight``, ``slant``, ``underline`` — and every widget
that reads it updates live. Bump the base size a point and make headings larger
and bold:

.. code-block:: python

   ttk.Fonts.configure("TkDefaultFont", size=11)
   ttk.Fonts.configure("TkHeadingFont", size=14, weight="bold")

   ttk.Label(app, text="Quarterly report", font="TkHeadingFont").pack()

Because widgets already read these names, that is a working type scale without
touching a single widget's ``font=``. (To retint the whole family live against an
existing root, ``Fonts.set_global_family(...)`` is the sibling of the
module-level call.)

**Define your own role.** When no built-in name maps to a role you need, register
one with ``Fonts.create_alias`` and refer to it by name everywhere — the same
mechanism the ``Tk*Font`` names use. Re-registering a name reconfigures it rather
than erroring, so it is safe to call at startup:

.. code-block:: python

   ttk.Fonts.create_alias("Caption", family="Georgia", size=9, slant="italic")

   ttk.Label(app, text="figure 1 — quarterly revenue", font="Caption").pack()

Define your fonts once and the rest of the code just names the role; restyle a
role later — a bigger caption, a different heading family — in that one place and
the whole app follows.

.. admonition:: 📷 Screenshot (placeholder)
   :class: screenshot-placeholder

   A small card using three roles — bold ``TkHeadingFont`` title, default body
   text, and the italic ``Caption`` alias — showing the type scale in one view.

**Seeing what the fonts are.** ``Fonts.names()`` lists the managed named fonts and
``Fonts.describe(name)`` returns a font's resolved family/size/weight (omit the
name for the whole mapping) — useful when a value isn't what you expect:

.. code-block:: python

   ttk.Fonts.describe("TkDefaultFont")
   # {'family': 'Segoe UI', 'size': 11, 'weight': 'normal', …}

``Fonts.reset`` drops ttkbootstrap's cached font wrappers; it runs automatically
when the app is destroyed, so you rarely call it yourself.

.. seealso::

   The named-font families are the standard tkinter fonts; for the underlying
   options and the ``font.Font`` object, see
   `tkinter.font <https://docs.python.org/3/library/tkinter.font.html>`__ on
   python.org.
