# Windows

Tk applications are composed of one or more **windows**.
Understanding how windows behave — and how they interact with focus, modality,
and the event loop — is essential for building correct desktop applications
with ttkbootstrap.

This page explains window behavior at a platform level and how ttkbootstrap
expects windows to be used.

---

## Root window

Every Tk application has exactly one **root window**.

In Tkinter, this window is created when the root application object is instantiated.
All other windows exist within the context of this root.

The root window:
- owns the Tcl/Tk interpreter
- manages global state such as styles and images
- serves as the parent for all other windows

ttkbootstrap formalizes this role through the `App` object.

---

## Top-level windows

Additional windows are created using **toplevel windows**.

Top-level windows:
- are independent OS-level windows
- have their own title, size, and decorations
- share the same Tcl/Tk interpreter as the root

They are commonly used for:
- dialogs
- secondary views
- floating tool panels

---

## Window ownership

A toplevel window may be associated with a **parent window**.

Ownership affects:
- window stacking
- focus behavior
- minimization and restoration

Associating dialogs with a parent window improves user experience and
prevents windows from becoming lost behind others.

---

## Modality

A modal window restricts user interaction until it is dismissed.

In Tk, modality is implemented through a combination of:
- pointer and keyboard grabs
- focus management
- event waiting (`wait_window`, `wait_visibility`)

ttkbootstrap encourages explicit modal patterns rather than implicit blocking.

---

## Window lifetime

Windows have an explicit lifetime:

- created
- displayed
- hidden or destroyed

Destroying a window releases its resources.
Hidden windows still consume resources and retain state.

ttkbootstrap favors explicit destruction when windows are no longer needed.

---

## Focus and activation

Window focus determines where keyboard input is delivered.

Focus behavior depends on:
- window activation state
- platform window manager rules
- explicit focus calls

Correct focus handling is especially important for dialogs and forms.

---

## ttkbootstrap guidance on windows

ttkbootstrap promotes the following patterns:

- use a single root window per application
- associate dialogs with a parent window
- prefer local grabs over global grabs
- destroy windows explicitly when done

These patterns improve predictability and usability across platforms.

---

## Common pitfalls

- creating multiple root windows
- failing to set a dialog parent
- relying on global grabs unnecessarily
- leaking windows by hiding instead of destroying them

Understanding window behavior helps avoid these issues.

---

## Next steps

- See **Event Loop** for how window events are dispatched
- See **Widget Lifecycle** for creation and destruction timing
- See **Capabilities → Signals** for coordinating window state
