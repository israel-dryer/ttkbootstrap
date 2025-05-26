from .badge import TTkBadgeCircleStyle, TTkBadgeDefaultStyle, TTkBadgePillStyle
from .button import TTkButtonDefaultStyle, TTkButtonTextStyle, TTkButtonOutlineStyle
from .check_box import TTkCheckBoxStyle
from .divider import TTkDividerDefaultStyle, TTkDividerDashedStyle
from .frame import TTkFrameRoundStyle, TTkFrameDefaultStyle
from .icon_button import TTkIconButtonDefaultStyle, TTkIconButtonTextStyle, TTkIconButtonOutlineStyle
from .label import TTkLabelInverseStyle, TTkLabelDefaultStyle
from .radio import TTkRadioStyle
from .scrollbar import TTkScrollbarDefaultStyle, TTkScrollbarRoundStyle
from .slider import TTkSliderDefaultStyle
from .switch import TTkSwitchDefaultStyle
from .text_box import TTkTextBoxDefaultStyle
from .tool_button import TTkToolButtonDefaultStyle
# from .tree_view import TTkTreeViewDefaultStyle

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
    # ('ttk.default.treeview', TTkTreeViewDefaultStyle),
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
