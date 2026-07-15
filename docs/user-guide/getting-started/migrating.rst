Migrating to 2.0
================

ttkbootstrap 2.0 is a cleanup and consolidation release. It removes long-standing
cruft, standardizes the API, and overhauls the theme engine and docs — but it is
still the same styling extension for tkinter you already know. Most apps need only
a handful of small edits.

This guide sorts every change into four kinds so you can tell at a glance what
needs your attention:

- **Breaking** — existing code stops working and you must change it.
- **Deprecated** — the old form still works but prints a ``DeprecationWarning``;
  update it before 3.0, which removes it.
- **Notable** — behavior or appearance differs, but no code change is required.
- **New** — an optional addition. These are covered in the feature guides, not
  here; this page only lists them so you know they exist.

The fastest path is to run your app once: fix anything that errors (the breaking
changes), then turn on warnings to catch the deprecations::

   python -W once::DeprecationWarning your_app.py


Breaking changes
----------------

These require an edit. There are only a few, and most apps hit at most one or two.

Styling keywords need a ttkbootstrap widget
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Importing ttkbootstrap no longer reaches into tkinter and adds ``bootstyle=`` /
``autostyle=`` to *every* widget class in the process. Those keywords now belong to
ttkbootstrap's own widget classes — the ones you get from ``import ttkbootstrap as
ttk``.

If your code already looks like this, nothing changes:

.. code-block:: python

   import ttkbootstrap as ttk

   app = ttk.App()
   ttk.Button(app, text="Save", bootstyle="success").pack()

What breaks is passing the keyword to a **raw** ``tkinter`` widget after importing
ttkbootstrap:

.. code-block:: python

   import tkinter.ttk as ttk_native
   import ttkbootstrap                       # no longer patches tkinter

   ttk_native.Button(app, bootstyle="success")   # TclError: unknown option "-bootstyle"

You have three ways forward:

- **Use ttkbootstrap's widgets** — construct from ``ttk.Button``, ``ttk.Frame``,
  and so on. This is the recommended fix.
- **Opt the whole process back in** — call :func:`~ttkbootstrap.enable_global_api`
  once at startup to restore the global patch, so raw ``tkinter`` / ``ttk`` widgets
  accept the styling keywords again (it also makes ``pack``/``grid``/``place``
  return the widget everywhere).
- **Style one foreign class** — :func:`~ttkbootstrap.bootify` returns a styled
  subclass, and :func:`~ttkbootstrap.apply_bootstyle` styles an instance you already
  have.

One application root
~~~~~~~~~~~~~~~~~~~~~~

The style engine is a singleton bound to the first root window, so an app has one
application root. Creating a **second** ``ttk.App`` (or ``ttk.Window``) while the
first is still alive now raises ``RuntimeError`` instead of silently leaving the
second window unthemed.

Give every extra window a ``Toplevel``, which is what secondary windows are:

.. code-block:: python

   app = ttk.App()
   editor = ttk.Toplevel()         # attaches to the root; not a second App/Window

Creating one root after another (each destroyed before the next) is unaffected.

Removed import paths
~~~~~~~~~~~~~~~~~~~~~~

Five old top-level module paths are gone. The classes themselves are unchanged —
reach them from the top-level ``ttk`` namespace, the same way you reach every other
widget and dialog.

.. list-table::
   :header-rows: 1
   :widths: 50 50

   * - 1.x import
     - 2.0
   * - ``import ttkbootstrap.scrolled``
     - ``ttk.ScrolledText`` / ``ttk.ScrolledFrame``
   * - ``from ttkbootstrap.tableview import Tableview``
     - ``ttk.Tableview``
   * - ``from ttkbootstrap.toast import ToastNotification``
     - ``ttk.ToastNotification``
   * - ``from ttkbootstrap.tooltip import ToolTip``
     - ``ttk.ToolTip``
   * - ``from ttkbootstrap.dialogs.dialogs import Messagebox``
     - ``ttk.Messagebox`` / ``ttk.Querybox``

If you prefer explicit imports, the full paths still work too —
``from ttkbootstrap.widgets.tableview import Tableview`` and
``from ttkbootstrap.dialogs import Messagebox``.

Character-icon constants removed
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``ttkbootstrap.icons`` module of named character constants (``Emoji`` and
``Icon``) is removed. Those constants were just Unicode characters, and a character
only appears if the user's system font happens to include that glyph — so they were
never reliable across platforms, which is why the catalog is gone.

