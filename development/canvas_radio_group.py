import tkinter as tk
from PIL import Image, ImageDraw, ImageTk


class RoundedToggleButtonGroup(tk.Canvas):
    def __init__(self, master, items, command=None, width=300, height=40, radius=10, **kwargs):
        super().__init__(master, width=width, height=height, highlightthickness=0, **kwargs)
        self.command = command
        self.items = items
        self.radius = radius
        self.width = width
        self.height = height
        self.segment_width = width // len(items)
        self.active_index = None
        self.hover_index = None
        self.bg_color = "#e0e0e0"
        self.hover_color = "#cce5ff"
        self.active_color = "#007bff"
        self.text_color = "black"
        self.active_text_color = "white"
        self._image_cache = {}

        self._render_static_background()
        self._draw_buttons()

        self.bind("<Motion>", self._on_hover)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_click)

    def _draw_buttons(self):
        self.buttons = []
        for i, text in enumerate(self.items):
            x0 = i * self.segment_width
            x1 = x0 + self.segment_width
            image_id = self.create_image(x0, 0, anchor="nw")
            text_id = self.create_text((x0 + x1)//2, self.height//2, text=text, font=("Segoe UI", 10), fill=self.text_color)
            self.buttons.append({"image": image_id, "text": text_id})
        self._redraw()

    def _render_static_background(self):
        self.create_image(0, 0, image=self._make_rounded_image(self.bg_color, full_round=True), anchor="nw")

    def _redraw(self):
        for i, btn in enumerate(self.buttons):
            is_hover = i == self.hover_index
            is_active = i == self.active_index

            fill = self.active_color if is_active else self.hover_color if is_hover else None
            text_color = self.active_text_color if is_active else self.text_color

            img = self._make_rounded_image(fill, position=i)
            self.itemconfig(btn["image"], image=img)
            self.itemconfig(btn["text"], fill=text_color)
            btn["__photo"] = img  # Prevent garbage collection

    def _make_rounded_image(self, color, position=0, full_round=False):
        key = (color, position, full_round)
        if key in self._image_cache:
            return self._image_cache[key]

        img = Image.new("RGBA", (self.segment_width, self.height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Determine corner rounding
        if full_round or (position == 0 and len(self.items) == 1):
            radius_tuple = (self.radius,) * 4
        elif position == 0:
            radius_tuple = (self.radius, 0, 0, self.radius)
        elif position == len(self.items) - 1:
            radius_tuple = (0, self.radius, self.radius, 0)
        else:
            radius_tuple = (0, 0, 0, 0)

        self._draw_rounded_rect(draw, (0, 0, self.segment_width, self.height), color, radius_tuple)

        photo = ImageTk.PhotoImage(img)
        self._image_cache[key] = photo
        return photo

    def _draw_rounded_rect(self, draw, box, fill, radii):
        """Draw a rounded rectangle with different corner radii."""
        if not fill:
            return  # skip drawing

        x0, y0, x1, y1 = box
        tl, tr, br, bl = radii
        draw.rectangle([x0 + tl, y0, x1 - tr, y1], fill=fill)
        draw.rectangle([x0, y0 + tl, x1, y1 - bl], fill=fill)

        # Draw corners
        if tl:
            draw.pieslice([x0, y0, x0 + 2 * tl, y0 + 2 * tl], 180, 270, fill=fill)
        if tr:
            draw.pieslice([x1 - 2 * tr, y0, x1, y0 + 2 * tr], 270, 360, fill=fill)
        if br:
            draw.pieslice([x1 - 2 * br, y1 - 2 * br, x1, y1], 0, 90, fill=fill)
        if bl:
            draw.pieslice([x0, y1 - 2 * bl, x0 + 2 * bl, y1], 90, 180, fill=fill)

    def _on_hover(self, event):
        index = event.x // self.segment_width
        if index != self.hover_index:
            self.hover_index = index
            self._redraw()

    def _on_leave(self, event):
        self.hover_index = None
        self._redraw()

    def _on_click(self, event):
        index = event.x // self.segment_width
        self.active_index = index
        self._redraw()
        if self.command:
            self.command(self.items[index])


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Rounded Toggle Group")

    def on_select(value):
        print("Selected:", value)

    group = RoundedToggleButtonGroup(root, ["Left", "Middle", "Right"], command=on_select, width=300, height=40)
    group.pack(padx=20, pady=20)

    root.mainloop()
