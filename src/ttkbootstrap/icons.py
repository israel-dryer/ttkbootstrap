import json
import os
import tempfile

from PIL import Image, ImageDraw, ImageFont, ImageTk
from importlib.resources import files
from pathlib import Path

from ttkbootstrap.logger import logger

"""
    USAGE
    =====
    from ttkbootstrap.icons import Icon

    Icon.initialize()  # must be called once

    alarm_icon = Icon("alarm", size=32)
    tk.Label(root, image=alarm_icon.image).pack()
    
    PYINSTALLER INSTRUCTIONS
    ========================
    Add this to your .spec file or CLI
    
    CLI:
    --add-data "ttkbootstrap/assets/bootstrap-icons.ttf;ttkbootstrap/assets"
    --add-data "ttkbootstrap/assets/bootstrap-icons.json;ttkbootstrap/assets"
    
    SPEC:
    datas = [
        ("ttkbootstrap/assets/bootstrap-icons.ttf", "ttkbootstrap/assets"),
        ("ttkbootstrap/assets/bootstrap-icons.json", "ttkbootstrap/assets"),
    ]
    
    CLEANUP SUGGESTION
    ==================
    delete the temporary file at exit:
    
    ```python
    import atexit
    atexit.register(lambda: os.remove(Icon._font_path))
    ```
"""


def get_icon_asset_path(filename: str) -> Path:
    return files("ttkbootstrap.assets").joinpath(filename)


class Icon:
    _icon_map = None
    _font_path = None
    _cache = {}
    _initialized = False

    __str__ = lambda self: str(self.image)

    def __init__(self, name: str, size: int = 24, color: str = "black"):
        if not Icon._icon_map or not Icon._font_path:
            raise RuntimeError("Call Icon.configure(font_path, icon_map) first.")
        self.name = name
        self.size = size
        self.color = color
        self.image = self._render()

    @classmethod
    def configure(cls, font_path: str, icon_map: dict):
        if not os.path.exists(font_path):
            raise FileNotFoundError(f"Font not found: {font_path}")
        cls._font_path = font_path
        cls._icon_map = {
            name: chr(codepoint) for name, codepoint in icon_map.items()
        }

    def _render(self):
        key = (self.name, self.size, self.color)
        if key in Icon._cache:
            return Icon._cache[key]

        glyph = Icon._icon_map.get(self.name)
        if not glyph:
            raise ValueError(f"Icon '{self.name}' not found in icon map.")

        font = ImageFont.truetype(Icon._font_path, self.size)

        # Glyph bounding box
        bbox = font.getbbox(glyph)
        glyph_w, glyph_h = bbox[2] - bbox[0], bbox[3] - bbox[1]

        # Font-wide vertical metrics
        ascent, descent = font.getmetrics()
        full_height = ascent + descent

        canvas_size = self.size
        img = Image.new("RGBA", (canvas_size, canvas_size), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)

        # Center horizontally as usual
        dx = (canvas_size - glyph_w) // 2 - bbox[0]

        # Center vertically using full font height
        dy = (canvas_size - full_height) // 2 + (ascent - bbox[3])

        # Optional per-icon correction
        manual_offsets = {
            "key": -1,
            "paperclip": -1,
        }
        dy += manual_offsets.get(self.name, 0)

        draw.text((dx, dy), glyph, font=font, fill=self.color)

        tk_img = ImageTk.PhotoImage(img)
        Icon._cache[key] = tk_img
        return tk_img

    @classmethod
    def initialize(cls):
        if (cls._initialized):
            return
        json_res = get_icon_asset_path("bootstrap-icons.json")
        font_res = get_icon_asset_path("bootstrap-icons.ttf")

        # Dump to real temp file (for font)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".ttf") as tmp_font:
            tmp_font.write(font_res.read_bytes())
            font_path = tmp_font.name

        # Read icon map directly (Traversable supports .read_text())
        icon_map = json.loads(json_res.read_text(encoding="utf-8"))

        # Configure globally
        Icon.configure(font_path=font_path, icon_map=icon_map)
        cls._initialized = True
        logger.info("Icon", "Initialized icons")

    @classmethod
    def cleanup(cls):
        """Remove temp font file, if it exists."""
        if cls._font_path and os.path.exists(cls._font_path):
            try:
                os.remove(cls._font_path)
                cls._font_path = None
            except Exception as e:
                logger.error('Icon', f'Failed to remove temp font: {e}')
        cls._initialized = False
        cls._cache.clear()
