"""Root-bound scaling and asset-geometry regression tests."""
import ast
from math import floor
from pathlib import Path

import pytest

from ttkbootstrap import utility
from ttkbootstrap.style.assets import Assets
from ttkbootstrap.style.builders_ttk import StyleBuilderTTK
from ttkbootstrap.style.elements import RecolorRenderer
from ttkbootstrap.style.scaling import Scaling


class _FakeTk:
    def __init__(self, windowing_system, scaling):
        self.windowing_system = windowing_system
        self.scaling = scaling

    def call(self, *args):
        if args == ("tk", "windowingsystem"):
            return self.windowing_system
        if args == ("tk", "scaling"):
            return self.scaling
        raise AssertionError(args)


class _FakeRoot:
    def __init__(self, windowing_system, scaling):
        self.tk = _FakeTk(windowing_system, scaling)

    def _root(self):
        return self

    def winfo_fpixels(self, value):
        assert value == "1i"
        return self.tk.scaling * 72


@pytest.mark.parametrize(
    ("factor", "expected"),
    [
        (1.00, (22, 20, 6, 1)),
        (1.25, (28, 25, 8, 1)),
        (1.50, (33, 30, 9, 2)),
        (2.00, (44, 40, 12, 2)),
    ],
)
def test_logical_matrix_uses_round_half_up(factor, expected):
    scaling = Scaling(_FakeRoot("win32", (4 / 3) * factor))
    assert tuple(scaling.logical(value) for value in (22, 20, 6, 1)) == expected
    assert scaling.logical((22, 6)) == [expected[0], expected[2]]


@pytest.mark.parametrize(
    ("windowing_system", "baseline"),
    [("win32", 4 / 3), ("x11", 4 / 3), ("aqua", 1.0)],
)
def test_platform_baseline_and_nominal_noise(windowing_system, baseline):
    scaling = Scaling(_FakeRoot(windowing_system, baseline * 1.00049))
    assert scaling.baseline == baseline
    assert scaling.factor == 1.0


def test_source_conversion_rounds_only_at_final_boundary():
    scaling = Scaling(_FakeRoot("x11", (4 / 3) * 1.25))
    assert scaling.source(5, source_scale=2) == 3
    assert scaling.source((5, 8), source_scale=2) == [3, 5]


def test_zero_minimum_negative_and_sequence_contracts():
    scaling = Scaling(_FakeRoot("x11", 4 / 3))
    assert scaling.logical(0, minimum=1) == 0
    assert scaling.logical(0.1, minimum=1) == 1
    assert scaling.logical(0.5) == 1
    assert scaling.logical(-0.5) == -1
    assert scaling.logical((1, 2)) == [1, 2]
    assert scaling.logical([1, 2]) == [1, 2]
    assert scaling.logical("1") is None


def test_custom_factor_is_not_forced_to_quarter_step():
    scaling = Scaling(_FakeRoot("x11", (4 / 3) * 1.31))
    assert scaling.factor == pytest.approx(1.31)


def test_tk_scaling_falls_back_to_screen_pixels_per_inch():
    root = _FakeRoot("x11", 1.75)
    original_call = root.tk.call

    def call(*args):
        if args == ("tk", "scaling"):
            raise RuntimeError("unavailable")
        return original_call(*args)

    root.tk.call = call
    assert Scaling(root).tk_scaling == 1.75


def test_source_scale_and_render_origin_validation():
    scaling = Scaling(_FakeRoot("x11", 4 / 3))
    with pytest.raises(ValueError, match="source_scale"):
        scaling.source(1, source_scale=0)
    assert scaling.render_origin(4.5, oversample=3) == 6
    assert scaling.render_origin(-4.5, oversample=3) == -6
    with pytest.raises(ValueError, match="oversample"):
        scaling.render_origin(1, oversample=0)


def test_image_size_contract():
    scaling = Scaling(_FakeRoot("x11", 4 / 3))
    assert scaling.image_size(15) == (15, 15)
    assert scaling.image_size((15, 9)) == (15, 9)
    with pytest.raises(TypeError, match="two-item sequence"):
        scaling.image_size((1, 2, 3))


