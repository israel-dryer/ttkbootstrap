The bootstyle grammar
=====================

Every ttkbootstrap widget is styled through one keyword: ``bootstyle``. This
guide is the canonical reference for its grammar.

A ``bootstyle`` value is a single string of space-separated tokens in a fixed
slot order::

   [@surface] [color] [modifier] <base-type> [orient]

- **@surface** — the surface the control sits on: ``@card`` (a neutral raised
  panel) or an accent (``@primary`` …), so a ghost, outline, or link control
  blends on a card or an accent bar instead of only the window background.
  Optional and position-free.
- **color** — the semantic intent: ``primary``, ``secondary``, ``success``,
  ``info``, ``warning``, ``danger``, ``light``, ``dark``, ``neutral``.
- **modifier** — a variant such as ``outline``, ``link``, ``ghost``, ``round``,
  ``striped``.
- **base-type** — the widget family, usually inferred from the widget and
  spelled only for the chameleon families ``toggle`` / ``toolbutton``.
- **orient** — ``horizontal`` / ``vertical`` where applicable.

**Spaces are the recommended separator** —
``ttk.Button(bootstyle="@primary success ghost")``. Dashes
(``primary-success-ghost``) and any token order still parse, but spaces read
best and are what editor autocomplete suggests.

The parser is a tokenizer over a closed vocabulary: unknown tokens fail loudly
(a warning by default; ``set_bootstyle_strict(True)`` or
``TTKBOOTSTRAP_STRICT=1`` raises).

The full vocabulary and every registered widget family follow, generated from
the closed vocabulary and the builder registry.

.. include:: /_generated/bootstyle_reference.rst
