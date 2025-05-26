from .tk_base_style import TkBaseStyle
from .tk_button_style import TkButtonStyle
from .tk_canvas_style import TkCanvasStyle
from .tk_checkbutton_style import TkCheckbuttonStyle
from .tk_entry_style import TkEntryStyle
from .tk_frame_style import TkFrameStyle
from .tk_label_style import TkLabelStyle
from .tk_labelframe_style import TkLabelFrameStyle
from .tk_listbox_style import TkListboxStyle
from .tk_menu_style import TkMenuStyle
from .tk_menubutton_style import TkMenubuttonStyle
from .tk_radiobutton_style import TkRadiobuttonStyle
from .tk_scale_style import TkScaleStyle
from .tk_spinbox_style import TkSpinboxStyle
from .tk_text_style import TkTextStyle
from .tk_toplevel_style import TkToplevelStyle

tk_handlers = [
    ('tk.base', TkBaseStyle),
    ('tk.button', TkButtonStyle),
    ('tk.canvas', TkCanvasStyle),
    ('tk.checkbutton', TkCheckbuttonStyle),
    ('tk.entry', TkEntryStyle),
    ('tk.frame', TkFrameStyle),
    ('tk.label', TkLabelStyle),
    ('tk.labelframe', TkLabelFrameStyle),
    ('tk.listbox', TkListboxStyle),
    ('tk.menu', TkMenuStyle),
    ('tk.menubutton', TkMenubuttonStyle),
    ('tk.radiobutton', TkRadiobuttonStyle),
    ('tk.scale', TkScaleStyle),
    ('tk.spinbox', TkSpinboxStyle),
    ('tk.text', TkTextStyle),
    ('tk.toplevel', TkToplevelStyle),
]
