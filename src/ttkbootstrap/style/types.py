from tkinter.font import Font
from typing import Literal, Union

ColorShade = Literal[100, 200, 300, 400, 500, 600, 700, 800, 900]
ColorMode = Union[Literal['light', 'dark'], str]
ColorModel = Literal['hex', 'hsl', 'rgb']

# === Color Types ===

# supports subtle variants, e.g., 'primary[subtle]'
SemanticColor = Literal['primary', 'secondary', 'success', 'info', 'warning', 'danger', 'light', 'dark']
UtilityColor = Literal['foreground', 'background']

# supports shade variants 100-900, e.g. `blue[300]`
ShadeColor = Literal['blue', 'indigo', 'purple', 'red', 'orange', 'yellow', 'green', 'teal', 'cyan', 'gray']

# === Color Tokens ===

SurfaceColor = Union[SemanticColor, str]
ForegroundColor = Union[SemanticColor, ShadeColor, UtilityColor, str]
ThemeColor = Union[SemanticColor, ShadeColor, UtilityColor, str]
SeparatorColor = Union[Literal['border'], SemanticColor]
BorderColor = Union[Literal['border'], SemanticColor, ShadeColor, str]

# === Font Tokens ====

BootstrapFontType = Literal[
    'label', 'body', 'body-sm', 'body-lg', 'body-xl', 'caption',
    'display-xl', 'display-lg', 'heading-xl', 'heading-lg', 'heading-md', 'code'
]

TypographyToken = Union[BootstrapFontType, str, Font]