You can still use a literal character yourself if you want to — any widget accepts
``text=`` — with the same font-dependent caveat:

.. code-block:: python

   ttk.Label(app, text="🔔").pack()   # shows only where the system font has it

For an icon that renders the same everywhere and follows the theme, use ``icon=``
instead, which draws from a bundled Bootstrap Icons font:

.. code-block:: python

   ttk.Button(app, text="Add", icon="plus-lg", bootstyle="success").pack()

If you passed a character to ``ToastNotification(icon=...)``, give it a Bootstrap
Icons glyph name instead (for example ``icon="bell-fill"``).

Keyword-only constructors and renamed options
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The shipped widgets and dialogs were normalized to a consistent signature: options
are passed by keyword after the first positional argument, and multi-word option
names are ``snake_case``. Most option renames keep a deprecated alias that warns, so
they land in the deprecations list below — but two shapes cannot be shimmed and are
hard breaks:

- **Constructors are keyword-only** after the leading positional(s). Pass widget and
  window options by keyword — ``ttk.Window("Title", size=(800, 600))``, not a long
  positional argument list. Affects ``Window`` / ``Toplevel`` and the shipped
  widgets (``Meter``, ``DateEntry``, ``Floodgauge``, ``ScrolledText`` /
  ``ScrolledFrame``, ``LabeledScale``, ``ToolTip``, ``ToastNotification``).
- **Value-carrying widgets are DoubleVar-backed** (were ``IntVar``). ``Meter``,
  ``Floodgauge``, and ``LabeledScale`` now return a ``float`` from ``value`` /
  ``cget("value")`` where you previously got an ``int`` — fractional values are
  honored instead of truncated.

See the widget reference pages for each widget's final option names.

``get_date`` returns ``None`` when cancelled
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``Querybox.get_date`` (and the ``DateEntry`` calendar) previously always returned a
``date``, so a cancelled dialog was indistinguishable from a real pick. It now
returns ``None`` on cancel. Guard the result if you used it unconditionally:

.. code-block:: python

   picked = ttk.Querybox.get_date()
   if picked is not None:
       ...

The other ``Querybox.get_*`` methods likewise return ``None`` on cancel.


Deprecated (still works, warns)
-------------------------------

These keep working through the 2.x series and print a one-time
``DeprecationWarning`` naming the replacement. Update them at your leisure; they are
removed in 3.0.

- **Tuple and list bootstyle** — the canonical form is a single string.
  ``bootstyle=("primary", "outline")`` becomes ``bootstyle="primary outline"``. See
  :doc:`Styling with bootstyle </user-guide/foundations/bootstyle-grammar>`.
- **Legacy theme names** — ``"darkly"``, ``"cosmo"``, ``"litera"``, and the rest of
  the pre-2.0 Bootswatch names still work; naming one registers it on demand with a
  warning. See *Theme names changed* below.
- **Validation helpers** — the flat ``add_*_validation`` functions moved under a
  namespace: ``add_numeric_validation(w)`` becomes ``ttk.Validation.numeric(w)``.
  See :doc:`Validation </user-guide/feature-guides/validation>`.
- **Utility import paths** — ``ttkbootstrap.utility`` and ``ttkbootstrap.colorutils``
  are now the ``ttkbootstrap.utils`` package; the old paths forward with a warning.
  The helpers are also on ``ttk`` directly (``ttk.scale_size``,
  ``ttk.contrast_color``).
- **Window kwarg spellings** — ``hdpi`` → ``high_dpi``, ``overrideredirect`` →
  ``override_redirect``, ``windowtype`` → ``window_type``, ``toolwindow`` →
  ``tool_window`` on ``Window`` / ``Toplevel``.
- **Widget option spellings** — renamed options such as ``Meter``'s ``metersize`` →
  ``meter_size`` or ``DateEntry``'s ``startdate`` → ``start_date`` keep a warning
  alias.
- **ThemeDefinition selector** — ``themetype=`` → ``mode=`` (and ``.type`` →
  ``.mode``).
- **FloodgaugeLegacy** — ``FloodgaugeLegacy(...)`` warns on use; migrate to
  ``ttk.Floodgauge``.
