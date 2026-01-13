"""Debug centering - specifically measure text position within button."""

import ttkbootstrap as ttk
from tkinter import font
from PIL import ImageGrab

app = ttk.App(theme="dark")
app.geometry("200x200")

# Create xs button
xs_btn = ttk.Button(app, text='Button', style_options={'size': 'xs'})
xs_btn.pack(padx=20, pady=20)


def debug_info():
    app.update()

    btn = xs_btn
    x = btn.winfo_rootx()
    y = btn.winfo_rooty()
    w = btn.winfo_width()
    h = btn.winfo_height()

    print(f"Widget size: {w}x{h}")

    img = ImageGrab.grab(bbox=(x, y, x+w, y+h))

    # In dark theme:
    # - Window background is dark gray (~45, 45, 45)
    # - Button background is blue (~59, 130, 246 for primary)
    # - Text is white (~255, 255, 255)

    # Sample button background color from center-left area (avoiding text)
    btn_bg = img.getpixel((5, h//2))
    print(f"Button background sample: {btn_bg[:3]}")

    # Find text pixels (very bright, close to white)
    text_rows = []
    for row in range(h):
        has_text = False
        for col in range(w):
            pixel = img.getpixel((col, row))
            # Text is white - look for very bright pixels
            brightness = sum(pixel[:3]) / 3
            if brightness > 200:  # White text
                has_text = True
                break
        if has_text:
            text_rows.append(row)

    if text_rows:
        text_top = text_rows[0]
        text_bottom = text_rows[-1]
        text_height = text_bottom - text_top + 1
        text_center = (text_top + text_bottom) / 2
        widget_center = (h - 1) / 2
        offset = text_center - widget_center

        print(f"\nText detection (white pixels):")
        print(f"  Text rows: {text_top} to {text_bottom} ({text_height}px)")
        print(f"  Text center: {text_center:.1f}")
        print(f"  Widget center: {widget_center:.1f}")
        print(f"  Offset: {offset:+.1f}px")
        print(f"  Top margin: {text_top}px")
        print(f"  Bottom margin: {h - 1 - text_bottom}px")

        # Also find button chrome bounds (non-window-background)
        window_bg = img.getpixel((0, 0))
        chrome_rows = []
        for row in range(h):
            has_chrome = False
            for col in range(w):
                pixel = img.getpixel((col, row))
                diff = sum(abs(a - b) for a, b in zip(pixel[:3], window_bg[:3]))
                if diff > 30:
                    has_chrome = True
                    break
            if has_chrome:
                chrome_rows.append(row)

        if chrome_rows:
            chrome_top = chrome_rows[0]
            chrome_bottom = chrome_rows[-1]
            print(f"\nButton chrome:")
            print(f"  Rows: {chrome_top} to {chrome_bottom}")
            print(f"  Text position within chrome:")
            print(f"    From chrome top: {text_top - chrome_top}px")
            print(f"    From chrome bottom: {chrome_bottom - text_bottom}px")
    else:
        print("Could not detect text")


app.after(500, debug_info)
app.after(3000, app.destroy)
app.mainloop()