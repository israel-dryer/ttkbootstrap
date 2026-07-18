"""Screenshot scenes for docs/user-guide/how-to/working-with-images.rst."""

import ttkbootstrap as ttk
from PIL import Image, ImageDraw, ImageTk


def _sample_photo(w, h):
    # A generated stand-in for the page's photo.jpg (no external asset needed):
    # a sunset gradient with a sun and a hill silhouette.
    img = Image.new("RGB", (w, h))
    px = img.load()
    for y in range(h):
        t = y / h
        r = int(255 * (1 - t) + 60 * t)
        g = int(120 * (1 - t) + 40 * t)
        b = int(90 * (1 - t) + 90 * t)
        for x in range(w):
            px[x, y] = (r, g, b)
    draw = ImageDraw.Draw(img)
    draw.ellipse([w * 0.55, h * 0.18, w * 0.8, h * 0.43], fill=(255, 224, 150))
    draw.ellipse([-w * 0.2, h * 0.62, w * 0.7, h * 1.4], fill=(40, 30, 55))
    draw.ellipse([w * 0.45, h * 0.72, w * 1.3, h * 1.5], fill=(28, 22, 42))
    return img


def photo():
    app = ttk.App(title="Image")
    pil = _sample_photo(200, 200)
    photo = ImageTk.PhotoImage(pil)
    label = ttk.Label(app, image=photo, padding=10)
    label.image = photo          # keep the reference
    label.pack()
    app.mainloop()


SCENES = {
    "photo": photo,
}
