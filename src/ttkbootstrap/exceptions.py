class StyleHandlerNotFoundError(LookupError):
    """Raised when a style handler method does not exist for the given style key."""

    def __init__(self, color: str, variant: str, widget_class: str):
        super().__init__(
            f"No style handler found for {{color:{color}, variant:{variant}, widget_class: {widget_class}}}")
        self.color = color
        self.variant = variant
        self.widget_class = widget_class


class ThemeNotFoundError(LookupError):
    """Raised when attempting to use a ttk theme that does not exist."""

    def __init__(self, theme_name: str):
        super().__init__(f"Theme '{theme_name}' not found.")
        self.theme_name = theme_name

class ThemeAlreadyExistsError(ValueError):
    """Raised when attempting to create a theme with a name that already exists."""

    def __init__(self, theme_name: str):
        super().__init__(f"Theme '{theme_name}' already exists.")
        self.theme_name = theme_name
