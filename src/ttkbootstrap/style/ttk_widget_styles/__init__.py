from .ttk_button_default_style import TTkButtonDefaultStyle
from .ttk_button_outline_style import TTkButtonOutlineStyle
from .ttk_button_text_style import TTkButtonTextStyle
from .ttk_check_box_style import TTkCheckBoxStyle
from .ttk_text_box_default_style import TTkTextBoxDefaultStyle
from .ttk_scrollbar_default_style import TTkScrollbarDefaultStyle
from .ttk_scrollbar_rounded_style import TTkScrollbarRoundStyle
from .ttk_radio_style import TTkRadioStyle
from .ttk_switch_default_style import TTkSwitchDefaultStyle
from .ttk_frame_round_style import TTkFrameRoundStyle
from .ttk_slider_default_style import TTkSliderDefaultStyle
from .ttk_tool_button_default_style import TTkToolButtonDefaultStyle
from .ttk_tree_view_style import TTkTreeViewDefaultStyle
from .ttk_icon_button_default_style import TTkIconButtonDefaultStyle
from .ttk_icon_button_outline_style import TTkIconButtonOutlineStyle
from .ttk_icon_button_text_style import TTkIconButtonTextStyle

ttk_handlers = [
    ('ttk.default.button', TTkButtonDefaultStyle),
    ('ttk.outline.button', TTkButtonOutlineStyle),
    ('ttk.text.button', TTkButtonTextStyle),
    ('ttk.default.checkbutton', TTkCheckBoxStyle),
    ('ttk.default.scrollbar', TTkScrollbarDefaultStyle),
    ('ttk.round.scrollbar', TTkScrollbarRoundStyle),
    ('ttk.default.radiobutton', TTkRadioStyle),
    ('ttk.default.switch', TTkSwitchDefaultStyle),
    ('ttk.default.input', TTkTextBoxDefaultStyle),
    ('ttk.round.frame', TTkFrameRoundStyle),
    ('ttk.default.slider', TTkSliderDefaultStyle),
    ('ttk.default.checkbutton.toggle', TTkToolButtonDefaultStyle),
    ('ttk.default.radiobutton.toggle', TTkToolButtonDefaultStyle),
    ('ttk.default.treeview', TTkTreeViewDefaultStyle),
    ('ttk.default.icon.button', TTkIconButtonDefaultStyle),
    ('ttk.outline.icon.button', TTkIconButtonOutlineStyle),
    ('ttk.text.icon.button', TTkIconButtonTextStyle)
]
