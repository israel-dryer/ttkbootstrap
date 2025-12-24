# Widgets

ttkbootstrap provides a comprehensive set of themed widgets for building modern desktop applications. All widgets support the bootstyle system for easy styling with Bootstrap-inspired color schemes and variants.

## Widget Categories

### Actions

Interactive elements for triggering commands and actions.

| Widget | Description |
|--------|-------------|
| [Button](actions/button.md) | Standard themed button |
| [DropdownButton](actions/dropdownbutton.md) | Button with dropdown menu |
| [MenuButton](actions/menubutton.md) | Button that displays a menu |
| [ContextMenu](actions/contextmenu.md) | Right-click context menu |
| [ButtonGroup](actions/buttongroup.md) | Group of related buttons |

### Inputs

Widgets for text and data entry.

| Widget | Description |
|--------|-------------|
| [TextEntry](inputs/textentry.md) | Single-line text input |
| [PasswordEntry](inputs/passwordentry.md) | Masked password input |
| [PathEntry](inputs/pathentry.md) | File/folder path selector |
| [ScrolledText](inputs/scrolledtext.md) | Multi-line text with scrollbars |
| [SpinnerEntry](inputs/spinnerentry.md) | Text entry with loading spinner |
| [NumericEntry](inputs/numericentry.md) | Numeric input with validation |
| [Scale](inputs/scale.md) | Slider for numeric values |
| [LabeledScale](inputs/labeledscale.md) | Scale with value label |
| [DateEntry](inputs/dateentry.md) | Date picker input |
| [TimeEntry](inputs/timeentry.md) | Time picker input |

### Selection

Widgets for choosing options and making selections.

| Widget | Description |
|--------|-------------|
| [CheckButton](selection/checkbutton.md) | Checkbox for boolean values |
| [CheckToggle](selection/checktoggle.md) | Toggle switch style checkbox |
| [RadioButton](selection/radiobutton.md) | Radio button for single selection |
| [RadioToggle](selection/radiotoggle.md) | Toggle switch style radio button |
| [RadioGroup](selection/radiogroup.md) | Group of radio buttons |
| [ToggleGroup](selection/togglegroup.md) | Group of toggle buttons |
| [OptionMenu](selection/optionmenu.md) | Dropdown option selector |
| [SelectBox](selection/selectbox.md) | Searchable selection box |

### Data Display

Widgets for presenting information and data.

| Widget | Description |
|--------|-------------|
| [Label](data-display/label.md) | Text or image display |
| [ListView](data-display/listview.md) | Scrollable list of items |
| [TreeView](data-display/treeview.md) | Hierarchical tree display |
| [TableView](data-display/tableview.md) | Data table with sorting and filtering |
| [Badge](data-display/badge.md) | Small status indicator |
| [Progressbar](data-display/progressbar.md) | Progress indicator |
| [Meter](data-display/meter.md) | Circular progress/gauge |
| [FloodGauge](data-display/floodgauge.md) | Animated fill gauge |

### Layout

Container widgets for organizing UI elements.

| Widget | Description |
|--------|-------------|
| [Frame](layout/frame.md) | Basic container |
| [LabelFrame](layout/labelframe.md) | Container with title |
| [PanedWindow](layout/panedwindow.md) | Resizable paned container |
| [ScrollView](layout/scrollview.md) | Scrollable container |
| [Scrollbar](layout/scrollbar.md) | Scroll control |
| [Separator](layout/separator.md) | Visual divider |
| [SizeGrip](layout/sizegrip.md) | Window resize handle |

### Views

Widgets for organizing content into views.

| Widget | Description |
|--------|-------------|
| [Notebook](views/notebook.md) | Tabbed container |
| [PageStack](views/pagestack.md) | Stacked page container |

### Forms

Widgets for building data entry forms.

| Widget | Description |
|--------|-------------|
| [Form](forms/form.md) | Form layout and validation |

### Dialogs

Pre-built dialog windows for common tasks.

| Widget | Description |
|--------|-------------|
| [MessageDialog](dialogs/messagedialog.md) | Information/alert messages |
| [MessageBox](dialogs/messagebox.md) | Simple message popup |
| [ColorChooser](dialogs/colorchooser.md) | Color selection |
| [ColorDropper](dialogs/colordropper.md) | Screen color picker |
| [FontDialog](dialogs/fontdialog.md) | Font selection |
| [DateDialog](dialogs/datedialog.md) | Date selection |
| [FormDialog](dialogs/formdialog.md) | Multi-field form dialog |
| [QueryDialog](dialogs/querydialog.md) | Single input query |
| [QueryBox](dialogs/querybox.md) | Quick input popup |
| [FilterDialog](dialogs/filterdialog.md) | Data filtering interface |
| [Dialog](dialogs/dialog.md) | Base dialog class |

### Overlays

Widgets that appear on top of other content.

| Widget | Description |
|--------|-------------|
| [Toast](overlays/toast.md) | Temporary notification |
| [ToolTip](overlays/tooltip.md) | Hover tooltip |

### Primitives

Low-level widgets for advanced use cases.

| Widget | Description |
|--------|-------------|
| [Canvas](primitives/canvas.md) | Drawing surface |
| [Combobox](primitives/combobox.md) | Dropdown with text entry |
| [Entry](primitives/entry.md) | Basic text entry |
| [Spinbox](primitives/spinbox.md) | Numeric spinner |
| [Text](primitives/text.md) | Multi-line text widget |

## Bootstyle System

All widgets support the `bootstyle` parameter for easy theming:

```python
import ttkbootstrap as ttk

app = ttk.App()

# Color variants
ttk.Button(app, text="Primary", bootstyle="primary")
ttk.Button(app, text="Success", bootstyle="success")
ttk.Button(app, text="Danger", bootstyle="danger")

# Style modifiers
ttk.Button(app, text="Outline", bootstyle="primary-outline")
ttk.Button(app, text="Link", bootstyle="info-link")

app.mainloop()
```

See the [Design System](../design-system/index.md) guide for more details on colors and variants.