# from .badge import TTkBadgeCircleStyle, TTkBadgeDefaultStyle, TTkBadgePillStyle
# from .button import TTkButtonDefaultStyle, TTkButtonTextStyle, TTkButtonOutlineStyle
# from .check_button import TTkCheckButtonStyle
# from .divider import TTkDividerDefaultStyle, TTkDividerDashedStyle
# from .frame import TTkFrameRoundStyle, TTkFrameDefaultStyle
# from .label import TTkLabelInverseStyle, TTkLabelDefaultStyle
# from .progress import TTkProgressStripedStyle, TTkProgressDefaultStyle
# from .radio import TTkRadioStyle
# from .scrollbar import TTkScrollbarDefaultStyle, TTkScrollbarSquareStyle
# from .slider import TTkSliderDefaultStyle
# from .switch import TTkSwitchDefaultStyle
# from .text_box import TTkTextBoxDefaultStyle
# from .tool_button import TTkToolButtonDefaultStyle
# from .tree_view import TTkTreeViewDefaultStyle

from .button import (
    TTkButtonDefaultStyle, TTkButtonOutlineStyle, TTkButtonTextStyle,
    TTkIconButtonDefaultStyle, TTkIconButtonOutlineStyle, TTkIconButtonTextStyle
)
from .tool_button import TTkToolButtonDefaultStyle

ttk_handlers = [
    ('ttk.default.button', TTkButtonDefaultStyle),
    ('ttk.outline.button', TTkButtonOutlineStyle),
    ('ttk.text.button', TTkButtonTextStyle),
    ('ttk.default.icon.button', TTkIconButtonDefaultStyle),
    ('ttk.outline.icon.button', TTkIconButtonOutlineStyle),
    ('ttk.text.icon.button', TTkIconButtonTextStyle),
    ('ttk.default.tool.button', TTkToolButtonDefaultStyle),
]