def test_public_utility_reuses_root_service():
    root = _FakeRoot("x11", (4 / 3) * 1.5)
    service = Scaling.for_widget(root)
    assert Scaling.for_widget(root) is service
    assert utility.scale_size(root, [22, 6]) == [33, 9]


def test_style_builder_utility_and_assets_share_root_service(root):
    builder = StyleBuilderTTK(build=False)
    assert builder.style.scaling is Scaling.for_widget(root)
    assert builder.assets.scaling is builder.style.scaling


def test_window_and_style_initialize_scaling_before_style_builds():
    package = Path(__file__).parents[1] / "src" / "ttkbootstrap"
    window_source = (package / "window.py").read_text(encoding="utf-8")
    init_source = window_source[window_source.index("class App"):]
    assert init_source.index("utility.enable_high_dpi_awareness()") < init_source.index(
        "super().__init__(**kwargs)"
    )
    assert init_source.index("super().__init__(**kwargs)") < init_source.index(
        "utility.enable_high_dpi_awareness(self, scaling)"
    ) < init_source.index("self._style = Style(theme")

    engine_source = (package / "style" / "engine.py").read_text(encoding="utf-8")
    style_init = engine_source[engine_source.index("class Style"):]
    assert style_init.index("super().__init__()") < style_init.index(
        "self.scaling = Scaling.for_widget(self.master)"
    ) < style_init.index("self.theme_use(theme)")


APPROVED_MANIFEST_GEOMETRY = {
    "checkbox_checked": ((18, 18), 0, 0),
    "checkbox_unchecked": ((18, 18), 0, 0),
    "checkbox_indeterminate": ((18, 18), 0, 0),
    "radiobutton": ((18, 18), 0, 0),
    "switch_round": ((38, 18), 0, 0),
    "switch_square": ((38, 18), 0, 0),
    "slider_handle": ((22, 22), 0, 0),
    "slider_track": ((12, 6), (2, 0), 0),
    "progressbar_default": ((16, 8), (4, 0), 0),
    "progressbar_thin": ((8, 4), (2, 0), 0),
    "sizegrip": ((8, 8), (0, 0), 0),
}


def _scaled(value, factor):
    def one(item):
        return floor(item * factor + 0.5) if item > 0 else 0

    if isinstance(value, int):
        return one(value)
    return tuple(one(item) for item in value)


def test_manifest_records_approved_logical_geometry():
    assert set(RecolorRenderer._load_manifest()["images"]) == set(
        APPROVED_MANIFEST_GEOMETRY
    )
    for name, (size, border, padding) in APPROVED_MANIFEST_GEOMETRY.items():
        info = RecolorRenderer.info(name)
        assert tuple(info["size"]) == size
        assert tuple(info["source_size"]) == RecolorRenderer._source(name).size
        actual_border = info["border"]
        actual_border = (
            tuple(actual_border)
            if isinstance(actual_border, list)
            else actual_border
        )
        assert actual_border == border
        assert info["padding"] == padding


@pytest.mark.parametrize("factor", [1.00, 1.25, 1.50, 2.00])
def test_manifest_geometry_and_image_matrix(root, factor):
    tk = root.tk
    before = float(tk.call("tk", "scaling"))
    try:
        tk.call("tk", "scaling", root.style.scaling.baseline * factor)
        assets = Assets(root.style)
        for name, (logical_size, logical_border, logical_padding) in (
            APPROVED_MANIFEST_GEOMETRY.items()
        ):
            result = assets.recolor(
                name,
                white="#ffffff",
                black="#111111",
                magenta="#336699",
            )
            expected_size = _scaled(logical_size, factor)
            assert (result.meta.width, result.meta.height) == expected_size
            assert result.meta.border == _scaled(logical_border, factor)
            assert result.meta.padding == _scaled(logical_padding, factor)
            assert int(tk.call("image", "width", result.image)) == expected_size[0]
            assert int(tk.call("image", "height", result.image)) == expected_size[1]

        rotated = assets.recolor(
            "slider_track",
            white="#222222",
            black="#222222",
            transform="rotate-90",
        )
        assert (rotated.meta.width, rotated.meta.height) == _scaled((6, 12), factor)
        assert rotated.meta.border == _scaled((0, 2), factor)
    finally:
        tk.call("tk", "scaling", before)


