from __future__ import annotations

from typing import Mapping, Any

from ttkbootstrap.core.capabilities.after import AfterMixin
from ttkbootstrap.core.capabilities.bind import BindingsMixin
from ttkbootstrap.core.capabilities.bindtags import BindtagsMixin
from ttkbootstrap.core.capabilities.clipboard import ClipboardMixin
from ttkbootstrap.core.capabilities.focus import FocusMixin
from ttkbootstrap.core.capabilities.grab import GrabMixin
from ttkbootstrap.core.capabilities.grid import GridMixin
from ttkbootstrap.core.capabilities.pack import PackMixin
from ttkbootstrap.core.capabilities.place import PlaceMixin
from ttkbootstrap.core.capabilities.selection import SelectionMixin
from ttkbootstrap.core.capabilities.winfo import WinfoMixin


class WidgetCapabilitiesMixin(
    AfterMixin,
    BindingsMixin,
    BindtagsMixin,
    ClipboardMixin,
    FocusMixin,
    GrabMixin,
    GridMixin,
    PackMixin,
    PlaceMixin,
    SelectionMixin,
    WinfoMixin,
):
    """Common widget API surface (tk + ttk).

    This mixin aggregates documented capability mixins into a single interface
    suitable for both Tk and ttk widgets, plus a small set of commonly used
    widget operations (configure/cget/destroy, stacking order, etc.).
    """

    # -------------------------------------------------------------------------
    # Lifecycle
    # -------------------------------------------------------------------------

    def destroy(self) -> None:
        """Destroy this widget and release its Tk resources."""
        return super().destroy()  # type: ignore[misc]

    # -------------------------------------------------------------------------
    # Configuration
    # -------------------------------------------------------------------------

    def configure(self, cnf: Mapping[str, Any] | None = None, **kw: Any) -> Any:
        """Configure widget options.

        Args:
            cnf: Optional mapping of option values.
            **kw: Option values as keyword arguments.

        Returns:
            Tk returns configuration details when called with no args; otherwise
            the return value is implementation-dependent.
        """
        if cnf is None:
            return super().configure(**kw)  # type: ignore[misc]
        return super().configure(cnf, **kw)  # type: ignore[misc]

    config = configure

    def cget(self, key: str) -> Any:
        """Return the current value for an option.

        Args:
            key: Option name (with or without a leading dash).

        Returns:
            The option value.
        """
        return super().cget(key)  # type: ignore[misc]

    # -------------------------------------------------------------------------
    # Stacking order
    # -------------------------------------------------------------------------

    def lift(self, aboveThis: Any | None = None) -> None:
        """Raise this widget above its siblings.

        Args:
            aboveThis: Optional sibling widget to raise above.
        """
        return super().lift(aboveThis)  # type: ignore[misc]

    tkraise = lift

    def lower(self, belowThis: Any | None = None) -> None:
        """Lower this widget below its siblings.

        Args:
            belowThis: Optional sibling widget to lower below.
        """
        return super().lower(belowThis)  # type: ignore[misc]

    # -------------------------------------------------------------------------
    # Layout convenience
    # -------------------------------------------------------------------------

    def forget(self) -> None:
        """Remove the widget from layout (best-effort).

        This calls the appropriate forget method depending on the active geometry manager:

            - grid  -> grid_forget()
            - pack  -> pack_forget()
            - place -> place_forget()
        """
        try:
            mgr = self.winfo_manager()  # type: ignore[attr-defined]
        except Exception:
            mgr = ""

        if mgr == "grid":
            try:
                self.grid_forget()  # type: ignore[attr-defined]
            except Exception:
                pass
        elif mgr == "pack":
            try:
                self.pack_forget()  # type: ignore[attr-defined]
            except Exception:
                pass
        elif mgr == "place":
            try:
                self.place_forget()  # type: ignore[attr-defined]
            except Exception:
                pass