- **The publisher module** — ``ttkbootstrap.publisher`` forwards to
  ``ttkbootstrap.internal.publisher`` with a warning (and see *Theme-change
  notifications* under Notable changes — the engine no longer fires it).


Notable changes
---------------

No code change is required for these, but the app looks or behaves differently than
it did in 1.x.

Theme names changed
~~~~~~~~~~~~~~~~~~~~~

The built-in catalog is now 15 curated **families**, each generating a matched
``-light`` and ``-dark`` pair (30 themes total), and the default theme is now
``bootstrap-light`` (was ``litera``). Prefer a curated name in new code:

.. code-block:: python

   app = ttk.App(theme="bootstrap-dark")

.. admonition:: Coming from 1.x
   :class: note

   Your existing ``App(themename="darkly")`` still works — naming a legacy theme
   registers it on demand with a warning. To register the whole pre-2.0 set at once
   (say, to list them in a theme picker), call
   :func:`~ttkbootstrap.install_legacy_themes`. Legacy themes keep their authored
   colors; only their inconsistent plumbing is regenerated. There is no one-to-one
   legacy-to-curated mapping (``darkly`` is not ``bootstrap-dark``), so pick a
   curated theme deliberately rather than expecting an automatic swap.

See :doc:`Theming & Colors </user-guide/feature-guides/theming>` for the theme model
and how to author your own.

Theme-change notifications
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Switching themes no longer notifies the old ``Publisher`` mechanism. If you
subscribed to it to rebuild something on a theme change, bind the standard Tk
``<<ThemeChanged>>`` virtual event instead, or register a callback with
:func:`~ttkbootstrap.on_theme_change`:

.. code-block:: python

   ttk.on_theme_change(lambda style: rebuild_my_chart(style))

Bare buttons are quiet by default
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A ``ttk.Button`` or ``ttk.Menubutton`` with no ``bootstyle`` now renders in a calm,
theme-adaptive ``neutral`` look instead of the ``primary`` accent — a plain button
is not a call to action. Add ``bootstyle="primary"`` to the buttons that should draw
attention, or restore the old default globally:

.. code-block:: python

   app = ttk.App(default_button="primary")

Appearance refinements
~~~~~~~~~~~~~~~~~~~~~~~~

2.0 regenerates each theme's palette from its accents for consistent contrast, and
restyles several widgets. You may notice: solid buttons gain a subtle hairline
border; scrollbars are restyled; an input shows its accent color on **focus** only,
not on hover; and the date picker opens as a frameless popover that dismisses on an
outside click or ``Escape``. None of these need a code change. Pin exact 1.x colors,
if you need them, by authoring your own theme.


New in 2.0
----------

Optional additions worth knowing about — each has a feature guide:

- **Light/dark mode toggle** — ``app.toggle_theme()`` and a settable
  ``app.theme_mode`` flip between a family's light and dark variants.
- **Fluent geometry** — ``pack``/``grid``/``place`` return the widget, so you can
  construct and place in one expression.
- **Themed icons** — ``icon=`` puts a theme-aware Bootstrap Icons glyph on a widget;
  ``icon_only=True`` makes a compact icon button. See
  :doc:`Icons </user-guide/feature-guides/icons>`.
- **Typography** — ``ttk.set_global_family("Inter")`` and the ``ttk.Fonts`` manager.
  See :doc:`Typography </user-guide/feature-guides/typography>`.
- **Localization** — ``ttk.L``, ``ttk.LocaleVar``, and ``ttk.set_locale`` for
  runtime language switching. See
  :doc:`Localization </user-guide/feature-guides/localization>`.
- **File dialogs** — ``ttk.Querybox.get_open_filename`` and friends, plus
  ``ttk.filedialog``. See :doc:`Dialogs </user-guide/feature-guides/dialogs>`.
- **Custom-style toolkit** — ``Assets``, ``El``/``layout``, and
  ``register_style`` for building your own styles. See
  :doc:`Custom styles </user-guide/feature-guides/custom-styles>`.


See also
--------

- :doc:`Styling with bootstyle </user-guide/foundations/bootstyle-grammar>` — the
  canonical string grammar that replaces tuples.
- :doc:`Theming & Colors </user-guide/feature-guides/theming>` — the new theme model
  and authoring your own.
- :doc:`The delivery model </user-guide/foundations/delivery-model>` — how the
  styling keywords reach widgets, and ``enable_global_api``.
