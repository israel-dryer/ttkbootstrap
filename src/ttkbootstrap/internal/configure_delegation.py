"""Configure/cget delegation for ttkbootstrap's custom widgets.

Custom widgets (Meter, Floodgauge, DateEntry, ...) add their own options on top
of a real ttk/tk widget. Historically each hand-maintained two parallel `if/else`
ladders — one in a `configure` override to *set*, one to *get* — and often forgot
a `cget` override entirely, so an option could be set but never read back (or a
construction-only option had no `configure` branch at all). Those ladders are
where the round-trip bugs live.

This mixin replaces them. A widget marks one method per option with
`@configure_delegate("name")`; `__init_subclass__` collects every such method in
the MRO into a `key -> handler` map at class-creation time; and `configure`,
`config`, `cget`, `keys`, `__getitem__`, and `__setitem__` all route delegated
keys through that map (returning proper Tk 5-tuple specs), falling back to the
real widget for everything else. A single handler serves both directions:

```python
class Meter(ConfigureDelegationMixin, Frame):
    @configure_delegate("amountused")
    def _amountused(self, value):
        if value is None:                 # query
            return self._amountusedvar.get()
        self._amountusedvar.set(value)    # set
```

`cget("amountused")`, `configure("amountused")`, `meter["amountused"]`,
`configure(amountused=…)`, and `meter["amountused"] = …` now all work and stay in
sync, with no ladder to keep aligned.

**Inner-widget fallthrough** (the piece bootstack's original lacks): a composite
that proxies to an inner widget — e.g. `ScrolledText` wrapping a `Text` — can
override `_configure_delegate_target()` to return that inner widget. Non-delegated
options then route to it instead of the outer frame, so `st.configure(font=…)` /
`st.cget("wrap")` reach the `Text`. The default returns `None` (use the widget
itself), which is what the non-composite widgets want.

This module is internal (`ttkbootstrap.internal`): no back-compat guarantee.
"""
from __future__ import annotations

from typing import Any, Callable

# Marker attribute stamped on a delegate method by the decorator. Namespaced to
# ttkbootstrap so it never collides with a real attribute or bootstack's marker.
_DELEGATE_KEYS_ATTR = "_tb_configure_keys"


def configure_delegate(*names: str) -> Callable[[Callable], Callable]:
    """Mark a method as the get/set handler for one or more configure options.

    The decorated method takes a single ``value`` argument: called with ``None``
    it returns the option's current value (query); called with a value it applies
    it (set). Registering several names on one method is allowed (aliases).
    """
    def _decorator(func: Callable) -> Callable:
        keys = set(getattr(func, _DELEGATE_KEYS_ATTR, ()))
        keys.update(names)
        setattr(func, _DELEGATE_KEYS_ATTR, tuple(keys))
        return func

    return _decorator


class ConfigureDelegationMixin:
    """Dispatch delegated configure/cget keys to `@configure_delegate` handlers.

    Place it **before** the base widget in the bases, e.g.
    ``class Meter(ConfigureDelegationMixin, Frame)`` — so its `configure`/`cget`
    resolve first and delegate to `super()` (the real widget) for everything they
    do not own.
    """

    #: key -> handler-method-name, built per subclass in __init_subclass__.
    _configure_delegate_map: dict[str, str] = {}

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        mapping: dict[str, str] = {}
        # Reversed MRO so a subclass override of a delegate wins over its base.
        for base in reversed(cls.__mro__):
            for name, member in getattr(base, "__dict__", {}).items():
                keys = getattr(member, _DELEGATE_KEYS_ATTR, None)
                if keys:
                    for key in keys:
                        mapping[str(key)] = name
        cls._configure_delegate_map = mapping

    # -- extension point ----------------------------------------------------- #
    def _configure_delegate_target(self):
        """Widget that receives *non-delegated* options, or ``None`` for ``self``.

        Override in a composite to proxy pass-through options to an inner widget
        (e.g. `ScrolledText` returning its inner `Text`). The default keeps the
        base-widget behavior (route to ``super()``).
        """
        return None

    # -- delegation core ----------------------------------------------------- #
    def _config_delegate_set(self, key: str, value: Any) -> bool:
        method_name = self._configure_delegate_map.get(key)
        if method_name is None:
            return False
        getattr(self, method_name)(value)
        return True

    def _config_delegate_get(self, key: str) -> tuple[bool, Any]:
        method_name = self._configure_delegate_map.get(key)
        if method_name is None:
            return False, None
        value = getattr(self, method_name)(None)
        # A tk Variable renders as its Tcl name, matching cget() on a real option.
        if key in ("variable", "textvariable") and hasattr(value, "_name"):
            return True, str(value)
        return True, value

    @staticmethod
    def _spec(key: str, value: Any) -> tuple:
        """A Tk configure spec: (name, dbName, dbClass, default, current)."""
        return (key, key, key.capitalize(), None, value)

    # -- public tk-style surface --------------------------------------------- #
    def configure(self, cnf: Any = None, **kwargs: Any) -> Any:
        if isinstance(cnf, dict):
            kwargs = {**cnf, **kwargs}
            cnf = None

        if kwargs:
            for key in list(kwargs):
                if key in self._configure_delegate_map:
                    self._config_delegate_set(key, kwargs.pop(key))
            if kwargs:
                target = self._configure_delegate_target()
                if target is not None:
                    target.configure(**kwargs)
                else:
                    super().configure(**kwargs)
            return None

        if isinstance(cnf, str):
            if cnf in self._configure_delegate_map:
                _, value = self._config_delegate_get(cnf)
                return self._spec(cnf, value)
            target = self._configure_delegate_target()
            if target is not None:
                return target.configure(cnf)
            return super().configure(cnf)

        # No-arg query: full option dict, with the delegated options merged in.
        base = super().configure() or {}
        for key in self._configure_delegate_map:
            _, value = self._config_delegate_get(key)
            base[key] = self._spec(key, value)
        return base

    config = configure

    def cget(self, key: str) -> Any:
        if key in self._configure_delegate_map:
            _, value = self._config_delegate_get(key)
            return value
        target = self._configure_delegate_target()
        if target is not None:
            return target.cget(key)
        return super().cget(key)

    def __setitem__(self, key: str, value: Any) -> None:
        if self._config_delegate_set(key, value):
            return
        target = self._configure_delegate_target()
        if target is not None:
            target[key] = value
        else:
            super().__setitem__(key, value)

    def __getitem__(self, key: str) -> Any:
        if key in self._configure_delegate_map:
            _, value = self._config_delegate_get(key)
            return value
        target = self._configure_delegate_target()
        if target is not None:
            return target[key]
        return super().__getitem__(key)

    def keys(self) -> list:
        """Option names, including the delegated custom options (for discovery)."""
        try:
            names = list(super().keys())
        except AttributeError:
            names = []
        for key in self._configure_delegate_map:
            if key not in names:
                names.append(key)
        return names


__all__ = ["configure_delegate", "ConfigureDelegationMixin"]
