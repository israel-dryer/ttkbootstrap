About
=====

ttkbootstrap is a theming extension for tkinter. It generates modern, flat,
Bootstrap-inspired themes on demand and adds a single ``bootstyle`` keyword to
the widgets you already use — so a standard tkinter app can look current without
a rewrite.

Beautiful, easy-to-use styles
-----------------------------

Creating ttk styles by hand is tedious. Between element layouts, state maps, and
image assets, a single good-looking submit button can mean adjusting a couple
dozen settings. ttkbootstrap takes that pain away: it ships a curated set of
light and dark themes with a Bootstrap-inspired palette, so you can spend your
time designing your application instead of hand-tuning widget styles.

Style with keywords
-------------------

Keep it simple. Set a widget's look with a keyword instead of a ttk style class.
Where plain ttk wants ``success.Horizontal.TProgressbar``, ttkbootstrap wants
``success`` — one semantic keyword that carries the same meaning on every widget:

.. code-block:: python

   ttk.Button(app, text="Save", bootstyle="success")
   ttk.Progressbar(app, bootstyle="success")
   ttk.Entry(app, bootstyle="success")

Anyone who has used Bootstrap for the web will recognize the idea: a small set of
semantic classes — ``primary``, ``success``, ``danger`` — that give you a
consistent, professional API for building quickly. I took the same approach here,
pre-defining styles for nearly every ttk widget and letting you reach them with
plain keywords.

In 2.0 that keyword language became a proper grammar. A ``bootstyle`` is a fixed
set of slots — a color, an optional modifier, a widget type, an optional
orientation — written with spaces: ``"primary outline"``, ``"success round
toggle"``, ``"info striped"``. The vocabulary is closed, so a typo now fails
loudly instead of silently doing nothing. See the
:doc:`bootstyle grammar </user-guide/foundations/bootstyle-grammar>` for the full
language.

Build only what you use
-----------------------

If you are not using a style, it should not be taking up memory in your app.
Nothing bloats an application like a pile of assets it may never touch.

So ttkbootstrap builds ttk styles and themes **on demand**. A style that is never
used is never created. To put that in perspective: in the old image-based
approach (ttkbootstrap 0.5), a single scale widget meant loading **288 images**
to cover every possible theme and color combination — that is simply how ttk
styles were traditionally handled. By 1.0, the on-demand engine cut that to the
three or four images the widget actually needs for its hover and pressed states.
Only what you use gets built.

2.0 rebuilt that engine again, this time for speed and memory over the whole life
of the app. Identical assets are now rendered exactly once and shared; switching
themes repaints only the widgets currently on screen — styles rebuild lazily, as
they are needed, rather than all at once — and the image references that used to
accumulate across theme switches are gone. Theme switching is fast, and it stays
fast.

A styling extension, not a widget library
-----------------------------------------

ttkbootstrap is deliberately a **styling layer for vanilla tkinter**, not a new
UI framework. The widgets are tkinter's widgets; ttkbootstrap themes them and
adds a handful of conveniences. Everything you already know about tkinter — the
geometry managers, variables, events, the widget tree — still applies, and the
:doc:`documentation </user-guide/index>` teaches it in that dialect rather than
sending you elsewhere.

That focus is a design choice. A richer, component-oriented framework is a
separate project (bootstack); ttkbootstrap stays small, dependency-light (only
Pillow, for image-based assets), and true to the library it extends.

What 2.0 brings
---------------

2.0 is a cleanup and consolidation release — not a grab-bag of new features, but
a sharper, more consistent version of the same idea:

- a normalized, keyword-first API, with the old import-time monkey-patch retired
  in favor of plain widget classes;
- the single canonical ``bootstyle`` grammar described above;
- a :doc:`semantic-anchor theme model </themes>` with a curated catalog of light
  and dark themes, surface elevation, and addressable color ramps;
- crisp, theme-following :doc:`icons </user-guide/feature-guides/icons>` rendered
  from a built-in icon font (``icon=``) — no image files to manage;
- a public toolkit that makes your own
  :doc:`custom styles and themes </user-guide/feature-guides/custom-styles>`
  straightforward;
- and a top-to-bottom documentation rewrite.

The through-line is the same as day one: make a standard tkinter app look good
with as little ceremony as possible.

----

ttkbootstrap is released under the :doc:`MIT License <license>`. Release notes for
every version are published on the
`GitHub releases page <https://github.com/israel-dryer/ttkbootstrap/releases>`_.

.. toctree::
   :hidden:

   Changelog <https://github.com/israel-dryer/ttkbootstrap/releases>
   license
