from ...ttk_types import StyleColor
from ...widgets.legacy import TkTopLevel
from ...widgets.layout.frame import Frame
from ...widgets.display.label import Label

try:
    from typing import Literal, Unpack
except ImportError:
    from typing_extensions import Unpack

ToastType = Literal['default', 'info', 'success', 'warning', 'error']
ToastPosition = Literal['top-left', 'top-right', 'bottom-left', 'bottom-right', 'top', 'bottom', 'center']


class Toast(TkTopLevel):
    def __init__(
        self,
        master,
        message,
        toast_type: ToastType = "default",
        duration=3000,
        position: ToastPosition = "top",
        close_on_click: bool = False,
        **kwargs
    ):
        super().__init__(master, **kwargs)
        self.withdraw()
        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.configure(bg="black")

        self.toast_type = toast_type
        self.message = message
        self.duration = duration
        self.position = position
        self.close_on_click = close_on_click

        color: StyleColor = "default"
        icon = None

        match toast_type:
            case "error":
                color = "danger"
                icon = "x-circle"
            case "info":
                color = "info"
                icon = "info-circle"
            case "success":
                color = "success"
                icon = "check-circle"
            case "warning":
                color = "warning"
                icon = "exclamation-triangle"
            case "default":
                color = "foreground"
                icon = None

        self.frame = Frame(self, color=color, padding=16)
        self.frame.pack(fill="both", expand=True)

        if icon is not None:
            self.icon_label = Label(self.frame, icon=icon, color=color, variant="inverse", compound="image")
            self.icon_label.pack(side="left", padx=(0, 12))

        self.label = Label(
            self.frame,
            text=message,
            variant="inverse",
            color=color,
            anchor="w",
            justify="left",
            wraplength=568
        )
        self.label.pack(side="left", fill="x", expand=True)

        self.frame.configure(width=568)
        self.resizable(False, False)

        if self.close_on_click:
            for widget in (self, self.frame, self.label):
                widget.bind("<Button-1>", lambda e: self.destroy())
            if icon is not None:
                self.icon_label.bind("<Button-1>", lambda e: self.destroy())

    def show(self):
        self._place_toast(self.position)
        if not self.close_on_click:
            self.after(self.duration, self.destroy)

    def _place_toast(self, position: ToastPosition):
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        width = self.winfo_reqwidth()
        height = self.winfo_reqheight()
        margin = 20

        x = (screen_width - width) // 2
        y = screen_height - height - margin

        match position:
            case "bottom-right":
                x = screen_width - width - margin
                y = screen_height - height - margin
            case "bottom-left":
                x = margin
                y = screen_height - height - margin
            case "top-right":
                x = screen_width - width - margin
                y = margin
            case "top-left":
                x = margin
                y = margin
            case "top":
                x = (screen_width - width) // 2
                y = margin
            case "bottom":
                x = (screen_width - width) // 2
                y = screen_height - height - margin
            case "center":
                x = (screen_width - width) // 2
                y = (screen_height - height) // 2

        self.geometry(f"{width}x{height}+{x}+{y}")
        self.deiconify()
