"""Widget mixins for ttkbootstrap."""

from ttkbootstrap.widgets.mixins.configure_mixin import (
    ConfigureDelegationMixin,
    configure_delegate,
)
from ttkbootstrap.widgets.mixins.font_mixin import FontMixin
from ttkbootstrap.widgets.mixins.icon_mixin import IconMixin
from ttkbootstrap.widgets.mixins.validation_mixin import ValidationMixin

__all__ = [
    "ConfigureDelegationMixin",
    "configure_delegate",
    "FontMixin",
    "IconMixin",
    "ValidationMixin",
]