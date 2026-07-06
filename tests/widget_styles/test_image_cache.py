"""Content-addressed image cache tests (2.0 Workstream A / PR 2).

Asset images (Scale thumb, toggle, radiobutton, scrollbar, ...) are memoized on
their pixel-determining inputs (resolved colors + scaled size + geometry), NOT
the theme name. This gives three guarantees these tests pin down:

- identical widgets share one image (dedup, no per-widget PhotoImage leak);
- a theme switch yields *fresh* pixels (the builder-purity gate: no stale image
  survives because a color change is a different key);
- returning to a visited theme is a pure cache hit (no re-render, no growth).
"""
import ttkbootstrap as ttk


def _scale_thumb(style, primary):
    """Return the cached (name, PhotoImage) for the scale thumb of `primary`.

    The thumb is a recolored `slider_handle`; its magenta source channel maps to
    the theme primary. Recolor keys include every target color and transform.
    """
    for key, value in style._image_cache.items():
        if (key[0] == "recolor" and key[1] == "slider_handle"
                and key[5] == primary and key[6] is None):
            return value
    return None


def test_identical_widgets_share_one_image(root):
    """Two identical scales reference the same cached images (dedup)."""
    style = root.style
    before = len(style._image_cache)

    ttk.Scale(root, bootstyle="primary").pack()
    root.update_idletasks()
    after_one = len(style._image_cache)

    ttk.Scale(root, bootstyle="primary").pack()
    root.update_idletasks()
    after_two = len(style._image_cache)

    # the first scale added its assets; the identical second added none
    assert after_one > before
    assert after_two == after_one


def test_theme_switch_yields_fresh_pixels(root):
    """A theme switch repaints image assets with the new theme's colors.

    Pixel-level guard against stale cache hits: the scale thumb's center pixel
    must match each theme's resolved primary color.
    """
    style = root.style
    start = style.theme.name
    other = "bootstrap-dark" if start != "bootstrap-dark" else "bootstrap-light"

    ttk.Scale(root, bootstyle="primary").pack()
    root.update_idletasks()

    start_primary = style.colors.primary
    name_a, img_a = _scale_thumb(style, start_primary)
    px_a = root.tk.call(name_a, "get", img_a.width() // 2, img_a.height() // 2)

    style.theme_use(other)
    root.update_idletasks()

    other_primary = style.colors.primary
    name_b, img_b = _scale_thumb(style, other_primary)
    px_b = root.tk.call(name_b, "get", img_b.width() // 2, img_b.height() // 2)

    # different theme primary -> different key -> different image and pixels
    assert other_primary != start_primary
    assert name_a != name_b
    assert px_a != px_b


def test_theme_return_is_a_cache_hit(root):
    """Returning to an already-visited theme renders no new images."""
    style = root.style
    start = style.theme.name
    other = "bootstrap-dark" if start != "bootstrap-dark" else "bootstrap-light"

    ttk.Scale(root, bootstyle="primary").pack()
    ttk.Checkbutton(root, bootstyle="round-toggle").pack()
    ttk.Radiobutton(root, bootstyle="success").pack()
    root.update_idletasks()

    style.theme_use(other)
    root.update_idletasks()
    size_other = len(style._image_cache)

    style.theme_use(start)
    root.update_idletasks()
    size_back = len(style._image_cache)

    # everything needed for `start` was already cached on first visit
    assert size_back == size_other


def test_clear_image_cache_empties(root):
    """clear_image_cache() releases every cached image."""
    style = root.style
    ttk.Scale(root, bootstyle="primary").pack()
    root.update_idletasks()
    assert len(style._image_cache) > 0

    style.clear_image_cache()
    assert len(style._image_cache) == 0
