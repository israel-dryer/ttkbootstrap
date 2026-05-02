# Widgets

The **Widgets** section documents every UI control ttkbootstrap ships
— from foundational primitives (`Entry`, `Canvas`, `Text`) to themed
wrappers over `ttk` (`Button`, `Frame`, `Notebook`) to higher-level
composites that bundle layout, validation, and data binding into a
single class (`TextEntry`, `TableView`, `AppShell`).

Each page is written to a category-specific template — most are
**spec pages**: a quick example, a mental-model section, a curated
options table, observable behavior, events, and a cross-linked
recommendation block at the bottom. Architectural decisions
(theming, state, signals, layout) live one section over in
[Capabilities](../capabilities/index.md); the substrate they sit on
top of (event loop, geometry managers, ttk styling internals) lives
in [Platform](../platform/index.md).

---

## Widgets vs primitives vs API reference

These three places describe the same widgets at different
resolutions:

- **Widgets** — narrative spec pages with examples, common-options
  tables, behavior notes, and gotchas. Read these first.
- **Primitives** — the small group of pages under
  [Primitives](primitives/canvas.md) that document raw `tk.Canvas`
  / `tk.Text` / `ttk.Entry` / `ttk.Combobox` / `ttk.Spinbox`
  surfaces. Composites (TextEntry, ScrolledText, SelectBox,
  Tableview) build on these; reach for the primitive only when the
  composite is the wrong abstraction.
- **API Reference** — the auto-generated [class signatures and
  attribute lists](../reference/widgets/index.md) rendered from
  source docstrings. Read these for exact kwargs, return types,
  and full method enumeration.

Most of the time a Widgets page tells you everything you need; the
API reference is the secondary lookup when you need a specific
parameter shape.

---

## When to read this section

Reach for Widgets pages when you want to know:

- **Which widget fits a given UX pattern** — start with the
  category that matches the *intent* (a button is an *action*; a
  text input is an *input*; a dialog is a *modal flow*).
- **What an existing widget can be configured to do** — every page
  has a curated `Common options` table that names the kwargs
  worth knowing (and excludes ones that are redundant or rarely
  useful).
- **What events a widget emits and how to observe them** — every
  page has an `Events` section listing virtual events, payloads,
  and the corresponding `on_*` / `off_*` helper names.
- **When to use one widget over a sibling** — each page closes
  with a `When should I use X?` block that names the closest
  alternatives and the deciding factor.

For *how to combine* widgets into common UX patterns (forms,
dialogs, navigation shells), see the
[Guides](../guides/index.md) section.

---

## Categories

Widgets are grouped by **intent**, not by underlying Tk class. The
zensical nav uses these same 12 groups. Each link below is a
sensible entry point — typically the most foundational widget in
the category.

**Application chrome (4)**

The window itself and the structural shell around the page body.

- [App](application/app.md), [Toplevel](application/toplevel.md)
  — the two window classes; `App` is the root, `Toplevel` is a
  secondary window.
- [AppShell](application/appshell.md) — `App` + toolbar + side
  navigation + page stack, wired together. The fastest path to a
  multi-page application.
- [Toolbar](application/toolbar.md) — application chrome bar with
  buttons, separators, spacers, and free-form widgets.

**Actions (5)**

Controls that *initiate* something. Anchored on
[Button](actions/button.md).

- [Button](actions/button.md), [MenuButton](actions/menubutton.md),
  [DropdownButton](actions/dropdownbutton.md) — single-action
  controls; MenuButton opens a static menu, DropdownButton opens a
  dynamic one.
- [ContextMenu](actions/contextmenu.md) — popup menu attached to a
  trigger event (right-click, button-click, programmatic).
- [ButtonGroup](actions/buttongroup.md) — segmented strip of
  position-aware buttons sharing a single accent.

**Inputs (11)**

Single-cell value entry — the widgets users type into. Anchored on
[TextEntry](inputs/textentry.md).

- [TextEntry](inputs/textentry.md), [PasswordEntry](inputs/passwordentry.md),
  [PathEntry](inputs/pathentry.md), [ScrolledText](inputs/scrolledtext.md)
  — text inputs.
- [NumericEntry](inputs/numericentry.md), [SpinnerEntry](inputs/spinnerentry.md),
  [Scale](inputs/scale.md), [LabeledScale](inputs/labeledscale.md)
  — numeric inputs.
- [DateEntry](inputs/dateentry.md), [TimeEntry](inputs/timeentry.md)
  — date and time inputs (locale-aware, with calendar popup).
- [SelectBox](inputs/selectbox.md) — combobox-style picker (free
  text, type-ahead, or read-only).

**Selection (9)**

Controls that *choose* between values. Anchored on
[CheckButton](selection/checkbutton.md).

- [CheckButton](selection/checkbutton.md), [Switch](selection/switch.md),
  [CheckToggle](selection/checktoggle.md) — boolean selection.
