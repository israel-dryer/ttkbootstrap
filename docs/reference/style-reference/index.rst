Style Reference
===============

.. note::

   The Style Reference is **generated** from live ttk introspection by an
   offline ``tools/`` step that emits committed rST (the same approach as the
   ``bootstyle`` reference table). It is being built in a later documentation
   slice.

For each native ttk widget family, this reference will document the exact
hand-styling surface:

- **bootstyle → ttk style name** — e.g. ``primary-outline`` →
  ``primary.Outline.TButton``.
- **Layout (elements)** — the element tree the widget is drawn from.
- **Configurable options** — ``background``, ``foreground``, ``bordercolor``,
  ``relief``, and the rest.
- **Supported states** — ``active``, ``pressed``, ``disabled``, ``focus``.
- **Hand-styling example** — ``style.configure(...)`` plus a widget using it.

This is the deep reference the :doc:`Widgets catalog </widgets/index>` links to
for native widgets.
