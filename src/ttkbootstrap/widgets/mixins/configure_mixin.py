"""Configuration delegation helpers for widget classes.

Provides a decorator and mixin so widgets can handle custom configure keys
without large if/else blocks. Suited for use by ttkbootstrap wrapper
subclasses and custom widgets.
"""

from __future__ import annotations

from typing import Any, Callable, Dict, Tuple


def configure_delegate(*names: str):
    """Decorator to mark a method as a configure handler for given names.

    The decorated method should accept a single argument `value` which will be
    the value provided via configure(..., name=value). If `value` is None, the
    method should return the current value for queries (configure(cnf=name)).
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
        return True, handler(None)


__all__ = ["configure_delegate", "ConfigureDelegationMixin"]
