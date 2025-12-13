---
title: Widgets
icon: fontawesome/solid/cubes
---

# Widgets

ttkbootstrap v2 organizes widgets the way you build real desktop apps:

- **Controls**: the widgets you reach for every day (buttons, toggles, field controls).
- **Data Display**: show status and data (tables, meters, progress).
- **Feedback**: communicate with the user (tooltips, toasts, dialogs).
- **Layout**: compose screens (frames, panes, scrolling).
- **Views**: switch between screens (tabs and page stacks).
- **Menus**: command surfaces (menu buttons and context menus).
- **Tk Widgets**: low-level Tk/ttk widgets that remain available, with ttkbootstrap theming.

The goal is to make the most common things easy, while keeping everything **Tk-native** and compatible.

---

## Controls vs Tk Widgets

Many v2 widgets come in two “layers”:

### Controls (recommended for apps)
Controls add the pieces you usually need in a desktop UI:

- label + helper/error message
- validation hooks
- consistent spacing and layout
- theme-aware styling
- higher-level events and patterns

Examples: **TextEntry**, **NumericEntry**, **DateEntry**, **Form**.

### Tk Widgets (building blocks)
Tk Widgets are the classic `ttk` controls (e.g., `Entry`, `Spinbox`, `Combobox`).  
They’re still available and themed — but they don’t include the extra “field” UX.

Use them when you need the lowest-level component or you’re building your own composite.

---

## How to choose the right widget

- If you’re building a **form** → start with **TextEntry / NumericEntry / DateEntry / Form**
- If you’re building **tables or lists** → start with **TableView / TreeView**
- If you’re giving **feedback** → use **Toast** for non-blocking, **Dialogs** for decisions
- If the content can overflow → use **ScrollView** (or **ScrolledText** for text)

---

## Styling

Most widgets accept `bootstyle=` to apply intent and variants consistently.

Examples:

```python
ttk.Button(app, text="Primary", bootstyle="primary")
ttk.Button(app, text="Outline", bootstyle="primary-outline")
```

See the **Design → Variants & States** pages for the full token model.

---

## Images in widget docs

Widget pages use images for things that are hard to explain in text:

- default/hover/pressed/disabled states
- layout and spacing patterns
- dark mode vs light mode comparisons
- error/validation message presentation

Until you capture screenshots, use placeholders like:

> _Image placeholder:_  
> Screenshot of TextEntry showing helper text, and an invalid state message.

---

## Next steps

- Start with **Conventions** to learn how examples and pages are structured.
- Browse **Controls** to find the widgets you’ll use most often.
