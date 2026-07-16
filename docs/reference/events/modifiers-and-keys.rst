Modifiers & keys
================

Modifiers
---------

A **modifier** requires a key or button to be held for the pattern to match.
Prefix it to the type: ``<Control-c>``, ``<Shift-Button-1>``,
``<Control-Alt-Delete>``.

.. list-table::
   :header-rows: 1
   :widths: 26 74

   * - Modifier
     - Requires
   * - ``Control``
     - The Control key.
   * - ``Shift``
     - The Shift key.
   * - ``Alt``
     - The Alt key. On some Linux keymaps Alt is a ``Mod`` modifier; if
       ``<Alt-…>`` does not match, try ``<Mod1-…>``.
   * - ``Lock``
     - Caps Lock to be on.
   * - ``Command``
     - The ⌘ Command key (macOS).
   * - ``Option``
     - The ⌥ Option key (macOS).
   * - | ``Meta``
       | ``M``
     - The Meta key (whichever ``Mod`` maps to it).
   * - | ``Mod1`` … ``Mod5``
       | ``M1`` … ``M5``
     - A numbered X modifier. Which physical key maps to which number is
       platform-dependent.
   * - | ``Button1`` … ``Button5``
       | ``B1`` … ``B5``
     - A mouse button held down — used with ``Motion`` for drags
       (``<B1-Motion>``).
   * - | ``Double``
       | ``Triple``
       | ``Quadruple``
     - The pattern to repeat 2 / 3 / 4 times in quick succession, close in time
       and space — ``<Double-Button-1>`` is a double-click.
   * - ``Extended``
     - The event to come from an extended key — numeric keypad, cursor cluster,
       right-hand Alt/Control (Windows).

Key symbols
-----------

For a key event, the **detail** is a *key symbol* (keysym) — a name for the key.
A printable key is its own symbol (``a``, ``A``, ``1``, ``space`` for the space
bar). Non-printing keys have names:

.. list-table::
   :header-rows: 1
   :widths: 30 35 35

   * - Key
     - Symbol
     - Pattern
   * - Enter / Return
     - ``Return``
     - ``<Return>``
   * - Escape
     - ``Escape``
     - ``<Escape>``
   * - Tab
     - ``Tab``
     - ``<Tab>``
   * - Backspace
     - ``BackSpace``
     - ``<BackSpace>``
   * - Delete
     - ``Delete``
     - ``<Delete>``
   * - Insert
     - ``Insert``
     - ``<Insert>``
   * - Space
     - ``space``
     - ``<space>``
   * - Arrows
     - ``Up`` ``Down`` ``Left`` ``Right``
     - ``<Up>``
   * - Home / End
     - ``Home`` ``End``
     - ``<Home>``
   * - Page Up / Down
     - ``Prior`` ``Next``
     - ``<Prior>``
   * - Function keys
     - ``F1`` … ``F12``
     - ``<F1>``

.. tip::

   To discover any key's symbol, bind ``<KeyPress>`` and print ``event.keysym``
   (the key name) or ``event.char`` (the character it produced). See
   :doc:`The event object <event-object>`.
