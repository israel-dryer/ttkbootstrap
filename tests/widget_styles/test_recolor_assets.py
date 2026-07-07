"""Manifest-backed recolorable element asset tests."""
from pathlib import Path

import pytest

import ttkbootstrap as ttk
from ttkbootstrap.style.assets import Assets
from ttkbootstrap.style.elements import RecolorRenderer


def test_black_white_and_alpha_channels_are_preserved():
    image = RecolorRenderer.render(
        "checkbox_checked", (36, 36), white="#112233", black="#445566")

    assert image.getpixel((26, 11)) == (0x11, 0x22, 0x33, 255)
    assert image.getpixel((4, 0)) == (0x44, 0x55, 0x66, 255)
    assert image.getpixel((0, 0))[3] == 0


def test_magenta_is_an_optional_fill_channel():
    with pytest.raises(ValueError, match="provide magenta"):
        RecolorRenderer.render(
            "slider_handle", (44, 44), white="#ffffff", black="#222222")

    image = RecolorRenderer.render(
        "slider_handle", (44, 44), white="#ffffff", black="#222222",
        magenta="#123456")
    assert image.getpixel((21, 10)) == (0x12, 0x34, 0x56, 255)


def test_flip_and_rotation_transform_pixels_and_metadata(root):
    normal = RecolorRenderer.render(
        "switch_round", (76, 36), white="#ff0000", black="#00ff00")
    flipped = RecolorRenderer.render(
        "switch_round", (76, 36), white="#ff0000", black="#00ff00",
        transform="flip-x")
    assert normal.getpixel((19, 18)) == flipped.getpixel((56, 18))
    assert normal.getpixel((57, 18)) == flipped.getpixel((18, 18))

    horizontal = RecolorRenderer.metadata("progressbar_default", root.style.scaling)
    vertical = RecolorRenderer.metadata(
        "progressbar_default", root.style.scaling, "rotate-90")
    assert (horizontal.width, horizontal.height, horizontal.border) == (16, 8, (4, 0))
    assert (vertical.width, vertical.height, vertical.border) == (8, 16, (0, 4))


def test_assets_recolor_dedupes_complete_render_key(root):
    assets = Assets(root.style)
    first = assets.recolor(
        "slider_handle", white="#ffffff", black="#222222", magenta="#336699")
    same = assets.recolor(
        "slider_handle", white="#ffffff", black="#222222", magenta="#336699")
    changed = assets.recolor(
        "slider_handle", white="#ffffff", black="#222222", magenta="#663399")

    assert first.image == same.image
    assert first.meta == same.meta
    assert changed.image != first.image


def test_target_widget_styles_use_raster_layouts(root):
    scrollbar = ttk.Scrollbar(root, bootstyle="primary", orient="horizontal")
    thin = ttk.Progressbar(root, bootstyle="thin", orient="vertical")
    root.update_idletasks()

    scrollbar_layout = repr(root.style.layout(scrollbar.cget("style"))).lower()
    assert "arrow" not in scrollbar_layout
    assert scrollbar.cget("style") == "primary.Horizontal.TScrollbar"
    assert thin.cget("style") == "Thin.Vertical.TProgressbar"


def test_indicator_layouts_space_image_from_label(root):
    widgets = (
        ttk.Checkbutton(root, text="Check", bootstyle="primary"),
        ttk.Radiobutton(root, text="Radio", bootstyle="primary"),
        ttk.Checkbutton(root, text="Round", bootstyle="round-toggle"),
        ttk.Checkbutton(root, text="Square", bootstyle="square-toggle"),
    )
    root.update_idletasks()

    for widget in widgets:
        ttkstyle = widget.cget("style")
        rendered = repr(root.style.layout(ttkstyle))
        indicator = f"{ttkstyle}.indicator"
        spacer = f"{ttkstyle}.spacer"
        assert indicator in rendered
        assert spacer in rendered
        assert rendered.index(indicator) < rendered.index(spacer)


@pytest.mark.parametrize("bootstyle", ["primary", "primary-thin"])
def test_progressbar_layout_stretches_only_along_orientation(root, bootstyle):
    horizontal = ttk.Progressbar(
        root, bootstyle=bootstyle, orient="horizontal")
    vertical = ttk.Progressbar(
        root, bootstyle=bootstyle, orient="vertical")
    root.update_idletasks()

    h_layout = root.style.layout(horizontal.cget("style"))
    v_layout = root.style.layout(vertical.cget("style"))
    h_bar_options = h_layout[0][1]["children"][0][1]
    v_bar_options = v_layout[0][1]["children"][0][1]
    assert h_bar_options["sticky"] == "we"
    assert v_bar_options["sticky"] == "ns"
    assert root.style.lookup(
        horizontal.cget("style"), "background") == root.style.colors.bg
    assert root.style.lookup(
        vertical.cget("style"), "background") == root.style.colors.bg


@pytest.mark.parametrize("bootstyle", ["primary", "primary-round"])
def test_scrollbar_layout_stretches_only_along_orientation(root, bootstyle):
    horizontal = ttk.Scrollbar(
        root, bootstyle=bootstyle, orient="horizontal")
    vertical = ttk.Scrollbar(
        root, bootstyle=bootstyle, orient="vertical")
    root.update_idletasks()

    h_layout = root.style.layout(horizontal.cget("style"))
    v_layout = root.style.layout(vertical.cget("style"))
    h_thumb_options = h_layout[0][1]["children"][0][1]
    v_thumb_options = v_layout[0][1]["children"][0][1]
    assert h_thumb_options["sticky"] == "we"
    assert v_thumb_options["sticky"] == "ns"
    assert h_layout[0][0] == "Horizontal.Scrollbar.trough"
    assert v_layout[0][0] == "Vertical.Scrollbar.trough"
    # the trough is now a subtle *visible* track (2.0 restyle), and every region
    # is that trough color so the whole widget reads as one track
    from ttkbootstrap.style.builders.scrollbar import _scrollbar_trough
    trough = _scrollbar_trough(root.style._get_builder())
    for sb in (horizontal, vertical):
        assert root.style.lookup(sb.cget("style"), "troughcolor") == trough
        assert root.style.lookup(sb.cget("style"), "background") == trough


def test_element_assets_are_packaged_next_to_style_module():
    elements_dir = Path(ttk.__file__).parent / "assets" / "elements"
    assert (elements_dir / "manifest.json").is_file()
    assert (elements_dir / "slider-handle.png").is_file()
