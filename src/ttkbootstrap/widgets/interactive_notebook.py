"""
    An interactive Notebook widget that has buttons to close or add tabs.

    Author: Daniil Soloviev
    Modified: 2021-09-08

    Based on https://stackoverflow.com/questions/39458337/is-there-a-way-to-add-close-buttons-to-tabs-in-tkinter-ttk-notebook/39459376#39459376
"""
from tkinter import ttk, TclError


class InteractiveNotebook(ttk.Notebook):
    """A custom version of the ttk.Notebook widget which includes a close button on each tab,
    and a button to create new tabs. Unlike the default Notebook widget, it does not support
    the 'disabled' state for tabs."""

    # A constant determining how many spaces of padding to add to each tab title.
    _padding_spaces = 3

    def __init__(self, *args, **kwargs):
        """Arguments different from ttk.Notebook:
            style (str): should be in the form [color.][Flat.]Interactive.Tnotebook. Set to Interactive.TNotebook by default.
            newtab (function): if provided, the notebook will include a 'new tab' button, which calls this function when pressed.
        For the other arguments, see https://docs.python.org/3/library/tkinter.ttk.html#ttk-notebook
        """
        if 'style' not in kwargs:
            kwargs['style'] = 'Interactive.TNotebook'

        self._has_newtab_button = ('newtab' in kwargs)
        if self._has_newtab_button:
            self._newtab_callback = kwargs.pop('newtab')

        super().__init__(*args, **kwargs)

        self._last_pressed = None

        self.bind('<ButtonPress-1>', self._on_close_press, True)
        self.bind('<ButtonRelease-1>', self._on_close_release)
        self.bind('<ButtonPress-2>', self._on_close_press, True)
        self.bind('<ButtonRelease-2>', self._on_close_release)

        if self._has_newtab_button:
            self._create_newtab()

    @property
    def _last_tab(self):
        """Returns the index of the last tab"""
        return self.index('end') - 1

    def _create_newtab(self):
        self._newtab_frame = ttk.Frame(self)
        super().add(self._newtab_frame, state='disabled')

    def add(self, child, *args, **kwargs):
        if 'text' in kwargs:
            kwargs['text'] += ' ' * self._padding_spaces

        try:
            self.index(child)
            # child already part of notebook, add() should unhide it
            super().add(child, *args, **kwargs)
        except TclError:
            # child not yet part of notebook, so insert it before the newtab button if it exists
            if self._has_newtab_button:
                super().insert(self._newtab_frame, child, *args, **kwargs)
            else:
                super().add(child, *args, **kwargs)

    def insert(self, *args, **kwargs):
        if 'text' in kwargs:
            kwargs['text'] += ' ' * self._padding_spaces
        super().insert(*args, **kwargs)

    def _on_close_press(self, event):
        element = self.identify(event.x, event.y)
        if element == '':
            # click happened outside of any tabs
            self._last_pressed = None
            return

        index = self.index(f'@{event.x},{event.y}')

        newtab_hit = (index == self._last_tab and self._has_newtab_button)

        if (
            (event.num == 1 and (('closebutton' in element) or newtab_hit))
            or (event.num == 2 and not newtab_hit)
        ):
            self.state(['pressed'])
            self._last_pressed = index
            return 'break'  # to prevent selecting the tab

    def _on_close_release(self, event):
        if not self.instate(['pressed']):
            return

        self.state(['!pressed'])

        element = self.identify(event.x, event.y)
        if element == '':
            # mouse was released outside of any tabs
            self._last_pressed = None
            return

        index = self.index(f'@{event.x},{event.y}')

        newtab_hit = (index == self._last_tab and self._has_newtab_button)

        if self._last_pressed == index:
            if event.num == 1 and newtab_hit:
                # new tab button was pressed
                self._newtab_callback()
            # for the close button, the click position has to be more accurate
            elif ((event.num == 1 and 'closebutton' in element)
                  or (event.num == 2 and not newtab_hit)
                  ):
                # a close tab button was pressed
                self.forget(index)
