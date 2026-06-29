"""Private ttk style recipe modules and their explicit loader."""

from ttkbootstrap.style.builders.registry import freeze_registry


_loaded = False


def _import_builder_modules() -> None:
    """Import the fixed built-in module list to trigger decorators."""
    from ttkbootstrap.style.builders import (  # noqa: F401
        button,
        calendar,
        checkbutton,
        combobox,
        entry,
        floodgauge,
        frame,
        label,
        labelframe,
        menubutton,
        notebook,
        panedwindow,
        progressbar,
        radiobutton,
        scale,
        scrollbar,
        separator,
        sizegrip,
        spinbox,
        toggle,
        toolbutton,
        treeview,
    )


def load_builders() -> None:
    """Import every built-in recipe module once, failing visibly."""
    global _loaded
    if _loaded:
        return

    _import_builder_modules()
    freeze_registry()
    _loaded = True
