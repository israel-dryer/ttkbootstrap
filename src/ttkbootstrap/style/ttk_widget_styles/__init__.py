from .ttk_badge_circle_style import TTkBadgeCircleStyle
from .ttk_badge_default_style import TTkBadgeDefaultStyle
from .ttk_badge_pill_style import TTkBadgePillStyle
from .ttk_button_default_style import TTkButtonDefaultStyle
from .ttk_button_outline_style import TTkButtonOutlineStyle
from .ttk_button_text_style import TTkButtonTextStyle
from .ttk_check_box_style import TTkCheckBoxStyle
from .ttk_label_jnverse_style import TTkLabelInverseStyle
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
from .ttk_frame_default_style import TTkFrameDefaultStyle
from .ttk_divider_default_style import TTkDividerDefaultStyle
from .ttk_divider_dashed_style import TTkDividerDashedStyle

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
    ('ttk.default.frame', TTkFrameDefaultStyle),
    ('ttk.round.frame', TTkFrameRoundStyle),
    ('ttk.default.slider', TTkSliderDefaultStyle),
    ('ttk.default.checkbutton.toggle', TTkToolButtonDefaultStyle),
    ('ttk.default.radiobutton.toggle', TTkToolButtonDefaultStyle),
    ('ttk.default.treeview', TTkTreeViewDefaultStyle),
    ('ttk.default.icon.button', TTkIconButtonDefaultStyle),
    ('ttk.outline.icon.button', TTkIconButtonOutlineStyle),
    ('ttk.text.icon.button', TTkIconButtonTextStyle),
    ('ttk.default.divider', TTkDividerDefaultStyle),
    ('ttk.dashed.divider', TTkDividerDashedStyle),
    ('ttk.default.badge', TTkBadgeDefaultStyle),
    ('ttk.pill.badge', TTkBadgePillStyle),
    ('ttk.circle.badge', TTkBadgeCircleStyle),
    ('ttk.default.frame', TTkFrameDefaultStyle),
    ('ttk.inverse.label', TTkLabelInverseStyle)
]
