"""Dynamic form widget for building data entry layouts quickly."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from tkinter import BooleanVar, DoubleVar, IntVar, StringVar, Text, Variable
from typing import Any, Callable, Iterable, Literal, Mapping, Sequence, TYPE_CHECKING

from ttkbootstrap.constants import DEFAULT_MIN_COL_WIDTH
from ttkbootstrap.widgets.primitives.button import Button
from ttkbootstrap.widgets.primitives.checkbutton import CheckButton
from ttkbootstrap.widgets.composites.dateentry import DateEntry
from ttkbootstrap.widgets.composites.field import Field
from ttkbootstrap.widgets.primitives.frame import Frame
from ttkbootstrap.widgets.primitives.label import Label
from ttkbootstrap.widgets.primitives.labelframe import LabelFrame
from ttkbootstrap.widgets.mixins import configure_delegate
from ttkbootstrap.widgets.primitives.notebook import Notebook
from ttkbootstrap.widgets.composites.numericentry import NumericEntry
from ttkbootstrap.widgets.composites.passwordentry import PasswordEntry
from ttkbootstrap.widgets.primitives.scale import Scale
from ttkbootstrap.widgets.primitives.selectbox import SelectBox
from ttkbootstrap.widgets.primitives.spinbox import Spinbox
from ttkbootstrap.widgets.composites.textentry import TextEntry
from ttkbootstrap.widgets.mixins.validation_mixin import ValidationMixin
from ttkbootstrap.widgets.types import Master

if TYPE_CHECKING:
    from ttkbootstrap.dialogs.dialog import DialogButton

DType = Literal['int', 'float', 'bool', 'date', 'datetime', 'password', 'str'] | type | None

EditorType = Literal[
    'selectbox',
    'combobox',
    'spinbox',
    'text',
    'textentry',
    'numericentry',
    'dateentry',
    'passwordentry',
    'toggle',
    'checkbutton',
    'scale',
]


@dataclass
class FieldItem:
    """Field definition used by Form."""
    key: str
    label: str | None = None
    dtype: DType = None
    readonly: bool = False
    visible: bool = True
    column: int | None = None
    row: int | None = None
    columnspan: int = 1
    rowspan: int = 1
    editor: EditorType | None = None
    editor_options: dict[str, Any] = field(default_factory=dict)
    type: Literal['field'] = "field"


@dataclass
class GroupItem:
    """Grouping of field items laid out in a grid with optional label/padding."""
    items: list[FieldItem | Mapping[str, Any] | GroupItem | TabsItem] = field(default_factory=list)
    label: str | None = None
    col_count: int = 1
    min_col_width: int = DEFAULT_MIN_COL_WIDTH
    width: int | None = None
    height: int | None = None
    column: int | None = None
    row: int | None = None
    columnspan: int = 1
    rowspan: int = 1
    padding: int | str | tuple[int, int] | tuple[int, int, int, int] | None = 8
    type: Literal['group'] = "group"


@dataclass
class TabItem:
    """Single tab within a TabsItem."""
    label: str
    items: list[FieldItem | Mapping[str, Any] | GroupItem | TabsItem] = field(default_factory=list)
    padding: int | str | tuple[int, int] | tuple[int, int, int, int] | None = 8


@dataclass
class TabsItem:
    """Notebook container with one or more TabItem entries."""
    tabs: list[TabItem | Mapping[str, Any]] = field(default_factory=list)
    label: str | None = None
    width: int | None = None
    height: int | None = None
    column: int | None = None
    row: int | None = None
    columnspan: int = 1
    rowspan: int = 1
    type: Literal['tabs'] = "tabs"


FormItem = FieldItem | GroupItem | TabsItem
ButtonInput = str | Mapping[str, Any] | "DialogButton"


class Form(Frame):
    """A configurable form that can be generated from data or explicit items.

    Args:
        master: Parent widget.
        data: Initial data backing the form. If items are not provided,
            field items are inferred from the keys and value types.
        items: Optional explicit form definition. Accepts dictionaries that
            match the FieldItem/GroupItem/TabsItem shapes or the dataclass
            instances directly.
        col_count: Number of columns at the top level.
        min_col_width: Minimum width for each column in pixels.
        on_data_changed: Optional callback invoked with the updated data dict
            whenever a field value changes.
        width: Requested width for the form container.
        height: Requested height for the form container.
        color: Color token for the form container (e.g., 'primary', 'secondary').
        buttons: Optional footer buttons. Accepts plain strings, DialogButton
            instances, or dictionaries that map to DialogButton kwargs.
        **kwargs: Additional Frame configuration options.
    """

    def __init__(
            self,
            master: Master = None,
            *,
            data: dict[str, Any] | None = None,
            items: Sequence[FormItem | Mapping[str, Any]] | None = None,
            col_count: int = 1,
            min_col_width: int = DEFAULT_MIN_COL_WIDTH,
            on_data_changed: Callable[[dict[str, Any]], Any] | None = None,
            width: int | None = None,
            height: int | None = None,
            color: str | None = None,
            buttons: Sequence[ButtonInput] | None = None,
            **kwargs: Any,
    ) -> None:
        """Build a configurable form from data or explicit items.

        Args:
            master: Parent widget.
            data: Initial data backing the form; keys become field names.
            items: Explicit form layout (FieldItem/GroupItem/TabsItem or mappings).
            col_count: Number of columns at the top level.
            min_col_width: Minimum width per column in pixels.
            on_data_changed: Callback invoked with updated data when a field changes.
            width: Requested form width; if None, size naturally.
            height: Requested form height; if None, size naturally.
            color: Color token for the form container.
            buttons: Optional footer buttons (DialogButton, mapping, or string).
            **kwargs: Additional Frame configuration options.
        """
        # Support legacy bootstyle parameter
        if 'bootstyle' in kwargs:
            color = color or kwargs.pop('bootstyle')
        super().__init__(master=master, width=width, height=height, color=color, **kwargs)

        self._data: dict[str, Any] = dict(data) if data else {}
        self.result: Any = None
        self._on_data_changed = on_data_changed
        self._col_count = col_count
        self._min_col_width = min_col_width
        self._widgets: dict[str, Any] = {}
        self._variables: dict[str, Variable] = {}
        self._signals: dict[str, Any] = {}
        self._textsignals: dict[str, Any] = {}
        self._items_by_key: dict[str, FieldItem] = {}
        self._suspend_sync = False

        normalized_items = self._normalize_items(items or self._infer_items_from_data(self._data))

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        container = Frame(self)
        container.grid(row=0, column=0, sticky='nsew')
        self._content_frame = Frame(container)
        self._content_frame.pack(fill='both', expand=True)

        # Respect explicit width/height by preventing geometry propagation.
        if width or height:
            if width:
                self.configure(width=width)
                container.configure(width=width)
            if height:
                self.configure(height=height)
                container.configure(height=height)
            self.grid_propagate(False)
            self.pack_propagate(False)
            container.grid_propagate(False)

        self._build_items(
            self._content_frame, normalized_items, col_count=self._col_count, min_col_width=self._min_col_width)

        if buttons:
            footer = Frame(self)
            footer.grid(row=1, column=0, sticky='ew', pady=(8, 0))
            footer.columnconfigure(0, weight=1)
            self._build_buttons(footer, buttons)

    @property
    def data(self) -> dict[str, Any]:
        """Current data backing the form."""
        return dict(self._collect_data())

    def validate(self) -> bool:
        """Run validation rules on all field widgets; returns True if all pass."""
        all_valid = True
        first_invalid_widget = None

        def _validate_field(widget: Field) -> bool:
            entry = getattr(widget, "_entry", widget)
            rules = getattr(entry, "_rules", [])
            if not rules:
                return True
            value = widget.value
            payload: dict[str, Any] = {"value": value, "is_valid": True, "message": ""}
            is_valid = True
            for rule in rules:
                if rule.trigger not in ("always", "manual"):
                    continue
                result = rule.validate(value)
                payload.update(is_valid=result.is_valid, message=result.message)
                if not result.is_valid:
                    is_valid = False
                    try:
                        entry.event_generate(ValidationMixin.EVENT_INVALID, data=payload)
                        entry.event_generate(ValidationMixin.EVENT_VALIDATED, data=payload)
                    except Exception:
                        pass
                    break
            if is_valid:
                try:
                    entry.event_generate(ValidationMixin.EVENT_VALID, data=payload)
                    entry.event_generate(ValidationMixin.EVENT_VALIDATED, data=payload)
                except Exception:
                    pass
            return is_valid

        for widget in self._widgets.values():
            if isinstance(widget, Field):
                ok = _validate_field(widget)
                if not ok and first_invalid_widget is None:
                    first_invalid_widget = widget
                all_valid = all_valid and ok
        if first_invalid_widget:
            try:
                first_invalid_widget.focus_set()
            except Exception:
                pass
        return all_valid

    def get_field_variable(self, key: str) -> Variable | None:
        """Return the Tk variable associated with a field key, if any."""
        return self._variables.get(key)

    def get_field_signal(self, key: str):
        """Return the Signal associated with a field key, if any."""
        return self._signals.get(key)

    def get_field_textsignal(self, key: str):
        """Return the TextSignal associated with a field key, if any."""
        return self._textsignals.get(key)

    @configure_delegate('data')
    def _delegate_data(self, value: Mapping[str, Any] = None):
        if value is None:
            return dict(self._collect_data())
        else:
            self._data = dict(value)
            self._suspend_sync = True
            try:
                for key, item in self._items_by_key.items():
                    value = self._data.get(key)
                    self._apply_value_to_widget(key, item, value)
            finally:
                self._suspend_sync = False
            return None

    def _build_items(self, parent: Frame, items: Sequence[FormItem], *, col_count: int, min_col_width: int) -> None:
        for col in range(col_count):
            parent.columnconfigure(col, weight=1, minsize=min_col_width)

        auto_row = 0
        auto_col = 0

        for item in items:
            widget = None
            columnspan = 1
            rowspan = 1

            if isinstance(item, FieldItem):
                widget = self._build_field(parent, item)
                columnspan = item.columnspan
                rowspan = item.rowspan
            elif isinstance(item, GroupItem):
                container = LabelFrame(parent, text=item.label, padding=item.padding) if item.label else Frame(
                    parent, padding=item.padding)
                if item.width:
                    container.configure(width=item.width)
                if item.height:
                    container.configure(height=item.height)
                nested_items = self._normalize_items(item.items)
                self._build_items(
                    container,
                    nested_items,
                    col_count=item.col_count or col_count,
                    min_col_width=item.min_col_width or min_col_width,
                )
                widget = container
                columnspan = item.columnspan
                rowspan = item.rowspan
            elif isinstance(item, TabsItem):
                notebook = Notebook(parent, width=item.width, height=item.height)
                for tab in self._normalize_tabs(item.tabs):
                    tab_frame = Frame(notebook, padding=tab.padding)
                    self._build_items(
                        tab_frame, self._normalize_items(tab.items), col_count=col_count, min_col_width=min_col_width)
                    notebook.add(tab_frame, text=tab.label)
                widget = notebook
                columnspan = item.columnspan
                rowspan = item.rowspan

            if widget is None:
                continue

            row = item.row if isinstance(item, (FieldItem, GroupItem, TabsItem)) and item.row is not None else auto_row
            column = item.column if isinstance(
                item, (FieldItem, GroupItem, TabsItem)) and item.column is not None else auto_col

            widget.grid(row=row, column=column, columnspan=columnspan, rowspan=rowspan, sticky='nsew', padx=6, pady=4)

            if isinstance(item, (FieldItem, GroupItem, TabsItem)) and item.row is None and item.column is None:
                auto_col += columnspan
                if auto_col >= col_count:
                    auto_col = 0
                    auto_row += 1

    def _build_field(self, parent: Frame, item: FieldItem):
        if not item.visible:
            return None

        editor = item.editor or self._default_editor_for_dtype(item.dtype, self._data.get(item.key))
        options = dict(item.editor_options or {})
        initial_value = self._data.get(item.key)
        variable = self._variable_for_item(item, initial_value, editor)
        label_text = item.label if item.label is not None else item.key.replace("_", " ").title()

        container = Frame(parent)
        container.columnconfigure(0, weight=1)  # Allow field widgets to expand horizontally

        # Validation options that should only be passed to widgets supporting ValidationMixin
        validation_options = {'show_message', 'required', 'validator'}

        field_widget: Any
        if editor == 'textentry':
            field_widget = TextEntry(
                container, value=initial_value or "", label=label_text, textvariable=variable, **options)
        elif editor == 'numericentry':
            numeric_value = initial_value if initial_value is not None else 0
            field_widget = NumericEntry(
                container, value=numeric_value, label=label_text, **options)
            self._bind_numeric_variable(item.key, field_widget, variable)
        elif editor == 'passwordentry':
            field_widget = PasswordEntry(
                container, value=initial_value or "", label=label_text, textvariable=variable, **options)
        elif editor == 'dateentry':
            field_widget = DateEntry(container, value=initial_value, label=label_text, textvariable=variable, **options)
        else:
            # Filter out validation options for widgets that don't support ValidationMixin
            filtered_options = {k: v for k, v in options.items() if k not in validation_options}

            # Use inline label for checkbutton/toggle, otherwise show a Label widget.
            if editor in ("checkbutton", "toggle"):
                if not filtered_options.get("text"):
                    filtered_options["text"] = label_text
            elif label_text != "" and editor not in ('selectbox', 'combobox'):
                Label(container, text=label_text).pack(anchor='w', pady=(0, 2))

            if editor in ('selectbox', 'combobox'):
                items = options.pop('items', options.pop('values', None)) or []
                items = [str(i) for i in items]
                field_widget = SelectBox(
                    container,
                    label=label_text,
                    value=initial_value or "",
                    items=items,
                    textvariable=variable,
                    **options
                )
                if initial_value is not None and variable is not None:
                    variable.set(initial_value)
            elif editor == 'spinbox':
                field_widget = Spinbox(container, textvariable=variable, **filtered_options)
                if initial_value is not None:
                    variable.set(initial_value)
            elif editor == 'text':
                field_widget = Text(container, **filtered_options)
                if initial_value:
                    field_widget.insert('1.0', str(initial_value))
            elif editor == 'toggle':
                field_widget = CheckButton(container, variable=variable, **filtered_options)
            elif editor == 'checkbutton':
                field_widget = CheckButton(container, variable=variable, **filtered_options)
            elif editor == 'scale':
                field_widget = Scale(container, variable=variable, **filtered_options)
            else:
                field_widget = TextEntry(
                    container, value=initial_value or "", label=label_text, textvariable=variable, **options)

            if editor != 'text':
                field_widget.pack(fill='x', expand=True)
            else:
                field_widget.pack(fill='both', expand=True)

        if isinstance(field_widget, Field):
            field_widget.bind("<<Change>>", lambda _e, k=item.key: self._sync_value_from_widget(k))
            field_widget.pack(fill='both', expand=True)
            if not isinstance(field_widget, NumericEntry):
                traced_var = getattr(field_widget, "variable", None)
                if traced_var is not None:
                    self._register_variable(item.key, traced_var)
        elif isinstance(field_widget, Text):
            text_var = variable or StringVar(value=str(initial_value) if initial_value is not None else "")
            self._register_variable(item.key, text_var)
            self._bind_text_change(field_widget, item.key, text_var)
        elif variable is not None:
            self._register_variable(item.key, variable)

        # record signals if the widget exposes them
        signal_obj = getattr(field_widget, "_signal", None)
        if signal_obj is not None:
            self._signals[item.key] = signal_obj
        text_signal = getattr(field_widget, "_textsignal", None)
        if text_signal is not None:
            self._textsignals[item.key] = text_signal

        if item.readonly:
            self._set_readonly(field_widget)

        self._widgets[item.key] = field_widget
        return container

    def _build_buttons(self, parent: Frame, buttons: Sequence[ButtonInput]) -> None:
        parsed = self._normalize_buttons(buttons)
        for spec in reversed(parsed):
            # Support both color and legacy bootstyle from DialogButton
            btn_color = getattr(spec, 'color', None) or spec.bootstyle
            btn_variant = getattr(spec, 'variant', None)

            if not btn_color:
                # Get color and variant from role
                btn_color, btn_variant = self._style_for_role(spec.role)

            btn = Button(parent, text=spec.text, color=btn_color, variant=btn_variant)
            btn.configure(command=self._make_button_command(spec))
            btn.pack(side='right', padx=(4, 0))

    # --- normalization --------------------------------------------------
    def _normalize_items(self, items: Iterable[FormItem | Mapping[str, Any]]) -> list[FormItem]:
        normalized: list[FormItem] = []
        for raw in items:
            item: FormItem | None = None
            if isinstance(raw, (FieldItem, GroupItem, TabsItem)):
                item = raw
            elif isinstance(raw, Mapping):
                type_hint = raw.get('type', 'field')
                if type_hint == 'group':
                    item = GroupItem(
                        items=list(raw.get('items', [])),
                        label=raw.get('label'),
                        col_count=raw.get('col_count', 1),
                        min_col_width=raw.get('min_col_width', DEFAULT_MIN_COL_WIDTH),
                        width=raw.get('width'),
                        height=raw.get('height'),
                        column=raw.get('column'),
                        row=raw.get('row'),
                        columnspan=raw.get('columnspan', 1),
                        rowspan=raw.get('rowspan', 1),
                    )
                elif type_hint == 'tabs':
                    item = TabsItem(
                        tabs=list(raw.get('tabs', [])),
                        label=raw.get('label'),
                        width=raw.get('width'),
                        height=raw.get('height'),
                        column=raw.get('column'),
                        row=raw.get('row'),
                        columnspan=raw.get('columnspan', 1),
                        rowspan=raw.get('rowspan', 1),
                    )
                else:
                    key_value = raw.get('key')
                    if key_value is None:
                        continue
                    item = FieldItem(
                        key=str(key_value),
                        label=raw.get('label'),
                        dtype=raw.get('dtype'),
                        readonly=raw.get('readonly', False),
                        visible=raw.get('visible', True),
                        column=raw.get('column'),
                        row=raw.get('row'),
                        columnspan=raw.get('columnspan', 1),
                        rowspan=raw.get('rowspan', 1),
                        editor=raw.get('editor'),
                        editor_options=dict(raw.get('editor_options', {}) or {}),
                    )

            if isinstance(item, GroupItem):
                item.items = self._normalize_items(item.items)
            if isinstance(item, TabsItem):
                item.tabs = self._normalize_tabs(item.tabs)
            if isinstance(item, FieldItem):
                self._items_by_key[item.key] = item

            if item:
                normalized.append(item)
        return normalized

    def _normalize_tabs(self, tabs: Iterable[TabItem | Mapping[str, Any]]) -> list[TabItem]:
        normalized: list[TabItem] = []
        for raw in tabs:
            if isinstance(raw, TabItem):
                normalized.append(raw)
            elif isinstance(raw, Mapping):
                normalized.append(TabItem(label=str(raw.get('label', 'Tab')), items=list(raw.get('items', []))))
        return normalized

    def _normalize_buttons(self, buttons: Sequence[ButtonInput]) -> list["DialogButton"]:
        from ttkbootstrap.dialogs.dialog import DialogButton  # local import to avoid circular init

        normalized: list[DialogButton] = []
        for raw in buttons:
            if isinstance(raw, DialogButton):
                normalized.append(raw)
            elif isinstance(raw, Mapping):
                normalized.append(DialogButton(**raw))  # type: ignore[arg-type]
            elif isinstance(raw, str):
                normalized.append(DialogButton(text=raw, role="primary" if not normalized else "secondary"))
        return normalized

    # --- data helpers ---------------------------------------------------
    def _collect_data(self) -> dict[str, Any]:
        current: dict[str, Any] = dict(self._data)
        for key in self._widgets.keys():
            current[key] = self._read_value_from_widget(key)
        return current

    def _read_value_from_widget(self, key: str) -> Any:
        widget = self._widgets.get(key)
        if widget is None:
            return self._data.get(key)

        if hasattr(widget, "value"):
            val_attr = getattr(widget, "value")
            value = val_attr() if callable(val_attr) else val_attr
        elif key in self._variables:
            value = self._variables[key].get()
        elif isinstance(widget, Text):
            value = widget.get("1.0", "end-1c")
        else:
            try:
                value = widget.get()
            except Exception:
                value = self._data.get(key)

        item = self._items_by_key.get(key)
        if item:
            value = self._coerce_value(item.dtype, value)
        return value

    def _apply_value_to_widget(self, key: str, item: FieldItem, value: Any) -> None:
        widget = self._widgets.get(key)
        if widget is None:
            return

        if isinstance(widget, Field):
            if hasattr(widget, "_suppress_changed_event"):
                widget._suppress_changed_event = True  # type: ignore[attr-defined]
                try:
                    widget.value = value
                finally:
                    widget._suppress_changed_event = False  # type: ignore[attr-defined]
            else:
                widget.value = value
            return

        if isinstance(widget, Text):
            widget.delete("1.0", "end")
            if value is not None:
                widget.insert("1.0", str(value))
            return

        if key in self._variables:
            self._variables[key].set("" if value is None else value)
            return

        try:
            widget.configure(value=value)
        except Exception:
            pass

    def _sync_value_from_widget(self, key: str) -> None:
        if self._suspend_sync:
            return
        if key not in self._items_by_key:
            return
        new_value = self._read_value_from_widget(key)
        self._data[key] = new_value
        if self._on_data_changed:
            self._on_data_changed(dict(self._data))

    def _variable_for_item(self, item: FieldItem, initial: Any, editor: EditorType | None) -> Variable | None:
        dtype = item.dtype
        if editor in ('checkbutton', 'toggle'):
            return BooleanVar(value=bool(initial) if initial is not None else False)
        if editor in ('numericentry', 'spinbox', 'scale') or dtype in ('int', int, 'float', float):
            if dtype in ('float', float):
                return DoubleVar(value=float(initial) if initial is not None else 0.0)
            return IntVar(value=int(initial) if initial is not None else 0)
        return StringVar(value="" if initial is None else str(initial))

    def _default_editor_for_dtype(self, dtype: Any, value: Any) -> EditorType:
        if dtype in ('int', int, 'float', float):
            return 'numericentry'
        if dtype in ('bool', bool):
            return 'checkbutton'
        if dtype in ('date', 'datetime', date, datetime):
            return 'dateentry'
        if dtype in ('password',):
            return 'passwordentry'
        if value is not None:
            if isinstance(value, (int, float)):
                return 'numericentry'
            if isinstance(value, (bool,)):
                return 'checkbutton'
            if isinstance(value, (date, datetime)):
                return 'dateentry'
        return 'textentry'

    def _coerce_value(self, dtype: Any, value: Any) -> Any:
        if dtype in ('int', int):
            try:
                return int(value)
            except Exception:
                return value
        if dtype in ('float', float):
            try:
                return float(value)
            except Exception:
                return value
        if dtype in ('bool', bool):
            return bool(value)
        if dtype in ('date', 'datetime', date, datetime):
            return value
        return value

    def _register_variable(self, key: str, var: Variable) -> None:
        self._variables[key] = var
        var.trace_add("write", lambda *_a, k=key: self._sync_value_from_widget(k))

    def _bind_text_change(self, widget: Text, key: str, var: StringVar | None = None) -> None:
        _updating = {"text": False}

        def _on_change(_event=None):
            if _updating["text"]:
                return
            _updating["text"] = True
            try:
                widget.edit_modified(False)
                text = widget.get("1.0", "end-1c")
                if var is not None:
                    var.set(text)
                self._sync_value_from_widget(key)
            finally:
                _updating["text"] = False

        def _on_var_change(*_args):
            if _updating["text"] or var is None:
                return
            _updating["text"] = True
            try:
                widget.delete("1.0", "end")
                widget.insert("1.0", var.get())
            finally:
                _updating["text"] = False

        widget.bind("<<Modified>>", _on_change)
        widget.edit_modified(False)

        if var is not None:
            var.trace_add("write", _on_var_change)

    def _bind_numeric_variable(self, key: str, widget: NumericEntry, var: Variable | None) -> None:
        if var is None:
            return

        self._register_variable(key, var)

        def _sync_numeric_var(*_args):
            new_value = widget.value
            if new_value is None:
                return
            try:
                current_value = var.get()
            except Exception:
                current_value = None
            if current_value == new_value:
                return
            previous_suspend = self._suspend_sync
            self._suspend_sync = True
            try:
                var.set(new_value)
            finally:
                self._suspend_sync = previous_suspend

        text_signal = getattr(widget, "signal", None)
        if text_signal is not None:
            text_signal.subscribe(lambda *_: _sync_numeric_var())
        _sync_numeric_var()

    def _set_readonly(self, widget: Any) -> None:
        if isinstance(widget, Field):
            widget.readonly(True)
        else:
            try:
                widget.state(['disabled'])
            except Exception:
                try:
                    widget.configure(state='disabled')
                except Exception:
                    pass

    # --- button helpers -------------------------------------------------
    def _make_button_command(self, spec: DialogButton):
        def command():
            if spec.command:
                spec.command(self)  # type: ignore[arg-type]
            self.result = spec.result if spec.result is not None else self.data

        return command

    def _style_for_role(self, role: str) -> tuple[str, str | None]:
        """Get color and variant for a button role.

        Returns:
            Tuple of (color, variant) for the role.
        """
        if role == "primary":
            return ("primary", None)
        if role == "secondary":
            return ("secondary", None)
        if role == "danger":
            return ("danger", None)
        if role == "cancel":
            return ("secondary", "outline")
        if role == "help":
            return ("info", "link")
        return ("secondary", None)

    # --- inference ------------------------------------------------------
    def _infer_items_from_data(self, data: Mapping[str, Any]) -> list[FieldItem]:
        inferred: list[FieldItem] = []
        for key, value in data.items():
            inferred.append(
                FieldItem(
                    key=str(key),
                    label=str(key).replace('_', ' ').title(),
                    dtype=self._infer_dtype_from_value(value),
                    editor=self._default_editor_for_dtype(self._infer_dtype_from_value(value), value),
                    editor_options={"show_message": True},
                )
            )
        return inferred

    @staticmethod
    def _infer_dtype_from_value(value: Any) -> DType:
        if isinstance(value, bool):
            return 'bool'
        if isinstance(value, int) and not isinstance(value, bool):
            return 'int'
        if isinstance(value, float):
            return 'float'
        if isinstance(value, (date, datetime)):
            return 'date'
        return 'str'


__all__ = [
    "Form",
    "FormItem",
    "FieldItem",
    "GroupItem",
    "TabsItem",
    "TabItem",
    "EditorType",
]