@pytest.mark.parametrize(
    ("factor", "expected"),
    [(1.00, 15), (1.25, 19), (1.50, 23), (2.00, 30)],
)
def test_procedural_and_icon_frames_scale_once_and_keep_exact_size(
    root, factor, expected
):
    tk = root.tk
    before = float(tk.call("tk", "scaling"))

    def empty(_draw, _width, _height):
        pass

    try:
        tk.call("tk", "scaling", root.style.scaling.baseline * factor)
        assets = Assets(root.style)
        names = (
            assets.circle("#123456", 15),
            assets.rect("#234567", 15),
            assets.image(15, empty, "scaling-matrix"),
            assets.icon("square", 15, "#345678"),
        )
        for name in names:
            assert int(tk.call("image", "width", name)) == expected
            assert int(tk.call("image", "height", name)) == expected
    finally:
        tk.call("tk", "scaling", before)


def test_representative_builder_geometry_scales_once(root):
    import tkinter as tk

    from ttkbootstrap.style.builders.button import build_button_style
    from ttkbootstrap.style.builders.entry import build_entry_style
    from ttkbootstrap.style.builders.floodgauge import build_floodgauge_style
    from ttkbootstrap.style.builders.panedwindow import build_panedwindow_style

    style = root.style
    tkapp = root.tk
    before = float(tkapp.call("tk", "scaling"))
    builder = StyleBuilderTTK(build=False)
    recipes = (
        build_button_style,
        build_entry_style,
        build_panedwindow_style,
        build_floodgauge_style,
    )
    try:
        tkapp.call("tk", "scaling", style.scaling.baseline * 1.5)
        for recipe in recipes:
            recipe(builder, "danger")

        assert style.configure("danger.TButton", "padding") == "15 6"
        assert int(style.configure("danger.TButton", "focusthickness")) == 2
        assert int(style.configure("danger.TEntry", "padding")) == 8
        assert int(style.configure("Sash", "sashthickness")) == 3
        assert int(
            style.configure("danger.Horizontal.TFloodgauge", "thickness")
        ) == 75

        text = tk.Text(root)
        builder.builder_tk.update_text_style(text)
        assert int(text.cget("insertwidth")) == 2
        assert int(text.cget("padx")) == 8
    finally:
        tkapp.call("tk", "scaling", before)
        for recipe in recipes[:-1]:
            recipe(builder, "danger")
        for ttk_style in (
            "danger.Horizontal.TFloodgauge",
            "danger.Vertical.TFloodgauge",
        ):
            builder.configure(
                ttk_style,
                thickness=builder.scale_size(50),
                borderwidth=builder.scale_size(1),
            )


GEOMETRY_OPTIONS = {
    "arrowpadding",
    "arrowsize",
    "border",
    "borderwidth",
    "focusthickness",
    "handlepad",
    "handlesize",
    "height",
    "highlightthickness",
    "insertwidth",
    "padding",
    "padx",
    "pady",
    "rowheight",
    "sashpad",
    "sashthickness",
    "sashwidth",
    "shiftrelief",
    "tabmargins",
    "thickness",
    "width",
}
ASSET_METHODS = {"circle", "icon", "image", "rect", "rounded_rect"}


def _contains_scaling_call(node):
    return any(
        isinstance(child, ast.Call)
        and isinstance(child.func, ast.Attribute)
        and child.func.attr in {"logical", "scale_size"}
        for child in ast.walk(node)
    )


def _contains_nonzero_literal(node):
    if isinstance(node, ast.Subscript):
        return _contains_nonzero_literal(node.value)
    if isinstance(node, ast.Constant):
        return (
            isinstance(node.value, (int, float))
            and not isinstance(node.value, bool)
            and node.value != 0
        )
    return any(
        _contains_nonzero_literal(child)
        for child in ast.iter_child_nodes(node)
    )


def _builder_paths():
    root = Path(__file__).parents[1] / "src" / "ttkbootstrap" / "style"
    return [
        root / "builders_tk.py",
        root / "builders_ttk.py",
        *(root / "builders").glob("*.py"),
    ]


