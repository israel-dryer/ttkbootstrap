"""Debug centering issue - check actual image dimensions and widget sizes."""

import ttkbootstrap as ttk
from tkinter import font
from PIL import ImageGrab

app = ttk.App(theme="dark")
app.geometry("200x200")

# Create xs button like the user's test
xs_btn = ttk.Button(app, text='Button', style_options={'size': 'xs'})
xs_btn.pack(padx=20, pady=20)

xs_btn_icon = ttk.Button(app, text='Button', icon='bootstrap', style_options={'size': 'xs'})
xs_btn_icon.pack(padx=20, pady=20)


def debug_info():
    app.update()

    # Get font metrics
    caption_font = font.nametofont('caption')
    metrics = caption_font.metrics()
    print(f"Caption font: ascent={metrics['ascent']}, descent={metrics['descent']}, linespace={metrics['linespace']}")

    # Get image scale info
    from ttkbootstrap.runtime.utility import _ScalingState
    from ttkbootstrap.style.utility import _load_manifest

    manifest = _load_manifest()
    source_res = manifest.get("default_dpi", 2.0)
    scale = _ScalingState.get_image_scale(source_resolution=source_res)

    xs_info = manifest.get("images", {}).get("button_xs")
    if xs_info:
        src_h = xs_info['height']
        src_border = xs_info['border']

        # Calculate scaled values (using rounding as per fix)
        scaled_h = int(src_h * scale + 0.5)
        scaled_border = int(src_border * scale + 0.5)
        stretchable = scaled_h - 2 * scaled_border

        print(f"\nImage scaling (scale={scale:.4f}):")
        print(f"  Source: {src_h}x{src_h}, border={src_border}")
        print(f"  Scaled: {scaled_h}x{scaled_h}, border={scaled_border}")
        print(f"  Stretchable region: {stretchable}px")

    # Get widget sizes
    for name, btn in [("xs_text", xs_btn), ("xs_icon", xs_btn_icon)]:
        w = btn.winfo_width()
        h = btn.winfo_height()
        print(f"\n{name}: widget size = {w}x{h}")

        if xs_info:
            growth = h - scaled_h
            print(f"  Growth (widget - image) = {growth}px")

        # Capture and analyze
        x = btn.winfo_rootx()
        y = btn.winfo_rooty()
        img = ImageGrab.grab(bbox=(x, y, x+w, y+h))

        # Find content bounds
        # For dark theme, background is dark, content is light
        bg = img.getpixel((2, 2))

        content_top = None
        content_bottom = None

        for row in range(h):
            for col in range(w):
                pixel = img.getpixel((col, row))
                diff = sum(abs(a - b) for a, b in zip(pixel[:3], bg[:3]))
                if diff > 50:
                    if content_top is None:
                        content_top = row
                    content_bottom = row
                    break

        if content_top is not None:
            content_center = (content_top + content_bottom) / 2
            widget_center = (h - 1) / 2
            offset = content_center - widget_center

            print(f"  Content: rows {content_top}-{content_bottom}")
            print(f"  Content center: {content_center:.1f}, Widget center: {widget_center:.1f}")
            print(f"  Offset: {offset:+.1f}px")
            print(f"  Top margin: {content_top}, Bottom margin: {h - 1 - content_bottom}")


app.after(500, debug_info)
app.after(3000, app.destroy)
app.mainloop()