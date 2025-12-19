from tkinter import TclError

from ttkbootstrap.widgets.mixins import configure_delegate
from ttkbootstrap.widgets.primitives.button import Button
from ttkbootstrap.widgets.primitives.frame import Frame
from ttkbootstrap.widgets.primitives.label import Label
from ttkbootstrap.widgets.primitives.separator import Separator


class ListItem(Frame):

    def __init__(self, master=None, **kwargs):
        # state tracking
        self._data = {}
        self._state = {}
        self._item_index = 0
        self._ignore_selection_by_click = False
        self._selection_icon = None
        self._drag_state = None

        # configuration properties
        self._focus_color = kwargs.pop('focus_color', None)
        self._show_separator = kwargs.pop('show_separator', False)
        self._show_chevron = kwargs.pop('show_chevron', False)
        self._enable_focus_state = kwargs.pop('enable_focus_state')
        self._enable_dragging = kwargs.pop('enable_dragging', False)
        self._enable_deleting = kwargs.pop('enable_deleting', False)
        self._selection_background = kwargs.pop('selection_background', 'primary')
        self._selection_mode = kwargs.pop('selection_mode', 'none')
        self._show_selection_controls = kwargs.pop('show_selection_controls', False)
        self._enable_alternating_rows = kwargs.pop('enable_alternating_rows', False)
        self._alternating_row_color = kwargs.pop('alternating_row_color', 'background[+1]')
        self._alternating_row_mode = kwargs.pop('alternating_row_mode', 'even')

        if self._selection_mode == 'none':
            select_by_click = kwargs.get('select_by_click', False)
            self._ignore_selection_by_click = False if not self._show_selection_controls else not select_by_click

        self._get_selection_icon()

        super().__init__(
            master=master,
            bootstyle='list_item_separated' if self._show_separator else 'list_item',
            takefocus=self._enable_focus_state,
            padding=(8, 4),
            style_options=dict(selection_background=self._selection_background, focus_color=self._focus_color)
        )

        # composite container widgets
        self._left_frame = Frame(
            self,
            bootstyle='list',
            takefocus=False,
            style_options=dict(selection_background=self._selection_background)
        )
        self._left_frame.pack(side='left')

        self._center_frame = Frame(
            self,
            bootstyle='list',
            takefocus=False,
            style_options=dict(selection_background=self._selection_background)
        )
        self._center_frame.pack(side='left', fill='x', expand=True)

        self._right_frame = Frame(
            self,
            bootstyle='list',
            takefocus=False,
            style_options=dict(selection_background=self._selection_background)
        )
        self._right_frame.pack(side='left')

        # conditional widgets
        self._separator = Separator(self)
        self._selection_widget = None
        self._icon_widget = None
        self._title_widget = None
        self._text_widget = None
        self._caption_widget = None
        self._delete_widget = None
        self._badge_widget = None
        self._chevron_widget = None
        self._drag_widget = None

        self._composite_widgets = set()
        for widget in [self, self._left_frame, self._center_frame, self._right_frame]:
            self._add_composite_widget(widget, ignore_click=self._ignore_selection_by_click)

        # row-level pointer events (Enter/Leave are handled by shared bindtag)
        self.bind('<FocusIn>', self._on_focusin, add='+')
        self.bind('<FocusOut>', self._on_focusout, add='+')
        self.bind('<space>', self._on_mousedown, add='+')

    @property
    def selected(self):
        return self._data.get('selected')

    @property
    def data(self):
        return self._data

    def _get_selection_icon(self):
        if self._selection_mode == 'multi':
            self._selection_icon = dict(name='square', state=[('selected', "check-square-fill")])
        elif self._selection_mode == 'single':
            self._selection_icon = dict(name='circle', state=[('selected', "check-circle-fill")])
        else:
            self._selection_icon = None

    def _add_composite_widget(self, widget, ignore_click=False):
        self._composite_widgets.add(widget)

        # Use a shared bindtag for hover management across all composite widgets
        # This prevents child widgets from independently managing hover state
        hover_tag = f'ListItemHover{id(self)}'
        current_tags = list(widget.bindtags())

        # Insert the shared hover tag before the widget's class tag
        # This ensures our hover handler runs before widget-specific handlers
        if hover_tag not in current_tags:
            if len(current_tags) > 1:
                current_tags.insert(1, hover_tag)
            else:
                current_tags.append(hover_tag)
            widget.bindtags(tuple(current_tags))

        # Bind Enter/Leave to the shared tag (only once per ListItem)
        if not hasattr(self, '_hover_tag_bound'):
            widget.bind_class(hover_tag, '<Enter>', self._on_enter)
            widget.bind_class(hover_tag, '<Leave>', self._on_leave)
            self._hover_tag_bound = True

        widget.bind('<FocusIn>', self._on_focusin, add='+')
        widget.bind('<FocusOut>', self._on_focusout, add='+')

        if not ignore_click:
            widget.bind('<ButtonPress-1>', self._on_mousedown, add='+')
            widget.bind('<ButtonRelease-1>', self._on_mouseup, add='+')

        try:
            current = set(self.state())
        except TclError:
            current = set()

        for s in ('hover', 'pressed', 'selected', 'focus'):
            if s in current:
                try:
                    widget.state([s])
                except TclError:
                    pass

    def _update_selection(self, selected: bool = False):
        """Apply selection state atomically (style + icon) with null guards"""
        mode = self._selection_mode

        if mode == 'none':
            if self._selection_widget is not None:
                try:
                    self._selection_widget.pack_forget()
                except TclError:
                    pass
                self._composite_widgets.discard(self._selection_widget)
                try:
                    self._selection_widget.destroy()
                except TclError:
                    pass

            self._selection_widget = None
            # clear selected state on row + composites

            try:
                self.state(['!selected'])
            except TclError:
                pass

            for w in list(self._composite_widgets):
                try:
                    w.state(['!selected'])
                    w.event_generate('<<CompositeDeselect>>')
                except TclError:
                    pass

            # keep a remembered icon so later comparisons are cheap
            if hasattr(self, '_state'):
                self._state['__sel_icon'] = None
                self._state['selected'] = False
            return

        # ensure state cache exists
        if not hasattr(self, '_state'):
            self._state = {}

        # ensure the selection control exists even if not visible
        if self._selection_widget is None:
            self._selection_widget = Label(
                self._left_frame,
                icon=self._selection_icon,
                bootstyle='list_icon',
                icon_only=True,
                style_options=dict(selection_background=self._selection_background),
                takefocus=False,
            )
            if self._show_selection_controls:
                self._selection_widget.pack(side='left', padx=5)
            self._add_composite_widget(self._selection_widget)

        # apply selected state to the row + all composites (styles co-update)
        try:
            self.state(['selected' if selected else '!selected'])
        except TclError:
            pass

        for w in list(self._composite_widgets):
            try:
                w.state(['selected' if selected else '!selected'])
                w.event_generate('<<CompositeSelect>>' if selected else '<<CompositeDeselect>>')
            except TclError:
                pass

        # remember logical selected flag
        self._state['selected'] = bool(selected)

    def _update_icon(self, icon=None):
        """Update icon widget, or create if not existing"""
        if icon is not None:
            if not self._icon_widget:
                self._icon_widget = Label(
                    self._left_frame,
                    icon=icon,
                    bootstyle='list_icon',
                    takefocus=False,
                    icon_only=True,
                    style_options=dict(selection_background=self._selection_background)
                )
                self._icon_widget.pack(side='left', padx=5)
                self._add_composite_widget(self._icon_widget, ignore_click=self._ignore_selection_by_click)
            else:
                self._icon_widget.configure(icon=icon)
        else:
            if self._icon_widget:
                try:
                    self._icon_widget.pack_forget()
                    self._composite_widgets.discard(self._icon_widget)
                    self._icon_widget.destroy()
                except TclError:
                    pass
                finally:
                    self._icon_widget = None

    def _update_title(self, text=None):
        if text is not None:
            if not self._title_widget:
                self._title_widget = Label(
                    self._center_frame,
                    text=text,
                    font='heading-lg',
                    bootstyle='list',
                    takefocus=False,
                    style_options=dict(selection_background=self._selection_background)
                )
                self._title_widget.pack(side='top', fill='x', anchor='w', padx=(0, 3))
                self._add_composite_widget(self._title_widget, ignore_click=self._ignore_selection_by_click)
            else:
                self._title_widget.configure(text=text)
        else:
            if self._title_widget:
                try:
                    self._title_widget.pack_forget()
                    self._composite_widgets.discard(self._title_widget)
                    self._title_widget.destroy()
                except TclError:
                    pass
                finally:
                    self._title_widget = None

    def _update_text(self, text=None):
        if text is not None:
            if not self._text_widget:
                self._text_widget = Label(
                    self._center_frame,
                    text=text,
                    bootstyle='list',
                    takefocus=False,
                    style_options=dict(selection_background=self._selection_background)
                )
                self._text_widget.pack(side='top', fill='x', padx=(0, 3))
                self._add_composite_widget(self._text_widget, ignore_click=self._ignore_selection_by_click)
            else:
                self._text_widget.configure(text=text)
        else:
            if self._text_widget:
                try:
                    self._text_widget.pack_forget()
                    self._composite_widgets.discard(self._text_widget)
                    self._text_widget.destroy()
                except TclError:
                    pass
                finally:
                    self._text_widget = None

    def _update_caption(self, text=None):
        if text is not None:
            if not self._caption_widget:
                self._caption_widget = Label(
                    self._center_frame,
                    text=text,
                    font='caption',
                    anchor='w',
                    bootstyle='list',
                    takefocus=False,
                    style_options=dict(selection_background=self._selection_background)
                )
                self._caption_widget.pack(side='top', fill='x', padx=(0, 3))
                self._add_composite_widget(self._caption_widget, ignore_click=self._ignore_selection_by_click)
            else:
                self._caption_widget.configure(text=text)
        else:
            if self._caption_widget:
                try:
                    self._caption_widget.pack_forget()
                    self._composite_widgets.discard(self._caption_widget)
                    self._caption_widget.destroy()
                except TclError:
                    pass
                finally:
                    self._caption_widget = None

    def _update_badge(self, text=None):
        if text is not None:
            if not self._badge_widget:
                self._badge_widget = Label(
                    self._right_frame,
                    text=text,
                    bootstyle='list',
                    style_options=dict(selection_background=self._selection_background)
                )
                self._badge_widget.pack(side='right', padx=6)
                self._add_composite_widget(self._badge_widget, ignore_click=self._ignore_selection_by_click)
            else:
                self._badge_widget.configure(text=text)
        else:
            if self._badge_widget:
                try:
                    self._badge_widget.pack_forget()
                    self._composite_widgets.discard(self._badge_widget)
                    self._badge_widget.destroy()
                except TclError:
                    pass
                finally:
                    self._badge_widget = None

    def _update_chevron(self):
        if self._show_chevron:
            if not self._chevron_widget:
                self._chevron_widget = Button(
                    self._right_frame,
                    icon='chevron-right',
                    icon_only=True,
                    bootstyle='list_icon',
                    takefocus=False,
                    style_options=dict(selection_background=self._selection_background)
                )
                self._chevron_widget.pack(side='right', padx=6)
                self._add_composite_widget(self._chevron_widget, ignore_click=self._ignore_selection_by_click)
        else:
            if self._chevron_widget:
                try:
                    self._chevron_widget.pack_forget()
                    self._composite_widgets.discard(self._chevron_widget)
                    self._chevron_widget.destroy()
                except TclError:
                    pass
                finally:
                    self._chevron_widget = None

    def _update_delete(self):
        if self._enable_deleting:
            if not self._delete_widget:
                self._delete_widget = Button(
                    self._right_frame,
                    icon='x-lg',
                    icon_only=True,
                    bootstyle='list_icon',
                    takefocus=False,
                    style_options=dict(selection_background=self._selection_background)
                )
                self._delete_widget.pack(side='right', padx=6)
                self._delete_widget.bind('<ButtonPress-1>', lambda _: self.delete())
                self._add_composite_widget(self._delete_widget, ignore_click=self._ignore_selection_by_click)
        else:
            if self._delete_widget:
                try:
                    self._delete_widget.pack_forget()
                    self._composite_widgets.discard(self._delete_widget)
                    self._delete_widget.destroy()
                except TclError:
                    pass
                finally:
                    self._delete_widget = None

    def _update_drag(self):
        if self._enable_dragging:
            if not self._drag_widget:
                self._drag_widget = Button(
                    self._right_frame,
                    icon='grip-vertical',
                    icon_only=True,
                    bootstyle='list_icon',
                    cursor='fleur',
                    takefocus=False,
                    style_options=dict(selection_background=self._selection_background)
                )
                self._drag_widget.pack(side='right', padx=6)

                # Setup drag detection
                self._drag_state = {'dragging': False, 'start_y': None}
                self._drag_widget.bind('<ButtonPress-1>', self._on_drag_mouse_down, add='+')
                self._drag_widget.bind('<B1-Motion>', self._on_drag_mouse_motion, add='+')
                self._drag_widget.bind('<ButtonRelease-1>', self._on_drag_mouse_up, add='+')
                self._add_composite_widget(self._drag_widget, ignore_click=True)
        else:
            if self._drag_widget:
                try:
                    self._drag_widget.pack_forget()
                    self._composite_widgets.discard(self._drag_widget)
                    self._drag_widget.destroy()
                except TclError:
                    pass
                finally:
                    self._drag_widget = None
                    self._drag_state = None

    # ---- Event Handlers

    def _on_drag_mouse_down(self, event):
        """Mouse pressed on drag handle - prepare for drag"""
        if not hasattr(self, '_drag_state'):
            self._drag_state = {}
        self._drag_state['start_y'] = event.y_root
        self._drag_state['dragging'] = False

    def _on_drag_mouse_motion(self, event):
        """Mouse moving with button held - this is a drag"""
        if not hasattr(self, '_drag_state') or self._drag_state.get('start_y') is None:
            return

        # if this is the first motion event, emit drag start
        if not self._drag_state.get('dragging'):
            self._drag_state['dragging'] = True
            self.master.event_generate(
                '<<ItemDragStart>>',
                data={**self._data, 'source_index': self._item_index, 'y_start': self._drag_state['start_y']}
            )

        # emit drag motion event
        self.master.event_generate(
            '<<ItemDragging>>',
            data={
                **self._data,
                'source_index': self._item_index,
                'y_current': event.y_root,
                'y_start': self._drag_state['start_y'],
                'delta_y': event.y_root - self._drag_state['start_y']
            }
        )

    def _on_drag_mouse_up(self, event):
        """Mouse release - end drag if we were dragging"""
        if not hasattr(self, '_drag_state'):
            return

        # only emit drag end if we actually started dragging
        if self._drag_state.get('dragging'):
            self.master.event_generate('<<ItemDragEnd>>',
                                       data={
                                           **self._data,
                                           'source_index': self._item_index,
                                           'y_end': event.y_root,
                                           'y_start': self._drag_state.get('start_y')
                                       })
        # reset drag state
        self._drag_state = {'dragging': False, 'start_y': None}

    def _on_enter(self, event):
        try:
            self.state(['hover'])
        except TclError:
            pass

        for widget in self._composite_widgets:
            try:
                widget.state(['hover'])
            except TclError:
                pass

    def _on_leave(self, event):
        related = getattr(event, 'related', None)

        # Check if we're leaving to another widget within this ListItem
        # If so, don't remove hover state since we're still inside the item
        if related is not None:
            try:
                related_str = str(related)
                self_str = str(self)

                # Check if related widget is a child of this ListItem
                if related_str.startswith(self_str + '.'):
                    return 'break'

                # Also check if related is one of our composite widgets
                for widget in self._composite_widgets:
                    if str(widget) == related_str:
                        return 'break'
            except Exception:
                pass

        # We're truly leaving the ListItem, remove hover from all widgets
        try:
            self.state(['!hover'])
        except TclError:
            pass

        for widget in self._composite_widgets:
            try:
                widget.state(['!hover'])
            except TclError:
                pass
        return None

    def _on_focusin(self, _):
        if not self._enable_focus_state:
            return

        self._set_focus_state(True)
        self._data['focused'] = True
        # notify parent list that item is focused
        self.master.event_generate('<<ItemFocused>>', data=self._data)

    def _on_focusout(self, event):
        if not self._enable_focus_state:
            return None

        # Keep focus styling if focus moved to a descendant of this row
        related = getattr(event, 'related', None)
        try:
            if related is not None and str(related).startswith(str(self)):
                return 'break'
        except TclError:
            pass

        self._set_focus_state(False)
        self._data['focused'] = False
        return None

    def _on_keydown_space(self, _):
        ...

    def _on_mousedown(self, _):
        if self._enable_focus_state:
            self.focus()
        # notify parent list that item has been clicked
        self.master.event_generate('<<ItemClick>>', data=self._data)
        self.select()
        for widget in self._composite_widgets:
            try:
                widget.state(['pressed'])
            except TclError:
                pass

    def _on_mouseup(self, _):
        for widget in self._composite_widgets:
            try:
                widget.state(['!pressed'])
            except TclError:
                pass

    def _set_focus_state(self, focused: bool):
        # helper to apply guaranteed transition to row + composites
        targets = [self, *list(self._composite_widgets)]

        for w in targets:
            try:
                # force a real transition so ttk recomputes maps
                # clear then set, even if we think it's already that value
                w.state(['!focus'])
                if focused:
                    w.state(['focus'])
            except TclError:
                pass

            try:
                # nudge reassign style to force re-resolve
                style = w.cget('style')
                if style:
                    w.configure(style=style)
            except TclError:
                pass

        if focused:
            for w in targets:
                try:
                    w.state(['!active'])
                except TclError:
                    pass

    # --- Configuration delegates ---

    @configure_delegate('selection_mode')
    def _delegate_selection_mode(self, value=None):
        ...

    @configure_delegate('show_selection_controls')
    def _delegate_show_selection_controls(self, value=None):
        ...

    @configure_delegate('selection_background')
    def _delegate_selection_background(self, value=None):
        ...

    @configure_delegate('show_chevron')
    def _delegate_show_chevron(self, value=None):
        ...

    @configure_delegate('enable_dragging')
    def _delegate_enable_dragging(self, value=None):
        ...

    @configure_delegate('enable_deleting')
    def _delegate_enable_deleting(self, value=None):
        ...

    # ---- Public API ----

    def select(self):
        mode = self._selection_mode
        if mode == 'none':
            return None

        is_selected = bool(self.selected or False)
        if is_selected:
            if mode == 'single':
                return None
            self._data['selected'] = False
            self.master.event_generate('<<ItemSelecting>>', data=self._data)
            return False

        self._data['selected'] = True
        self.master.event_generate('<<ItemSelecting>>', data=self._data)
        return True

    def delete(self):
        """Notify subscribers to handle delete action"""
        self.master.event_generate('<<ItemDeleting>>', data=self._data)

    def update_data(self, record: dict | None):
        """Efficiency update row visuals only when values have changed"""
        if record is None or '__empty__' in record:
            self.pack_forget()
            return

        self._data = record
        self._item_index = self._data.get('item_index', 0)

        if self._enable_alternating_rows:
            # TODO configure alternating rows
            ...

        selected = bool(record.get('selected', False))
        if self._state.get('selected') != selected:
            self._update_selection(selected)
            self._state['selected'] = selected

        # handle focus - apply tkinter focus to the widget that should have logical focus
        focused = bool(record.get('focused', False))
        if self._state.get('focused') != focused and self._enable_focus_state:
            if focused:
                # this record should have focus - give tkinter focus to this widget
                try:
                    self.focus_set()
                except TclError:
                    pass
            else:
                # This record lost focus - clear focus styling
                self._set_focus_state(False)
            self._state['focused'] = focused

        # direct update for high-priority visuals
        for field, updater in {
            "title": self._update_title,
            "text": self._update_text,
            "caption": self._update_caption,
            "icon": self._update_icon,
        }.items():
            value = record.get(field)
            if self._state.get(field) != value:
                updater(value)
                self._state[field] = value

        self.after_idle(self._update_chevron)
        self.after_idle(self._update_drag)
        self.after_idle(self._update_delete)
