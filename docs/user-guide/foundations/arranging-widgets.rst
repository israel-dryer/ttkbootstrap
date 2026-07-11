Arranging widgets
=================

Creating a widget doesn't make it appear — a **geometry manager** has to place it
inside its parent first. tkinter has three, and you choose one per container based
on the shape of the layout:

- **grid** — rows and columns, like a table. The workhorse for forms and anything
  that lines up in two dimensions. Start here:
  :doc:`Layout with grid </user-guide/foundations/layout-with-grid>`.
- **pack** — stack widgets against a side. Ideal for toolbars, a column of
  controls, or a content area above a status bar:
  :doc:`Layout with pack </user-guide/foundations/layout-with-pack>`.
- **place** — exact coordinates, for overlays and the rare pixel-perfect case.
  You'll seldom need it; it's covered briefly on the pack page.

Two rules hold no matter which manager you use:

**One manager per container.** Don't mix ``grid`` and ``pack`` on children of the
*same* parent — they size things differently and tkinter will hang trying to
reconcile them.

**Nest frames to combine them.** Real windows are frames inside frames, each using
whichever manager fits that region — a toolbar packed along the top, a form
gridded inside the content area. Both tutorials build toward exactly that.

New here? Read :doc:`Layout with grid </user-guide/foundations/layout-with-grid>`
first — it's the manager you'll reach for most — then
:doc:`Layout with pack </user-guide/foundations/layout-with-pack>`.
