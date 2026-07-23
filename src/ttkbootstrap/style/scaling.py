"""Private root-bound scaling primitives for ttkbootstrap.

Theme recipes use logical UI units. This service converts them exactly once to
the physical pixels consumed by Tk and Pillow.
"""
import tkinter
from math import ceil, floor


_QUARTER_STEP_TOLERANCE = 0.005
_ROOT_ATTRIBUTE = "_ttkbootstrap_scaling"


def _round_half_away(value: float) -> int:
    """Round halves away from zero without Python's banker rounding."""
    if value >= 0:
        return floor(value + 0.5)
    return ceil(value - 0.5)


class Scaling:
    """Convert logical UI units for one Tk root/interpreter."""

    def __init__(self, root):
        """Bind the service to `root`'s Tk interpreter."""
        self.root = root

    @classmethod
    def for_widget(cls, widget):
        """Return the service attached to `widget`'s root."""
        root_getter = getattr(widget, "_root", None)
        root = root_getter() if callable(root_getter) else widget
        service = getattr(root, _ROOT_ATTRIBUTE, None)
        if service is None:
            service = cls(root)
            setattr(root, _ROOT_ATTRIBUTE, service)
        return service

    @property
    def windowing_system(self) -> str:
        """Name of the underlying Tk windowing system (`x11`, `win32`, or `aqua`)."""
        return str(self.root.tk.call("tk", "windowingsystem"))

    @property
    def baseline(self) -> float:
        """Tk scaling value that corresponds to a 1.0 (unscaled) UI factor.

        A standard-density display reports 4/3 (96 dpi) everywhere -- except on
        aqua before Tk 9, which assumed 72 dpi and reported 1.0. Reading the
        wrong baseline scales every asset and every pixel-valued geometry by the
        ratio between them, so the version gate matters as much as the platform.
        """
        if self.windowing_system == "aqua" and tkinter.TkVersion < 8.7:
            return 1.0
        return 4 / 3

    @property
    def tk_scaling(self) -> float:
        """Current Tk scaling factor, falling back to a fpixels-based estimate."""
        try:
            return float(self.root.tk.call("tk", "scaling"))
        except Exception:
            return float(self.root.winfo_fpixels("1i")) / 72

    @property
    def factor(self) -> float:
        """Scaling factor relative to `baseline`, snapped to the nearest quarter step when close."""
        raw = self.tk_scaling / self.baseline
        quarter = round(raw * 4) / 4
        if abs(raw - quarter) <= _QUARTER_STEP_TOLERANCE:
            return quarter
        return raw

    def logical(self, value, *, minimum: int = 0):
        """Convert logical UI units to physical pixels.

        Scalars return an integer. Tuple and list inputs retain the historical
        public `scale_size` result shape and return a list.
        """

        def convert(item, factor):
            if item == 0:
                return 0
            result = _round_half_away(float(item) * factor)
            return max(minimum, result) if item > 0 else result

        if isinstance(value, (int, float)):
            return convert(value, self.factor)
        if isinstance(value, (tuple, list)):
            factor = self.factor
            return [convert(item, factor) for item in value]
        return None

    def source(self, value, *, source_scale: float, minimum: int = 0):
        """Convert source-image pixels directly to physical pixels."""
        if source_scale <= 0:
            raise ValueError("source_scale must be greater than zero")
        if isinstance(value, (int, float)):
            return self.logical(float(value) / source_scale, minimum=minimum)
        if isinstance(value, (tuple, list)):
            logical = [float(item) / source_scale for item in value]
            return self.logical(logical, minimum=minimum)
        return None

    def image_size(self, size) -> tuple[int, int]:
        """Convert a logical scalar or pair to physical `(width, height)`."""
        if isinstance(size, (int, float)):
            edge = self.logical(size, minimum=1)
            return edge, edge
        if isinstance(size, (tuple, list)) and len(size) == 2:
            width, height = self.logical(size, minimum=1)
            return width, height
        raise TypeError(f"size must be a number or two-item sequence, got {size!r}")

    @staticmethod
    def render_origin(value: float, *, oversample: int) -> int:
        """Align an oversampled coordinate to the final-pixel grid."""
        if oversample < 1:
            raise ValueError("oversample must be at least 1")
        return _round_half_away(value / oversample) * oversample
