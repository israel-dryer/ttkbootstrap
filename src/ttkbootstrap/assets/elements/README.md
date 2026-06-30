# Recolorable ttk element assets

These 2x PNG templates are derived or adapted from bootstack's element asset
set and are distributed under ttkbootstrap's project license.

The source palette is semantic: black and white are independently recolorable
structural channels, magenta is an optional third fill channel, and alpha stays
transparent. Magenta is currently used only for the slider handle center; it is
not a focus channel. There is no cyan/teal channel.

`manifest.json` records source-pixel dimensions separately from logical UI
size and logical ttk border/padding metadata. Horizontal sources may be flipped
or quarter-turned at render time; transformed pixels and metadata always use the
same transform.
