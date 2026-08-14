# ttkbootstrap 2.2.1 — notable changes

> The consolidated log of changes that alter behavior or appearance since
> **2.2.0**, each with **what** changed and **why**. Same role its predecessors
> (`2_2_changes.md`, `2_1_1_changes.md`, `2_0_breaking_changes.md`) played: kept
> in `development/` so it survives, and the source for this release's notes.
>
> Scope is **relative to 2.2.0**. A regression introduced *and* fixed inside this
> cycle never reached a user, so it belongs to the dev log in `CLAUDE.md`, not
> here.
>
> Legend: **API** = source-level break · **Visual** = appearance-only (no code
> change needed) · **New** = additive · **Fix** = something that did not work
> before now does.

## Index

Rows mirror the section headings below, in order.

| Area | Kind |
|---|---|
| **Menu bars no longer take the menu border color on Linux** | Fix |

There are **no API breaks**: nothing was removed, and no call that worked in
2.2.0 fails.

---

## Menu bars no longer take the menu border color on Linux  *(Fix)*

**What.** On Linux, an application menu bar could come up painted in the theme's
border color instead of the surface color — a gray bar across the top of the
window, with the menu labels sitting on it. It now stays the surface color, and
popup menus keep the themed 1px border they gained in 2.1.

**Who notices.** Linux/X11 users of an app with a menu bar
(`window.configure(menu=...)`), on a build that maps menu bars — CPython
**3.13.15** is the one this was found on. Windows and macOS were never
affected: both draw menu bars with native OS chrome, which the library does not
touch. Nothing about an app's own code decided this, so an app that looked
correct could start showing it purely from an interpreter upgrade.

**Why.** The border is drawn by putting the *menu* background in the border
color and every *entry* in the surface color: a popup's entries tile its whole
interior, so only the 1px strip is left showing. That trick is wrong for a menu
bar, whose entries cover only the left of the bar — the border color floods the
rest.

Popups and menu bars were told apart by waiting for `<Map>`. Tk displays a menu
bar through a *clone*, so historically the widget the library styles never
mapped and so never got painted. That held everywhere it was measured, but it is
a property of the build rather than a guarantee: under CPython 3.13.15 it does
map. Not a Tk version difference either — CI's 3.10 job does not map it on the
very same Tk 8.6.14.

A menu bar is now refused explicitly — the library asks whether the menu is
installed as a window's menu bar rather than inferring it from mapping — so the
behavior no longer depends on which Tk is underneath.
