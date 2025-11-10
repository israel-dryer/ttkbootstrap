from __future__ import annotations

import re
import threading
from typing import Callable, Dict, Optional

from typing_extensions import Any, ParamSpec, Protocol, TypeVar

from ttkbootstrap.exceptions import BootstyleBuilderError
from ttkbootstrap.style.element import Element, ElementImage
from ttkbootstrap.style.theme_provider import ThemeProvider
from ttkbootstrap.style.bootstyle_builder_base import BootstyleBuilderBase


class BuilderCallable(Protocol):
    def __call__(self, builder: BootstyleBuilderBuilderTTk, ttk_style: str, **options: Any) -> None:
        ...


F = TypeVar("F", bound=BuilderCallable)
P = ParamSpec("P")
R = TypeVar("R")

from ttkbootstrap.style.token_maps import WIDGET_CLASS_MAP, WIDGET_NAME_MAP

# Default variant name used when no variant is specified
# Builders should register under both their specific name AND 'default'
# Example:
#   @BootstyleBuilder.register_builder('solid', 'TButton')
#   @BootstyleBuilder.register_builder('default', 'TButton')
#   def build_button_solid(builder, ttk_style, **options):
#       ...
DEFAULT_VARIANT = 'default'


class BootstyleBuilderBuilderTTk(BootstyleBuilderBase):
    """Builder manager with widget-specific style builder registry.

    This class manages registration and invocation of style builder functions.
    Builders are registered per-widget-class and variant.

    Registry structure:
        {
            'TButton': {
                'solid': builder_func,
                'outline': builder_func,
                ...
            },
            'TLabel': {
                'solid': builder_func,
                'inverse': builder_func,
                ...
            }
        }
    """

    # Widget-specific builder registry: {widget_class: {variant: builder_func}}
    _builder_registry: Dict[str, Dict[str, Callable]] = {}
    _builder_lock = threading.Lock()
    _builders_loaded = False  # Track if builders have been auto-imported

    def __init__(
            self, theme_provider: Optional[ThemeProvider] = None,
            style_instance: Optional[Any] = None):
        """Initialize the BootstyleBuilder.

        Args:
            theme_provider: Optional ThemeProvider instance (creates one if None)
            style_instance: Optional Style instance (set later to avoid circular import)
        """
        super().__init__(theme_provider, style_instance)

    def set_style_instance(self, style_instance: Any):
        """Set the Style instance (avoids circular import in __init__).

        Args:
            style_instance: Style instance to use for configuration
        """
        self._style = style_instance

    # provider, style, colors inherited from BootstyleBase

    @classmethod
    def register_builder(cls, variant: str, widget_class: str):
        """Register a builder for a specific widget variant.

        Args:
            variant: Variant name (e.g., 'solid', 'outline', 'link')
            widget_class: TTK widget class (e.g., 'TButton', 'TLabel')

        Returns:
            Decorator function

        Raises:
            BootstyleBuilderError: If variant or widget_class invalid

        Example:
            >>> @BootstyleBuilderBuilderTTk.register_builder('outline', 'TButton')
            ... def build_button_outline(builder, ttk_style, **options):
            ...     # Builder implementation
            ...     pass
        """
        if not isinstance(variant, str) or not variant:
            raise BootstyleBuilderError("`variant` must be a non-empty string")

        if not isinstance(widget_class, str) or not widget_class:
            raise BootstyleBuilderError("`widget_class` must be a non-empty string")

        def deco(func: F) -> F:
            with cls._builder_lock:
                if widget_class not in cls._builder_registry:
                    cls._builder_registry[widget_class] = {}

                if variant not in cls._builder_registry[widget_class]:
                    cls._builder_registry[widget_class][variant] = func
                else:
                    # Warn about overwriting?
                    cls._builder_registry[widget_class][variant] = func

            return func

        return deco

    def call_builder(
            self, widget_class: str, variant: str, ttk_style: str,
            color: Optional[str] = None, **options):
        """Call a registered builder for a specific widget variant.

        Args:
            widget_class: TTK widget class (e.g., 'TButton')
            variant: Variant name (e.g., 'outline')
            ttk_style: Full TTK style name
            color: Optional color token (passed directly to builder)
            **options: Custom style options

        Raises:
            BootstyleBuilderError: If builder not found
        """
        # Ensure builders are loaded before accessing registry
        BootstyleBuilderBuilderTTk._ensure_builders_loaded()

        with BootstyleBuilderBuilderTTk._builder_lock:
            widget_registry = BootstyleBuilderBuilderTTk._builder_registry.get(widget_class)

            if not widget_registry:
                raise BootstyleBuilderError(
                    f"No builders registered for widget class '{widget_class}'"
                )

            builder_func = widget_registry.get(variant)

            if not builder_func:
                available = ', '.join(widget_registry.keys())
                raise BootstyleBuilderError(
                    f"Builder '{variant}' not found for widget class '{widget_class}'. "
                    f"Available variants: {available}"
                )

            # Pass parsed color directly to builder
            # No need to pass variant - the builder itself is variant-specific
            builder_func(self, ttk_style, color=color, **options)

    @classmethod
    def get_widget_class(cls, widget_name: str) -> str:
        """Convert widget common name to TTK class name.

        Args:
            widget_name: Common widget name (e.g., 'button')

        Returns:
            TTK class name (e.g., 'TButton')

        Raises:
            ValueError: If widget name not recognized
        """
        if widget_name not in WIDGET_CLASS_MAP:
            raise ValueError(
                f"Unknown widget name: '{widget_name}'. "
                f"Known names: {', '.join(WIDGET_CLASS_MAP.keys())}"
            )
        return WIDGET_CLASS_MAP[widget_name]

    @classmethod
    def get_widget_name(cls, widget_class: str) -> str:
        """Convert TTK class name to common widget name.

        Args:
            widget_class: TTK class name (e.g., 'TButton')

        Returns:
            Common widget name (e.g., 'button')

        Raises:
            ValueError: If widget class not recognized
        """
        if widget_class not in WIDGET_NAME_MAP:
            raise ValueError(
                f"Unknown widget class: '{widget_class}'. "
                f"Known classes: {', '.join(WIDGET_NAME_MAP.keys())}"
            )
        return WIDGET_NAME_MAP[widget_class]

    @classmethod
    def get_default_variant(cls, widget_class: str = None) -> str:
        """Get the default variant name.

        The default variant is 'default'. Builders should register under
        both their specific variant name and 'default' to be used as the
        default for their widget class.

        Args:
            widget_class: TTK widget class (unused, kept for compatibility)

        Returns:
            Default variant name ('default')

        Example:
            >>> @BootstyleBuilderBuilderTTk.register_builder('solid', 'TButton')
            ... @BootstyleBuilderBuilderTTk.register_builder('default', 'TButton')
            ... def build_button_solid(builder, ttk_style, **options):
            ...     pass
        """
        return DEFAULT_VARIANT

    @classmethod
    def get_registered_builders(cls, widget_class: str) -> list:
        """Get list of registered builders for a widget class.

        Args:
            widget_class: TTK widget class

        Returns:
            List of variant names
        """
        cls._ensure_builders_loaded()
        registry = cls._builder_registry.get(widget_class, {})
        return list(registry.keys())

    @classmethod
    def get_all_registered_widgets(cls) -> list:
        """Get list of all widget classes with registered builders.

        Returns:
            List of TTK widget class names
        """
        cls._ensure_builders_loaded()
        return list(cls._builder_registry.keys())

    @classmethod
    def _ensure_builders_loaded(cls):
        """Ensure builders module is loaded (lazy import).

        This is called automatically when registry is accessed to ensure
        all builder functions are registered before use.
        """
        # Fast path - no lock needed if already loaded
        if cls._builders_loaded:
            return

        # Use a simple flag to prevent multiple imports
        # We check WITHOUT holding the lock to avoid deadlock
        if not cls._builders_loaded:
            try:
                # Import builders module WITHOUT holding the lock
                # This allows the builders to register themselves (which needs the lock)
                import ttkbootstrap.style.builders  # noqa: F401
                cls._builders_loaded = True
            except ImportError:
                # Builders module doesn't exist yet, that's ok
                cls._builders_loaded = True  # Set to avoid retrying
            except Exception:
                # Unexpected error, but set flag to avoid infinite retries
                cls._builders_loaded = True

    @classmethod
    def has_builder(cls, widget_class: str, variant: str) -> bool:
        """Check if a builder exists for widget class and variant.

        Args:
            widget_class: TTK widget class (e.g., 'TButton')
            variant: Variant name (e.g., 'solid', 'outline')

        Returns:
            True if builder exists, False otherwise

        Example:
            >>> BootstyleBuilderBuilderTTk.has_builder('TButton', 'solid')
            True
            >>> BootstyleBuilderBuilderTTk.has_builder('TButton', 'nonexistent')
            False
        """
        cls._ensure_builders_loaded()
        return variant in cls._builder_registry.get(widget_class, {})

    def map_style(self, ttk_style: str, **options):
        self.style.map(ttk_style, **options)

    def configure_style(self, ttk_style, **kwargs):
        self.style.configure(ttk_style, **kwargs)

    def create_style_element_image(self, element: ElementImage):
        name, args, kwargs = element.build()
        self.style.element_create(name, "image", *args, **kwargs)

    def create_style_layout(self, ttk_style: str, element: Element):
        self.style.layout(ttk_style, [element.spec()])

    # Color utilities inherited from BootstyleBase
