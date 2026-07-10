How styling is delivered
========================

.. note::

   This guide is being written for 2.0. It documents the single biggest change
   from 1.x.

In 1.x, ``import ttkbootstrap`` **monkey-patched tkinter** at import time so that
every ``ttk`` widget grew a ``bootstyle`` keyword. 2.0 stops doing that. The
styling API is now delivered through concrete subclasses, so widgets keep real
signatures and docstrings and importing the library mutates nothing.

This guide will cover:

- **Blessed widget subclasses.** ``ttk.Button``, ``ttk.Entry``, … are real
  subclasses that carry ``bootstyle=`` via
  :class:`~ttkbootstrap.BootMixin`; the legacy ``tk`` set
  (``Tk``/``Menu``/``Text``/``Canvas``/``TkFrame``/``TkLabel``/``LabelFrame``)
  auto-themes via :class:`~ttkbootstrap.AutoStyleMixin`.
- **Fluent geometry.** ``pack``/``grid``/``place`` return the widget, so
  ``ttk.Button(root, text="Save").pack()`` is one expression.
- **Styling widgets you didn't subclass.** ``bootify(cls)`` returns a
  bootstyle-enabled subclass of any third-party ttk class; ``apply_bootstyle
  (widget, style)`` styles one already-created vanilla widget.
- **Opting back into the global API.** ``enable_global_api()`` restores the 1.x
  behavior so *vanilla* ``tkinter``/``tkinter.ttk`` widgets accept ``bootstyle``
  and everything gains fluent geometry.
