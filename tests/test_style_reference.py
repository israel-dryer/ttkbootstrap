"""Structural sync test for the generated Style Reference (docs Workstream H).

Unlike the bootstyle reference (pure-Python-derived, so byte-compared), the
Style Reference *pages* carry live ttk introspection (element options, layout,
states) that varies by Tcl/Tk version and OS -- byte-comparing them would make
CI flake on a Tk point-release. So this test is deliberately **structural**:

- the index page is registry-derived (no introspection), so it *is* byte-checked
  -- adding a builder family without regenerating fails here;
- every family the registry produces must have a committed page.

Content freshness is the author's documented offline regen step
(`python tools/generate_style_reference.py`).
"""
import importlib.util
import pathlib


_REPO = pathlib.Path(__file__).resolve().parents[1]
_STYLE_REF_DIR = _REPO / "docs" / "reference" / "style-reference"


def _load_generator():
    path = _REPO / "tools" / "generate_style_reference.py"
    spec = importlib.util.spec_from_file_location("_style_ref_gen", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_style_reference_families_nonempty():
    gen = _load_generator()
    families = gen.style_reference_families()
    assert families, "the builder registry should yield styled families"
    # every family classifies into exactly one index group (render raises otherwise)
    gen.render_index_page()


def test_every_family_has_a_committed_page():
    gen = _load_generator()
    for family in gen.style_reference_families():
        page = _STYLE_REF_DIR / f"{family}.rst"
        assert page.exists(), (
            f"missing Style Reference page {page.name}; regenerate with "
            "`python tools/generate_style_reference.py`"
        )


def test_style_reference_index_is_current():
    # The index is purely registry-derived (families, blurbs, grouping, toctrees)
    # with no introspected content, so a byte-compare is deterministic and CI-safe.
    gen = _load_generator()
    current = (_STYLE_REF_DIR / "index.rst").read_text(encoding="utf-8")
    assert current == gen.render_index_page(), (
        "docs/reference/style-reference/index.rst is stale; regenerate with "
        "`python tools/generate_style_reference.py`"
    )
