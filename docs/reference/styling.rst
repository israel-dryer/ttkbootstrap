Styling
=======

Styling in ttkbootstrap runs through one engine and reaches widgets three ways.
The ``Style`` engine owns the active theme and builds ttk styles on demand. The
shipped widgets carry the ``bootstyle`` keyword; to put that keyword on a widget
ttkbootstrap does not ship, use the delivery helpers below. And when a name in
the ``bootstyle`` vocabulary can't describe the look you want, the toolkit builds
a ttk style by hand. The :doc:`Custom styles
</user-guide/feature-guides/custom-styles>` guide shows the toolkit in use.

The style engine
----------------

``Style`` is a process-wide singleton, bound to the first application window and
reachable as its ``style`` attribute (or ``Style.get_instance()``). It holds the
theme definitions, switches the active theme, and exposes the current theme's
colors.

.. autoclass:: ttkbootstrap.Style
   :members:

Applying styles to any widget
-----------------------------

The widgets ttkbootstrap ships already accept ``bootstyle``. These helpers extend
that keyword to widgets it does not ship — a third-party ttk widget, or a plain
``tkinter.ttk`` widget you created yourself.

How much of the ``bootstyle`` vocabulary applies depends on the widget's ttk
class. A widget that keeps a standard ttk class (a subclass of ``ttk.Button``,
``ttk.Entry``, …) gets the full vocabulary and behaves exactly like the
corresponding ttkbootstrap widget. A widget with its own ttk class has no
ttkbootstrap style recipe: a bare color (``bootstyle="info"``) warns and leaves
the widget's style unchanged, and naming a base type explicitly
(``bootstyle="info-frame"``) borrows that standard recipe where the widget's
elements support it.

A composite widget's internals follow the active theme on their own —
standard-class children resolve against the per-theme base styles, so they
match every theme switch without any wrapping. The accent, however, is not
fanned out to them: which child should carry it is the widget's design, not
something a wrapper can infer. To accent a specific internal, call
``apply_bootstyle`` on that child.

.. autofunction:: ttkbootstrap.bootify

.. autofunction:: ttkbootstrap.apply_bootstyle

.. autofunction:: ttkbootstrap.enable_global_api

Building custom styles
----------------------

For a look ``bootstyle`` can't name, compose a ttk style from **assets**,
**elements**, a **state map**, and a **layout** — each a small toolkit call.
``Assets`` renders cached images, ``image_element`` turns one into a named ttk
element, ``state_map`` is a validated ``style.map``, and ``layout`` arranges the
elements into the widget's element tree and registers the style. See the
:doc:`Custom styles </user-guide/feature-guides/custom-styles>` guide for a
worked example.

.. autoclass:: ttkbootstrap.Assets
   :members:

.. autofunction:: ttkbootstrap.image_element

.. autofunction:: ttkbootstrap.state_map

.. autofunction:: ttkbootstrap.statespec

.. autofunction:: ttkbootstrap.layout

.. autoclass:: ttkbootstrap.El
   :members:
   :exclude-members: name, options, children

.. autofunction:: ttkbootstrap.register_style

.. autoclass:: ttkbootstrap.StyleName
   :members:
   :exclude-members: colorname, element, ttk_style

.. note::

   To render a glyph as an element in a custom layout, see
   :func:`~ttkbootstrap.icon_element` on the :doc:`Imaging <imaging>` page.

See also
--------

- :doc:`Custom styles </user-guide/feature-guides/custom-styles>` — how to build
  and apply your own styles, with examples.
- :doc:`Theming & Colors </user-guide/feature-guides/theming>` — the theme model
  behind the engine.
