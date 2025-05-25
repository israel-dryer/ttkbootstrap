from __future__ import annotations

from PIL import Image, ImageDraw, ImageTk

from ttkbootstrap.logger import logger
from ttkbootstrap.utils.window_utils import get_image_name

from ttkbootstrap.style.style_builder import StyleBuilder
from ttkbootstrap.style.style_element import Element


class TTkSizeGripStyle(StyleBuilder):

    def __init__(self, builder: StyleBuilder):
        super().__init__(builder)

    def invoke(self, color, **_):
        """Apply the solid button style."""
        style = 'TSizegrip'

        if color == "default":
            if not self.is_dark:
                grip_color = self.colors.border
            else:
                grip_color = self.colors.input_background
        else:
            style = f"{color}.{style}"
            grip_color = self.colors.get(color)

        if self.activated:
            return style

        # set background color
        self.ttk.configure(style, background=self.colors.background)

        # create and register the widget assets
        image_name = f"{style}.Sizegrip.sizegrip"
        image = self.create_assets(grip_color)
        self.ttk.element_create(image_name, "image", image)

        # build the style layout
        Element(style).layout([Element(image_name, side="bottom", sticky="se")])

        self.activated = True
        return style

    def create_assets(self, color):
        box = self.builder.scale_size(1)
        pad = box * 2
        chunk = box + pad  # 4

        w = chunk * 3 + pad  # 14
        h = chunk * 3 + pad  # 14

        size = [w, h]

        im = Image.new("RGBA", size)
        draw = ImageDraw.Draw(im)

        draw.rectangle((chunk * 2 + pad, pad, chunk * 3, chunk), fill=color)
        draw.rectangle(
            (chunk * 2 + pad, chunk + pad, chunk * 3, chunk * 2), fill=color
        )
        draw.rectangle(
            (chunk * 2 + pad, chunk * 2 + pad, chunk * 3, chunk * 3),
            fill=color,
        )

        draw.rectangle(
            (chunk + pad, chunk + pad, chunk * 2, chunk * 2), fill=color
        )
        draw.rectangle(
            (chunk + pad, chunk * 2 + pad, chunk * 2, chunk * 3), fill=color
        )

        draw.rectangle((pad, chunk * 2 + pad, chunk, chunk * 3), fill=color)

        _img = ImageTk.PhotoImage(im)
        _name = get_image_name(_img)
        # TODO consider another method using weak ref
        self.builder.register_asset(_name, _img)  # to prevent garbage collection
        return _name
