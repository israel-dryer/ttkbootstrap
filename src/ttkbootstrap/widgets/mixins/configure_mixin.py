"""Configuration delegation helpers for widget classes.

Provides a decorator and mixin so widgets can handle custom configure keys
without large if/else blocks. Suited for use by ttkbootstrap wrapper
subclasses and custom widgets.
"""

from __future__ import annotations

from typing import Any, Callable, Dict, Tuple


def configure_delegate(*names: str):
    """Decorator to mark a method as a configure handler for given names.

    The decorated method should accept a single argument `value` to set,
    and optionally return None. For getting values, the mixin will read
    from self._<option_name> directly.
    """

    def _decorator(func: Callable[[Any, Any], Any]):
        keys = set(getattr(func, "_ttkbootstrap_configure_keys", ()))
        keys.update(names)
        setattr(func, "_ttkbootstrap_configure_keys", tuple(keys))
        return func

    return _decorator


class ConfigureDelegationMixin:
    """Mix-in that dispatches configure keys to decorated handlers.

    Subclasses can annotate methods with @configure_delegate("key") to handle
    custom configuration entries without if/else chains.
    """

    _configure_delegate_map: Dict[str, str] = {}

    def __init_subclass__(cls, **kwargs: Any) -> None:  # noqa: D401
        super().__init_subclass__(**kwargs)
        mapping: Dict[str, str] = {}
        for base in reversed(cls.__mro__):
            for name, member in getattr(base, "__dict__", {}).items():
                keys = getattr(member, "_ttkbootstrap_configure_keys", None)
                if keys:
                    for k in keys:
                        mapping[str(k)] = name
        cls._configure_delegate_map = mapping

    def _config_delegate_set(self, key: str, value: Any) -> bool:
        method_name = self._configure_delegate_map.get(key)
        if not method_name:
            return False
        handler = getattr(self, method_name)
        handler(value)
        return True

    def _config_delegate_get(self, key: str) -> Tuple[bool, Any]:
        method_name = self._configure_delegate_map.get(key)
        if not method_name:
            return False, None
        handler = getattr(self, method_name)
        value = handler(None)
        # For variable options, return the string name instead of the object
        if key in ('variable', 'textvariable') and hasattr(value, '_name'):
            return True, str(value)
        return True, value

    def configure(self, cnf=None, **kwargs):
        """Configure widget options, handling custom delegated options first."""
        # Handle custom delegated keys
        if kwargs:
            for _k in list(kwargs.keys()):
                if _k in self._configure_delegate_map:
                    if self._config_delegate_set(_k, kwargs[_k]):
                        kwargs.pop(_k, None)

        # Getter path for delegated keys
        if isinstance(cnf, str) and cnf in self._configure_delegate_map:
            handled, value = self._config_delegate_get(cnf)
            if handled:
                # Return in standard Tkinter format: (name, dbName, dbClass, default, current)
                return (cnf, cnf, cnf.capitalize(), None, value)

        # Forward remaining options to parent
        return super().configure(cnf, **kwargs)

    config = configure

    def __setitem__(self, key, value):
        """Set configuration option via indexing."""
        if key in self._configure_delegate_map:
            self._config_delegate_set(key, value)
            return
        return super().__setitem__(key, value)

    def __getitem__(self, key):
        """Get configuration option via indexing."""
        if key in self._configure_delegate_map:
            handled, value = self._config_delegate_get(key)
            if handled:
                return value
        return super().__getitem__(key)

    def cget(self, key):
        """Get configuration option."""
        if key in self._configure_delegate_map:
            handled, value = self._config_delegate_get(key)
            if handled:
                return value
        return super().cget(key)


__all__ = ["configure_delegate", "ConfigureDelegationMixin"]
