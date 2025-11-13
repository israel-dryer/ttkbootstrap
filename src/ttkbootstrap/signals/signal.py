import tkinter as tk
import weakref
from itertools import count
from typing import Any, Callable, Generic, Type, TypeVar

from ttkbootstrap.signals.types import TraceOperation

T = TypeVar("T")
U = TypeVar("U")


class _SignalTrace:
    """
    Internal helper to manage Tcl variable traces using tkinter's Variable API.
    This class encapsulates low-level `trace_add` and `trace_remove` logic.
    """

    def __init__(self, tk_var: tk.Variable):
        """
        Initialize a trace manager for a tkinter variable.

        Args:
            tk_var: A tkinter.Variable instance (e.g., StringVar, IntVar).
        """
        self._var = tk_var
        # Map trace id -> (operation, callback)
        self._traces: dict[str, tuple[TraceOperation, Callable[..., Any]]] = {}

    def callbacks(self) -> tuple[str, ...]:
        """
        Return all currently active trace IDs.

        Returns:
            A tuple of trace ID strings.
        """
        return tuple(self._traces.keys())

    def add(
            self,
            operation: TraceOperation,
            callback: Callable[[T], Any],
            get_value: Callable[[], T],
    ) -> str:
        """
        Add a new trace that calls a callback when the variable is written.
        """

        def traced_callback(name: str, index: str, mode: str) -> None:
            callback(get_value())

        try:
            fid = self._var.trace_add(operation, traced_callback)
        except tk.TclError as e:
            raise RuntimeError(f"failed to add trace: {e}") from e
        self._traces[fid] = (operation, traced_callback)
        return fid

    def remove(self, fid: str) -> None:
        """
        Remove a trace by ID. Safe if already removed or variable destroyed.
        """
        op_cb = self._traces.pop(fid, None)
        if op_cb is None:
            return
        operation, _ = op_cb
        try:
            self._var.trace_remove(operation, fid)
        except tk.TclError:
            # Variable may be unset/destroyed; ignore
            pass


