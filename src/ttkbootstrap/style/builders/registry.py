"""Private registry for ttk widget-family style recipes."""

from collections.abc import Callable
from typing import Any


DEFAULT_VARIANT = "default"
BuilderKey = tuple[str, str]
BuilderRecipe = Callable[[Any, str], None]


class BuilderRegistryError(RuntimeError):
    """Base error for invalid private builder-registry operations."""


class DuplicateBuilderError(BuilderRegistryError):
    """Raised when two recipes claim the same registry key."""


class FrozenBuilderRegistryError(BuilderRegistryError):
    """Raised when registration is attempted after loading completes."""


class BuilderRegistry:
    """Mutable-during-import registry that freezes after explicit loading."""

    def __init__(self) -> None:
        self._builders: dict[BuilderKey, BuilderRecipe] = {}
        self._frozen = False

    @staticmethod
    def _key(variant: str, widget_family: str) -> BuilderKey:
        for label, value in (
            ("variant", variant),
            ("widget_family", widget_family),
        ):
            if (
                not isinstance(value, str)
                or not value
                or value != value.strip()
                or value != value.lower()
            ):
                raise BuilderRegistryError(
                    f"{label} must be a non-empty canonical lowercase string"
                )
        return variant, widget_family

    def register(self, variant: str, widget_family: str):
        """Return a decorator registering one exact private builder key."""
        key = self._key(variant, widget_family)

        def decorator(recipe: BuilderRecipe) -> BuilderRecipe:
            if not callable(recipe):
                raise BuilderRegistryError(
                    f"builder for {key!r} must be callable"
                )
            if self._frozen:
                raise FrozenBuilderRegistryError(
                    f"builder registry is frozen; cannot register {key!r}"
                )
            previous = self._builders.get(key)
            if previous is not None:
                raise DuplicateBuilderError(
                    f"builder key {key!r} is already registered by "
                    f"{previous.__module__}.{previous.__qualname__}; attempted "
                    f"{recipe.__module__}.{recipe.__qualname__}"
                )
            self._builders[key] = recipe
            return recipe

        return decorator

    def get(
        self, variant: str, widget_family: str
    ) -> BuilderRecipe | None:
        """Return the recipe for a canonical key, if registered."""
        return self._builders.get(self._key(variant, widget_family))

    def keys(self) -> frozenset[BuilderKey]:
        """Return an immutable snapshot of all registered keys."""
        return frozenset(self._builders)

    def freeze(self) -> None:
        """Reject all subsequent registration attempts."""
        self._frozen = True

    @property
    def frozen(self) -> bool:
        """Whether loading completed and registration is closed."""
        return self._frozen


_REGISTRY = BuilderRegistry()
register_builder = _REGISTRY.register


def get_builder(
    variant: str, widget_family: str
) -> BuilderRecipe | None:
    """Return a recipe from the process-wide private registry."""
    return _REGISTRY.get(variant, widget_family)


def builder_keys() -> frozenset[BuilderKey]:
    """Return a snapshot of the process-wide registry keys."""
    return _REGISTRY.keys()


def freeze_registry() -> None:
    """Freeze the process-wide registry after all explicit imports."""
    _REGISTRY.freeze()


def registry_is_frozen() -> bool:
    """Return whether the process-wide registry is frozen."""
    return _REGISTRY.frozen
