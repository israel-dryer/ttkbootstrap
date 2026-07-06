"""Curated built-in theme families for ttkbootstrap 2.0 (Workstream E).

Each family is a `Theme` (semantic anchors + light/dark background blocks) that
generates a well-contrasted `<name>-light` / `<name>-dark` pair. The engine
registers `CURATED_THEMES` at startup (`Style._load_themes`).

Ten families adapt bootstack's catalog (which itself adapts well-known,
open-licensed designer palettes: Nord, Solarized, Catppuccin, Gruvbox, Dracula,
Tokyo Night, One, Everforest); five migrate distinctive ttkbootstrap identities
(vapor, minty, pulse, united, sandstone), keeping their original mode's accents
and authoring a generated opposite mode. The legacy 40-theme catalog is opt-in
via `ttkbootstrap.install_legacy_themes()` (see `themes/legacy.py`).
"""
from ttkbootstrap.style.theme import Theme

# --- From bootstack (10) ----------------------------------------------------

BOOTSTRAP = Theme(
    name="bootstrap",
    primary="#0d6efd", success="#198754", info="#0dcaf0", warning="#ffc107", danger="#dc3545",
    light=dict(background="#ffffff", foreground="#212529"),
    dark=dict(background="#212529", foreground="#f8f9fa"),
)

PYDATA = Theme(
    name="pydata",
    primary="#0a7d91", success="#198754", info="#0dcaf0", warning="#ffc107", danger="#dc3545",
    secondary="#8045e5", neutral="#677384",
    light=dict(background="#ffffff", foreground="#222832"),
    dark=dict(background="#14181e", foreground="#ced6dd"),
)

NORD = Theme(
    name="nord",
    primary="#5e81ac", success="#a3be8c", info="#88c0d0", warning="#ebcb8b", danger="#bf616a",
    secondary="#b48ead", neutral="#4c566a",
    light=dict(background="#eceff4", foreground="#2e3440"),
    dark=dict(background="#2e3440", foreground="#eceff4"),
)

SOLARIZED = Theme(
    name="solarized",
    primary="#268bd2", success="#859900", info="#2aa198", warning="#b58900", danger="#dc322f",
    secondary="#6c71c4", neutral="#839496",
    light=dict(background="#f6f1e9", foreground="#586e75"),
    dark=dict(background="#002b36", foreground="#93a1a1"),
)

CATPPUCCIN = Theme(
    name="catppuccin",
    primary="#8839ef", success="#40a02b", info="#179299", warning="#df8e1d", danger="#d20f39",
    secondary="#ea76cb", neutral="#8c8fa1",
    light=dict(background="#eff1f5", foreground="#4c4f69"),
    dark=dict(background="#1e1e2e", foreground="#cdd6f4"),
)

GRUVBOX = Theme(
    name="gruvbox",
    primary="#458588", success="#98971a", info="#689d6a", warning="#d79921", danger="#cc241d",
    secondary="#d65d0e", neutral="#928374",
    light=dict(background="#f2ede9", foreground="#3c3836"),
    dark=dict(background="#282828", foreground="#ebdbb2"),
)

DRACULA = Theme(
    name="dracula",
    primary="#bd93f9", success="#50fa7b", info="#8be9fd", warning="#ffb86c", danger="#ff5555",
    secondary="#ff79c6", neutral="#6272a4",
    light=dict(background="#f8f8f2", foreground="#282a36"),
    dark=dict(background="#282a36", foreground="#f8f8f2"),
)

TOKYO_NIGHT = Theme(
    name="tokyo-night",
    primary="#7aa2f7", success="#9ece6a", info="#7dcfff", warning="#e0af68", danger="#f7768e",
    secondary="#bb9af7", neutral="#565f89",
    light=dict(background="#e1e2e7", foreground="#343b58"),
    dark=dict(background="#1a1b26", foreground="#c0caf5"),
)

ONE = Theme(
    name="one",
    primary="#4078f2", success="#50a14f", info="#0184bc", warning="#c18401", danger="#e45649",
    secondary="#a626a4", neutral="#a0a1a7",
    light=dict(background="#fafafa", foreground="#383a42"),
    dark=dict(background="#282c34", foreground="#abb2bf"),
)

EVERFOREST = Theme(
    name="everforest",
    primary="#3a94c5", success="#8da101", info="#35a77c", warning="#dfa000", danger="#f85552",
    secondary="#df69ba", neutral="#939f91",
    light=dict(background="#edf3ed", foreground="#5c6a72"),
    dark=dict(background="#2d353b", foreground="#d3c6aa"),
)

# --- Migrated from ttkbootstrap (5) -----------------------------------------
# Original-mode accents/backgrounds are the authored values; the opposite-mode
# background blocks are generated new (starting points; tuned in the visual
# gate).

VAPOR = Theme(  # synthwave neon (originally dark)
    name="vapor",
    primary="#6e40c0", success="#3af180", info="#1da2f2", warning="#ffbd05", danger="#e34b54",
    secondary="#ea38b8", neutral="#6c5a8c",
    light=dict(background="#f7f3fc", foreground="#2a1758"),
    dark=dict(background="#190831", foreground="#32fbe2"),
)

MINTY = Theme(  # fresh mint pastel (originally light)
    name="minty",
    primary="#78c2ad", success="#56cc9d", info="#6cc3d5", warning="#ffce67", danger="#ff7851",
    secondary="#f3969a", neutral="#a0aca6",
    light=dict(background="#ffffff", foreground="#5a5a5a"),
    dark=dict(background="#1a2b27", foreground="#c8e6da"),
)

PULSE = Theme(  # vivid purple (originally light)
    name="pulse",
    primary="#593196", success="#13b955", info="#009cdc", warning="#efa31d", danger="#fc3939",
    neutral="#69676e",
    light=dict(background="#ffffff", foreground="#444444"),
    dark=dict(background="#17141f", foreground="#e9ecef"),
)

UNITED = Theme(  # ubuntu orange (originally light)
    name="united",
    primary="#e95420", success="#38b44a", info="#17a2b8", warning="#efb73e", danger="#df382c",
    neutral="#aea79f",
    light=dict(background="#ffffff", foreground="#333333"),
    dark=dict(background="#2b2119", foreground="#f0e6dd"),
)

SANDSTONE = Theme(  # warm earthy (originally light)
    name="sandstone",
    primary="#325d88", success="#93c54b", info="#29abe0", warning="#f47c3c", danger="#d9534f",
    neutral="#8e8c84",
    light=dict(background="#ffffff", foreground="#3e3f3a"),
    dark=dict(background="#2b2925", foreground="#e8e2d8"),
)

#: All curated built-in theme families, in display order.
CURATED_THEMES = [
    BOOTSTRAP, PYDATA, NORD, SOLARIZED, CATPPUCCIN,
    GRUVBOX, DRACULA, TOKYO_NIGHT, ONE, EVERFOREST,
    VAPOR, MINTY, PULSE, UNITED, SANDSTONE,
]
