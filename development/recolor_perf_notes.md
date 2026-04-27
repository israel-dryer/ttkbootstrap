# `recolor_element_image` perf — analysis and fix

This branch (`perf/vectorize-recolor-element-image`, off `release/v2`)
replaces the per-pixel Python loop in `recolor_element_image` with PIL
C-level ops. Notes kept here so the image-vs-native-clam decision can be
revisited with real numbers in hand.

## The bug

`src/ttkbootstrap/style/utility.py` had a pure-Python double loop touching
every pixel — each iteration unpacked a tuple, called `getpixel()` on a
grayscale layer, did three `round()` calls, and re-assigned a tuple. For a
button at 2x source resolution that's ~32k iterations of interpreted
Python per recolor.

The function is cached, so it only ran on misses. But every theme switch
is a cache miss for the new theme's color set — exactly the slow path
felt at runtime. Realistic call volume: ~50 recolors per cold theme
switch.

## The fix (PIL-only, no new deps)

The Python loop was replaced with three PIL operations, all running in C:

1. **Luminance interp via per-channel LUTs.** A 256-entry list per output
   channel, applied to the grayscale image with `Image.point()`. Equivalent
   to `out_c = round(bg_c + (fg_c - bg_c) * gray / 255)` but vectorized.
2. **Magenta passthrough.** Built as a 0/255 mask via three more LUTs
   (one per channel checking `r==255`, `g==0`, `b==255`), AND-ed together
   with `ImageChops.multiply`, then `Image.composite` swaps in the
   magenta-replacement color. Original alpha is restored after.
3. **Transparent flatten.** `Image.alpha_composite` against a solid
   backing image. Matches the old `out = trans*(1-a) + rgb*a, alpha=255`
   formula exactly.

No new dependency. Numpy was considered but rejected — PIL's C ops are in
the same ballpark and ship with Pillow already.

## Verification

`development/verify_recolor_equivalence.py` runs the old and new paths
side-by-side on six representative element images covering all magenta
and transparent permutations:

```
case                                            dR   dG   dB   dA  status
button: solid recolor                            0    0    0    0  OK
input: with transparent flatten                  0    0    0    0  OK
checkbox: with magenta                           0    0    0    0  OK
switch: alpha edges                              0    0    0    0  OK
slider: transparent + handle alpha               0    0    0    0  OK
badge: magenta + transparent                     0    0    0    0  OK
```

**Bit-identical output** across all four channels for every test case. No
visual regression possible.

## Measured speedup

`development/bench_recolor.py` against nine sample assets at source
resolution:

```
image                              pixels   old (ms)   new (ms)  speedup
button-default.png                   7744       4.93     0.1348    36.6x
button-compact.png                   3600       2.22     0.1199    18.5x
input-default.png                    7744       4.84     0.1293    37.5x
input-compact.png                    3600       2.24     0.1188    18.8x
checkbox-checked.png                 2304       1.36     0.1131    12.0x
switch-on.png                        3840       2.20     0.1216    18.1x
slider-handle.png                    2304       0.73     0.1133     6.4x
badge-pill.png                       1024       0.57     0.1099     5.2x
border.png                           7744       4.88     0.1329    36.7x
TOTAL (one pass per image)          39904      23.97     1.0936    21.9x
```

**~22× aggregate speedup.** The new path has near-constant per-image
overhead (~0.11 ms) — bigger images benefit more.

Projected for a realistic theme switch (50 recolor calls cold cache):

```
old impl:  133.1 ms
new impl:    6.1 ms
saved:     127.1 ms
```

The remaining ~6 ms is well below the noise floor of normal Tk redraw
work; theme switching should now feel instantaneous.

## Decision implications: image-based vs. native clam

With this fix landed, the perf argument for going native-clam essentially
disappears. The remaining arguments split:

**Stay image-based** (this branch alone):
- Rounded corners on every widget — preserved
- Single-source-of-truth recoloring pipeline — preserved
- 50+ PNG asset maintenance burden — unchanged
- macOS rendering inconsistency — **unchanged** (this is the one perf
  didn't address; it comes from PIL/Tk image scaling on Retina, not from
  recolor speed)

**Go native clam** (the parallel `feature/native-clam-styling` branch):
- Square corners
- Eliminates the asset pipeline entirely for migrated widgets
- Fixes macOS inconsistency for migrated widgets
- More maintainable, smaller builders

**Hybrid** (what `feature/native-clam-styling` actually does):
- Native clam for buttons + base inputs (no image needed)
- Image-based for genuinely custom indicators (checkbox, radio, switch,
  slider handle, badge, striped progressbar, notebook pill)
- Best of both, plus this perf fix benefits the kept-image widgets

## Bottom line

Perf is no longer a reason to migrate. The remaining decision is about
**macOS visual consistency** (clam wins) vs. **rounded corners + visual
parity with v1** (images win). Both are aesthetic/UX calls, not perf
calls.

If the user base is mostly Windows/Linux scientific apps and rounded
corners matter, sticking with images and shipping just this fix is a
defensible path. If macOS users are growing or you want to shrink the
asset surface, the hybrid native-clam plan on the other branch still has
merit on those grounds — it's just not urgent.