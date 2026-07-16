"""Backport of tkinter's busy methods for Python < 3.13.

Tk's ``tk busy`` command covers a widget with a transparent window that blocks
pointer events and shows a busy cursor. The command is Tk 8.6, so it is
available on every Python ttkbootstrap supports -- but tkinter only grew the
``busy``/``tk_busy_*`` method wrappers in **3.13**. On 3.10-3.12 they don't
exist at all, leaving `tk.call` reach-ins as the only way to use it.

`BusyMixin` closes that gap: it delegates to tkinter's own methods where they
exist, and issues the identical `tk.call` where they don't, so the same code
runs on every supported Python.

`tk busy` is not supported on macOS (aqua): the calls succeed and `busy_status`
reports True, but nothing is drawn or blocked.
"""
from tkinter import _cnfmerge


class BusyMixin:
    """Give a widget the tkinter busy methods on every supported Python.

    Mixed into the ttkbootstrap widget classes and into `App`/`Toplevel`, so
    `app.busy(cursor="watch")` works on Python 3.10 as it does on 3.13+.

    Each method prefers tkinter's native implementation when it is available
    (3.13+), falling back to the same underlying Tcl call otherwise. The
    signatures, aliases, and return types mirror tkinter's exactly.
    """

    def _busy_native(self, name):
        """Return tkinter's own busy method, or None on Python < 3.13.

        Looked up along the MRO *past* this mixin, so it finds `tkinter.Misc`'s
        implementation rather than recursing into ours.
        """
        return getattr(super(), name, None)

    def tk_busy_hold(self, **kw):
        """Make this widget appear busy.

        The specified widget and its descendants will be blocked from user
        interactions. Normally `update` should be called immediately afterward
        to insure that the hold operation is in effect before the application
        starts its processing.

        The only supported configuration option is:

            cursor: the cursor to be displayed when the widget is made busy.
        """
        native = self._busy_native('tk_busy_hold')
        if native is not None:
            return native(**kw)
        self.tk.call('tk', 'busy', 'hold', self._w, *self._options(kw))

    busy = busy_hold = tk_busy = tk_busy_hold

    def tk_busy_forget(self):
        """Make this widget no longer busy.

        User events will again be received by the widget.
        """
        native = self._busy_native('tk_busy_forget')
        if native is not None:
            return native()
        self.tk.call('tk', 'busy', 'forget', self._w)

    busy_forget = tk_busy_forget

    def tk_busy_status(self):
        """Return True if the widget is busy, False otherwise."""
        native = self._busy_native('tk_busy_status')
        if native is not None:
            return native()
        return self.tk.getboolean(self.tk.call(
            'tk', 'busy', 'status', self._w))

    busy_status = tk_busy_status

    def tk_busy_current(self, pattern=None):
        """Return a list of widgets that are currently busy.

        If a pattern is given, only busy widgets whose path names match a
        pattern are returned.
        """
        native = self._busy_native('tk_busy_current')
        if native is not None:
            return native(pattern)
        return [self._nametowidget(x) for x in
                self.tk.splitlist(self.tk.call(
                    'tk', 'busy', 'current', pattern))]

    busy_current = tk_busy_current

    def tk_busy_cget(self, option):
        """Return the value of a busy configuration option.

        The widget must have been previously made busy by `tk_busy_hold`.
        Option may have any of the values accepted by `tk_busy_hold`.
        """
        native = self._busy_native('tk_busy_cget')
        if native is not None:
            return native(option)
        return self.tk.call('tk', 'busy', 'cget', self._w, '-' + option)

    busy_cget = tk_busy_cget

    def tk_busy_configure(self, cnf=None, **kw):
        """Query or modify the busy configuration options.

        The widget must have been previously made busy by `tk_busy_hold`.
        Options may have any of the values accepted by `tk_busy_hold`.
        """
        native = self._busy_native('tk_busy_configure')
        if native is not None:
            return native(cnf, **kw)
        if kw:
            cnf = _cnfmerge((cnf, kw))
        elif cnf:
            cnf = _cnfmerge(cnf)
        if cnf is None:
            return self._getconfigure('tk', 'busy', 'configure', self._w)
        if isinstance(cnf, str):
            return self._getconfigure1(
                'tk', 'busy', 'configure', self._w, '-' + cnf)
        self.tk.call('tk', 'busy', 'configure', self._w, *self._options(cnf))

    busy_config = busy_configure = tk_busy_config = tk_busy_configure