class Signal(Generic[T]):
    """
    A reactive signal backed by a tkinter Variable.

    Supports value access, transformation via `.map()`, and subscription
    to change events via `.subscribe()`.

    Can be passed to Tkinter widgets using `str(signal)` or `signal.name`.
    """

    _cnt = count(1)

    def __init__(self, value: T, name: str | None = None, master: tk.Misc | None = None):
        self._name = name or f"SIG{next(self._cnt)}"
        self._type: Type[T] = type(value)
        self._master: tk.Misc | None = master
        self._var = self._create_variable(value)
        self._trace = _SignalTrace(self._var)
        # Map fid -> callback to allow multiple subscriptions of same function
        self._subscribers: dict[str, Callable[[T], Any]] = {}
        # Reverse index: callback -> set of fids
        self._callback_index: dict[Callable[[T], Any], set[str]] = {}
        # Cache last known value for robustness when Tcl variable is torn down
        self._last: T = value

    def _create_variable(self, value: T) -> tk.Variable:
        if isinstance(value, bool):
            return tk.BooleanVar(master=self._master, name=self._name, value=value)
        elif isinstance(value, int):
            return tk.IntVar(master=self._master, name=self._name, value=value)
        elif isinstance(value, float):
            return tk.DoubleVar(master=self._master, name=self._name, value=value)
        else:
            return tk.StringVar(master=self._master, name=self._name, value=value)

    def __call__(self) -> T:
        """
        Get the current value of the signal.

        Returns:
            The current typed value.
        """
        try:
            value = self._var.get()
            self._last = value  # cache last good value
            return value
        except tk.TclError:
            # Return last known value when underlying var is destroyed/unset
            return self._last

    def get(self) -> T:
        """Return the current value of the signal.

        Alias for calling the instance directly (``signal()``). Mirrors
        tkinter's ``Variable.get`` naming for consistency.
        """
        return self()

    @classmethod
    def from_variable(
            cls,
            tk_var: tk.Variable,
            *,
            name: str | None = None,
            coerce: Type[T] | None = None,
    ) -> "Signal[T]":
        """
        Wrap an existing tkinter Variable as a Signal.

        Args:
            tk_var: An existing tkinter.Variable instance (StringVar, IntVar, etc.).
            name: Optional override of the Tcl variable name. Defaults to tk_var's name.
            coerce: Optional Python type to treat the signal as (e.g., int/float/bool/str).
                    If omitted, the type is inferred from the tk_var subclass.

        Returns:
            A Signal bound to the provided tk_var.
        """
        # Infer Python type from the tk variable if not explicitly provided
        if coerce is None:
            if isinstance(tk_var, tk.BooleanVar):
                py_type: Type[Any] = bool
            elif isinstance(tk_var, tk.IntVar):
                py_type = int
            elif isinstance(tk_var, tk.DoubleVar):
                py_type = float
            else:
                py_type = str
        else:
            py_type = coerce

        # Construct without creating a new tk.Variable
        self = cls.__new__(cls)  # bypass __init__
        self._name = name or getattr(tk_var, "_name", str(tk_var))
        self._type = py_type  # type: ignore[assignment]
        self._var = tk_var
        self._trace = _SignalTrace(self._var)
        self._subscribers = {}
        self._callback_index = {}
        # Best-effort capture of master/interpreter for reference
        self._master = getattr(tk_var, "_master", None)
        try:
            current = tk_var.get()  # type: ignore[assignment]
        except tk.TclError:
            # Fallback default per inferred type
            if py_type is float:  # type: ignore[comparison-overlap]
                current = 0.0
            elif py_type is int:  # type: ignore[comparison-overlap]
                current = 0
            elif py_type is bool:  # type: ignore[comparison-overlap]
                current = False
            else:
                current = ""
        self._last = current  # type: ignore[assignment]
        return self

    def set(self, value: T) -> None:
        """
        Set the signal to a new value and notify subscribers.

        Args:
            value: The new value. Must match the original type.

        Raises:
            TypeError: If the value type does not match the original.
        """
        # Enforce exact type to avoid bool being accepted for int, etc.
        if type(value) is not self._type:
            raise TypeError(f"Expected {self._type.__name__}, got {type(value).__name__}")
        # Reduce redundant updates if value unchanged
        try:
            current = self._var.get()
            if current == value:
                return
        except tk.TclError:
            # If var is gone, proceed to set and let Tcl recreate path if possible
            pass
        self._var.set(value)
        self._last = value

    def map(self, transform: Callable[[T], U]) -> 'Signal[U]':
        """
        Create a derived signal that transforms this signal's value.

        Args:
            transform: A function applied to the current and future values.

        Returns:
            A new Signal[U] that stays updated with the transformed value.
        """
        derived = Signal(transform(self()))

        # Use weakref to avoid keeping derived alive solely via subscription
        weak_derived = weakref.ref(derived)

        def update(value: T) -> None:
            d = weak_derived()
            if d is None:
                # Auto-detach if derived is GC'd
                return
            d.set(transform(value))

        self.subscribe(update)
        return derived

    def subscribe(self, callback: Callable[[T], Any], *, immediate: bool = False) -> str:
        """
        Subscribe to value changes of this signal.

        Args:
            callback: A function that receives the current value (T) when updated.

        Returns:
            A trace ID that can be used for removal.
        """
        fid = self._trace.add("write", callback, self)
        self._subscribers[fid] = callback
        self._callback_index.setdefault(callback, set()).add(fid)
        if immediate:
            try:
                callback(self())
            except Exception:
                # Do not fail subscription due to callback error
                pass
        return fid

    def unsubscribe(self, callback: Callable[[T], Any]) -> None:
        """
        Remove a previously registered subscriber.

        Args:
            callback: The function originally passed to `subscribe()`.
        """
        fids = self._callback_index.pop(callback, set())
        for fid in fids:
            self._subscribers.pop(fid, None)
            self._trace.remove(fid)

    def unsubscribe_all(self) -> None:
        """
        Remove all currently subscribed callbacks.
        """
        # Copy keys to avoid mutation during iteration
        for fid in list(self._subscribers.keys()):
            self._trace.remove(fid)
        self._subscribers.clear()
        self._callback_index.clear()

    def __getattr__(self, name: str) -> Any:
        """
        Proxy access to the underlying tk.Variable instance.
        """
        return getattr(self._var, name)

    @property
    def name(self) -> str:
        """
        Return the Tcl name of the variable (for use in widget `textvariable`).
        """
        return self._name

    @property
    def type(self) -> Type[T]:
        """
        The original type of the signal value.

        Returns:
            A Python type (e.g., int, str).
        """
        return self._type

    @property
    def var(self) -> tk.Variable:
        return self._var

    def __str__(self) -> str:
        return self._name

    def __repr__(self) -> str:
        return self._name
