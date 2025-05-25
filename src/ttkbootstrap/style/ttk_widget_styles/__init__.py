from .ttk_button_default_style import TTkButtonDefaultStyle
from .ttk_button_outline_style import TTkButtonOutlineStyle
from .ttk_button_text_style import TTkButtonTextStyle
from .ttk_checkbutton_style import TTkCheckbuttonStyle
from .ttk_input_default_style import TTkInputDefaultStyle
from .ttk_scrollbar_default_style import TTkScrollbarDefaultStyle
from .ttk_scrollbar_rounded_style import TTkScrollbarRoundStyle
from .ttk_radiobutton_style import TTkRadiobuttonStyle
from .ttk_switch_default_style import TTkSwitchDefaultStyle
from .ttk_frame_round_style import TTkFrameRoundStyle
from .ttk_slider_default_style import TTkSliderDefaultStyle
from .ttk_toolbutton_default_style import TTkToolbuttonDefaultStyle
from .ttk_treeview_style import TTkTreeviewDefaultStyle
from .ttk_icon_button_default_style import TTkIconButtonDefaultStyle
from .ttk_icon_button_outline_style import TTkIconButtonOutlineStyle
from .ttk_icon_button_text_style import TTkIconButtonTextStyle

ttk_handlers = [
    ('ttk.default.button', TTkButtonDefaultStyle),
    ('ttk.outline.button', TTkButtonOutlineStyle),
    ('ttk.text.button', TTkButtonTextStyle),
    ('ttk.default.checkbutton', TTkCheckbuttonStyle),
    ('ttk.default.scrollbar', TTkScrollbarDefaultStyle),
    ('ttk.round.scrollbar', TTkScrollbarRoundStyle),
    ('ttk.default.radiobutton', TTkRadiobuttonStyle),
    ('ttk.default.switch', TTkSwitchDefaultStyle),
    ('ttk.default.input', TTkInputDefaultStyle),
    ('ttk.round.frame', TTkFrameRoundStyle),
    ('ttk.default.slider', TTkSliderDefaultStyle),
    ('ttk.default.checkbutton.toggle', TTkToolbuttonDefaultStyle),
    ('ttk.default.radiobutton.toggle', TTkToolbuttonDefaultStyle),
    ('ttk.default.treeview', TTkTreeviewDefaultStyle),
    ('ttk.default.icon.button', TTkIconButtonDefaultStyle),
    ('ttk.outline.icon.button', TTkIconButtonOutlineStyle),
    ('ttk.text.icon.button', TTkIconButtonTextStyle)
]