def _function_scopes(tree):
    return [
        node
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    ]


def _assignments(scope):
    values = {}
    for node in ast.walk(scope):
        if isinstance(node, ast.Assign):
            targets = node.targets
        elif isinstance(node, ast.AnnAssign):
            targets = [node.target]
        else:
            continue
        for target in targets:
            if isinstance(target, ast.Name):
                values.setdefault(target.id, []).append((node.lineno, node.value))
    return values


def _resolve_name(node, assignments, lineno):
    if not isinstance(node, ast.Name):
        return node
    candidates = [
        (line, value)
        for line, value in assignments.get(node.id, [])
        if line < lineno
    ]
    return max(candidates, default=(0, node))[1]


def _is_logical_toolkit_call(call):
    return (
        isinstance(call.func, ast.Attribute)
        and call.func.attr in ASSET_METHODS
    ) or (
        isinstance(call.func, ast.Name)
        and call.func.id == "icon_element"
    )


def _is_hairline_border(arg, value):
    """A 1px border is a physical hairline, not a scaled logical dimension.

    Solid buttons draw a `borderwidth=1` flat border that should stay a single
    physical pixel at every DPI (scaling it makes it read as a thick 2px+ edge on
    hi-DPI). This narrowly permits the literal `borderwidth=1`; any other width or
    option still must go through the scaling service.
    """
    return (
        arg == "borderwidth"
        and isinstance(value, ast.Constant)
        and value.value == 1
    )


def test_builder_numeric_geometry_is_scaled_or_already_physical():
    violations = []
    for path in _builder_paths():
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for scope in _function_scopes(tree):
            assignments = _assignments(scope)
            calls = (
                node for node in ast.walk(scope) if isinstance(node, ast.Call)
            )
            for call in calls:
                if _is_logical_toolkit_call(call):
                    continue
                for keyword in call.keywords:
                    value = _resolve_name(keyword.value, assignments, call.lineno)
                    if (
                        keyword.arg in GEOMETRY_OPTIONS
                        and _contains_nonzero_literal(value)
                        and not _contains_scaling_call(value)
                        and not _is_hairline_border(keyword.arg, value)
                    ):
                        violations.append(f"{path.name}:{call.lineno}:{keyword.arg}")
    assert not violations, "unscaled literal builder geometry: " + ", ".join(
        violations
    )


def test_builder_asset_inputs_are_logical_not_pre_scaled():
    violations = []
    logical_positions = {
        "circle": (1,),
        "icon": (1,),
        "image": (0,),
        "rect": (1,),
        "rounded_rect": (1, 2),
    }
    logical_keywords = {
        "circle": {"size", "width"},
        "icon": {"size"},
        "image": {"size"},
        "rect": {"size"},
        "rounded_rect": {"size", "radius", "width"},
    }
    for path in _builder_paths():
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for scope in _function_scopes(tree):
            assignments = _assignments(scope)
            calls = (
                node for node in ast.walk(scope) if isinstance(node, ast.Call)
            )
            for call in calls:
                if isinstance(call.func, ast.Name) and call.func.id == "icon_element":
                    logical_values = [
                        keyword.value
                        for keyword in call.keywords
                        if keyword.arg in {"size", "border", "padding", "width", "height"}
                    ]
                    for value in logical_values:
                        value = _resolve_name(value, assignments, call.lineno)
                        if _contains_scaling_call(value):
                            violations.append(
                                f"{path.name}:{call.lineno}:icon_element"
                            )
                    continue
                if (
                    not isinstance(call.func, ast.Attribute)
                    or call.func.attr not in ASSET_METHODS
                ):
                    continue
                values = [
                    call.args[index]
                    for index in logical_positions[call.func.attr]
                    if len(call.args) > index
                ]
                values.extend(
                    keyword.value
                    for keyword in call.keywords
                    if keyword.arg in logical_keywords[call.func.attr]
                )
                for value in values:
                    value = _resolve_name(value, assignments, call.lineno)
                    if _contains_scaling_call(value):
                        violations.append(
                            f"{path.name}:{call.lineno}:{call.func.attr}"
                        )
    assert not violations, "pre-scaled toolkit asset size: " + ", ".join(
        violations
    )
