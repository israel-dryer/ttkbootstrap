"""Behavioral guards for the private modular ttk builder registry."""

import pytest

import ttkbootstrap as ttk
from ttkbootstrap.style import Bootstyle, ThemeDefinition
from ttkbootstrap.style import builders_ttk as coordinator_module
from ttkbootstrap.style import builders as builders_package
from ttkbootstrap.style.builders import load_builders
from ttkbootstrap.style.builders.registry import (
    BuilderRegistry,
    BuilderRegistryError,
    DuplicateBuilderError,
    FrozenBuilderRegistryError,
    builder_keys,
    registry_is_frozen,
)


EXPECTED_KEYS = {
    ("date", "button"),
    ("default", "button"),
    ("ghost", "button"),
    ("default", "calendar"),
    ("default", "checkbutton"),
    ("default", "combobox"),
    ("default", "entry"),
    ("default", "floodgauge"),
    ("default", "frame"),
    ("card", "frame"),
    ("highlight", "frame"),
    ("default", "label"),
    ("default", "labelframe"),
    ("default", "menubutton"),
    ("default", "notebook"),
    ("default", "panedwindow"),
    ("default", "progressbar"),
    ("default", "radiobutton"),
    ("default", "scale"),
    ("default", "scrollbar"),
    ("default", "separator"),
    ("default", "sizegrip"),
    ("default", "spinbox"),
    ("default", "toggle"),
    ("default", "toolbutton"),
    ("default", "treeview"),
    ("inverse", "label"),
    ("link", "button"),
    ("meter", "label"),
    ("metersubtxt", "label"),
    ("outline", "button"),
    ("outline", "menubutton"),
    ("outline", "toolbutton"),
    ("round", "scrollbar"),
    ("thin", "scrollbar"),
    ("round", "toggle"),
    ("square", "toggle"),
    ("striped", "progressbar"),
    ("table", "treeview"),
    ("thin", "progressbar"),
}


def test_registry_is_complete_frozen_and_idempotent():
    load_builders()
    before = builder_keys()
    load_builders()

    assert before == EXPECTED_KEYS
    assert builder_keys() == before
    assert registry_is_frozen()


def test_loader_does_not_hide_import_failures(monkeypatch):
    previous = builders_package._loaded
    monkeypatch.setattr(builders_package, "_loaded", False)

    def fail_import():
        raise ImportError("broken recipe module")

    monkeypatch.setattr(
        builders_package, "_import_builder_modules", fail_import
    )
    with pytest.raises(ImportError, match="broken recipe module"):
        builders_package.load_builders()
    assert not builders_package._loaded
    builders_package._loaded = previous


def test_coordinator_has_no_recipe_method_or_reflection_surface():
    names = vars(coordinator_module.StyleBuilderTTK)
    recipe_methods = {
        name
        for name in names
        if name.startswith("create_")
        and name.endswith("_style")
        and name != "create_default_style"
    }
    assert not recipe_methods
    assert "name_to_method" not in names


@pytest.mark.parametrize(
    ("variant", "family"),
    [
        ("", "button"),
        ("Default", "button"),
        (" default", "button"),
        ("default", ""),
        ("default", "Button"),
        ("default", "button "),
    ],
)
def test_registry_rejects_noncanonical_keys(variant, family):
    registry = BuilderRegistry()
    with pytest.raises(BuilderRegistryError):
        registry.register(variant, family)


def test_registry_rejects_duplicate_and_late_registration():
    registry = BuilderRegistry()
    with pytest.raises(BuilderRegistryError, match="must be callable"):
        registry.register("default", "label")(None)

    @registry.register("default", "button")
    def first(_builder, _colorname):
        pass

    with pytest.raises(DuplicateBuilderError):

        @registry.register("default", "button")
        def duplicate(_builder, _colorname):
            pass

    registry.freeze()
    with pytest.raises(FrozenBuilderRegistryError):

        @registry.register("outline", "button")
        def late(_builder, _colorname):
            pass


def test_dispatch_distinguishes_missing_from_broken_recipe(
    root, monkeypatch
):
    builder = root.style._get_builder()

    monkeypatch.setattr(
        coordinator_module, "get_builder", lambda _variant, _family: None
    )
    assert not builder.build_style("default", "foreign", "")
    with pytest.raises(LookupError):
        builder.build_style("default", "foreign", "", required=True)

    def broken(_builder, _colorname):
        raise AttributeError("recipe defect")

    monkeypatch.setattr(
        coordinator_module, "get_builder", lambda _variant, _family: broken
    )
    with pytest.raises(AttributeError, match="recipe defect"):
        builder.build_style("default", "button", "")


def test_unregistered_third_party_style_still_passes_through(root):
    class ForeignWidget:
        def cget(self, _option):
            return ""

        def winfo_class(self):
            return "ForeignWidget"

    requested = "Foreign.CustomStyle"
    assert (
        Bootstyle.update_ttk_widget_style(ForeignWidget(), requested)
        == requested
    )


def test_new_theme_keeps_nondefault_recipes_lazy(root):
    style = root.style
    name = "builder-registry-lazy-test"
    style.register_theme(
        ThemeDefinition(
            name=name,
            colors=style.theme.colors,
            themetype=style.theme.type,
        )
    )
    style.theme_use(name)

    assert style.style_exists_in_theme("TButton")
    assert style.style_exists_in_theme("Link.TButton")
    assert style.style_exists_in_theme("TLabel")
    assert not style.style_exists_in_theme("danger.Outline.TButton")

    ttk.Button(root, bootstyle="danger-outline")
    assert style.style_exists_in_theme("danger.Outline.TButton")


@pytest.mark.parametrize(
    ("variant", "family", "styles"),
    [
        (
            "default",
            "separator",
            ("primary.Horizontal.TSeparator", "primary.Vertical.TSeparator"),
        ),
        (
            "thin",
            "progressbar",
            (
                "primary.Thin.Horizontal.TProgressbar",
                "primary.Thin.Vertical.TProgressbar",
            ),
        ),
        (
            "round",
            "scrollbar",
            (
                "primary.Round.Horizontal.TScrollbar",
                "primary.Round.Vertical.TScrollbar",
            ),
        ),
        (
            "default",
            "panedwindow",
            (
                "primary.Horizontal.TPanedwindow",
                "primary.Vertical.TPanedwindow",
            ),
        ),
        (
            "default",
            "calendar",
            ("primary.TCalendar", "Chevron.primary.TButton"),
        ),
    ],
)
def test_multi_output_recipes_keep_related_style_registrations(
    root, variant, family, styles
):
    builder = root.style._get_builder()
    assert builder.build_style(
        variant, family, "primary", required=True
    )
    for style_name in styles:
        assert root.style.style_exists_in_theme(style_name)
