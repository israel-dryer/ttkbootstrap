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
    TTkButtonDefaultStyle
)

ttk_handlers = [
    ('ttk.default.button', TTkButtonDefaultStyle),
]