- [RadioButton](selection/radiobutton.md), [RadioToggle](selection/radiotoggle.md),
  [RadioGroup](selection/radiogroup.md), [ToggleGroup](selection/togglegroup.md)
  — mutually-exclusive selection.
- [OptionMenu](selection/optionmenu.md) — list selection via a
  popup menu.
- [Calendar](selection/calendar.md) — date selection grid (single
  or range).

**Data display (8)**

Read-only widgets that show information back to the user. Anchored
on [Label](data-display/label.md).

- [Label](data-display/label.md), [Badge](data-display/badge.md)
  — atomic text displays.
- [Progressbar](data-display/progressbar.md), [FloodGauge](data-display/floodgauge.md),
  [Meter](data-display/meter.md) — progress and gauge readouts.
- [ListView](data-display/listview.md), [TableView](data-display/tableview.md),
  [TreeView](data-display/treeview.md) — data-bound list /
  tabular / hierarchical views.

**Layout (12)**

Containers and structural primitives. Anchored on
[Frame](layout/frame.md).

- [Frame](layout/frame.md), [Card](layout/card.md), [LabelFrame](layout/labelframe.md)
  — passive containers (your placement code does the layout).
- [PackFrame](layout/packframe.md), [GridFrame](layout/gridframe.md)
  — opinionated containers (the parent does the layout from
  declarative kwargs).
- [ScrollView](layout/scrollview.md) — scrollable viewport over an
  arbitrary widget tree.
- [Accordion](layout/accordion.md), [Expander](layout/expander.md),
  [PanedWindow](layout/panedwindow.md) — collapsible / resizable
  region containers.
- [Scrollbar](layout/scrollbar.md), [Separator](layout/separator.md),
  [SizeGrip](layout/sizegrip.md) — small structural primitives.

**Navigation (2)**

Primary chrome for moving between pages. Anchored on
[Tabs](navigation/tabs.md).

- [Tabs](navigation/tabs.md) — horizontal or vertical tab bar
  (no content coupling — pair with `PageStack` or wire pages
  manually).
- [SideNav](navigation/sidenav.md) — sidebar nav with collapsible
  pane and three display modes.

**Views (3)**

Keyed page containers that switch content. Anchored on
[PageStack](views/pagestack.md).

- [PageStack](views/pagestack.md) — keyed registry of pages with
  push / back / forward history.
- [TabView](views/tabview.md) — `Tabs` + `PageStack` wired
  together by a shared variable.
- [Notebook](views/notebook.md) — themed wrapper over
  `ttk.Notebook` with key-based registry and locale-aware tab
  labels.

**Forms (1)**

- [Form](forms/form.md) — spec-driven form builder; assembles a
  consistent set of input widgets, labels, validation, and layout
  from a single declaration.

**Dialogs (11)**

Modal interaction flows. Anchored on
[MessageDialog](dialogs/messagedialog.md).

- [MessageDialog](dialogs/messagedialog.md), [MessageBox](dialogs/messagebox.md)
  — confirm / inform / warn flows.
- [QueryDialog](dialogs/querydialog.md), [QueryBox](dialogs/querybox.md)
  — single-value prompts.
- [FormDialog](dialogs/formdialog.md) — embeds a `Form` in a
  modal.
- [DateDialog](dialogs/datedialog.md), [ColorChooser](dialogs/colorchooser.md),
  [ColorDropper](dialogs/colordropper.md), [FontDialog](dialogs/fontdialog.md)
  — value pickers.
- [FilterDialog](dialogs/filterdialog.md) — multi-select filter
  with search + Select All.
- [Dialog](dialogs/dialog.md) — base class to extend when the
  built-ins don't fit.

**Overlays (2)**

Ephemeral, non-modal UI. Anchored on
[ToolTip](overlays/tooltip.md).

- [ToolTip](overlays/tooltip.md) — hover-triggered, attached to a
  target widget.
- [Toast](overlays/toast.md) — programmatically shown
  notification, dismisses on a timer or button click.

**Primitives (5)**

The raw Tk / ttk surfaces composites build on. Anchored on
[Entry](primitives/entry.md).

- [Entry](primitives/entry.md), [Combobox](primitives/combobox.md),
  [Spinbox](primitives/spinbox.md) — `ttk.*` wrappers with
  ttkbootstrap styling tokens.
- [Text](primitives/text.md), [Canvas](primitives/canvas.md) —
  multi-line text and drawing surface (autostyled `tk.*`
  widgets).

---

## Where to start

If you are building your first ttkbootstrap app, three pages will
take you a long way:

- [App](application/app.md) — how the root window, theme, and
  settings come together.
- [AppShell](application/appshell.md) — opinionated multi-page
  shell with toolbar and side navigation.
- [Form](forms/form.md) — the fastest way to render a useful
  data-entry UI.

For visual styling — the meaning of `accent`, `variant`, `surface`,
`density`, theme tokens — see
[Design System](../design-system/index.md). For exact class
signatures, see the
[API Reference](../reference/widgets/index.md).
