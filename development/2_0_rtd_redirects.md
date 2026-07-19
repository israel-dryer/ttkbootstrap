# Read the Docs redirects for the 2.0 docs rebuild

The 2.0 release moved the documentation from **mkdocs** to **Sphinx** and
reorganized the information architecture. Two things changed for every page:

1. **URL shape.** mkdocs used directory URLs (`/en/latest/foo/`); Sphinx serves
   `/en/latest/foo.html`.
2. **Location.** Pages were regrouped into a new IA (Getting started / User guide
   / Widgets / Reference / Themes).

So every old inbound link — bookmarks, Google results, Stack Overflow answers,
old README/PyPI links — now 404s. These redirects map the old paths to their new
homes.

## How to apply

Read the Docs does **not** read redirects from `.readthedocs.yaml`. Add them in
the project dashboard: **Admin → Redirects**, or via the
[RTD redirects API](https://docs.readthedocs.io/en/stable/api/v3.html#redirects).
The `From URL` is the path under the version root (RTD applies it across
versions). Wildcards use a trailing `*`, captured as `:splat` in the `To URL`.

`docs/404.rst` (the `sphinx-notfound-page` extension) is the safety net for
anything not listed here.

## Keep the last 1.x version active

Old **versioned** builds keep their original mkdocs URLs, so `/en/v1.x/...` links
still resolve as long as that version is not deactivated. Only `latest`/`stable`
serve the new structure and need these redirects — confirm `stable` is not
silently pointing 1.x readers at 2.0's pages.

## Exact redirects (highest-traffic pages, land precisely)

| Type | From URL | To URL |
|---|---|---|
| Exact | `/en/latest/gettingstarted/tutorial/` | `/en/latest/user-guide/getting-started/quickstart.html` |
| Exact | `/en/latest/gettingstarted/installation/` | `/en/latest/user-guide/getting-started/installation.html` |
| Exact | `/en/latest/gettingstarted/legacy/` | `/en/latest/user-guide/getting-started/migrating.html` |
| Exact | `/en/latest/themes/themecreator/` | `/en/latest/user-guide/feature-guides/theming.html` |

## Per-widget redirects (`styleguide/<w>/` → `widgets/<w>.html`, 1:1)

These old style-guide slugs map one-to-one to the new widget pages. Add as Exact
redirects (or a single `styleguide/*` wildcard — see below — if you prefer fewer
rules and don't mind landing on the catalog index for the odd ones out).

| From URL | To URL |
|---|---|
| `/en/latest/styleguide/button/` | `/en/latest/widgets/button.html` |
| `/en/latest/styleguide/checkbutton/` | `/en/latest/widgets/checkbutton.html` |
| `/en/latest/styleguide/combobox/` | `/en/latest/widgets/combobox.html` |
| `/en/latest/styleguide/dateentry/` | `/en/latest/widgets/dateentry.html` |
| `/en/latest/styleguide/entry/` | `/en/latest/widgets/entry.html` |
| `/en/latest/styleguide/floodgauge/` | `/en/latest/widgets/floodgauge.html` |
| `/en/latest/styleguide/frame/` | `/en/latest/widgets/frame.html` |
| `/en/latest/styleguide/label/` | `/en/latest/widgets/label.html` |
| `/en/latest/styleguide/labelframe/` | `/en/latest/widgets/labelframe.html` |
| `/en/latest/styleguide/menubutton/` | `/en/latest/widgets/menubutton.html` |
| `/en/latest/styleguide/meter/` | `/en/latest/widgets/meter.html` |
| `/en/latest/styleguide/notebook/` | `/en/latest/widgets/notebook.html` |
| `/en/latest/styleguide/panedwindow/` | `/en/latest/widgets/panedwindow.html` |
| `/en/latest/styleguide/progressbar/` | `/en/latest/widgets/progressbar.html` |
| `/en/latest/styleguide/radiobutton/` | `/en/latest/widgets/radiobutton.html` |
| `/en/latest/styleguide/scale/` | `/en/latest/widgets/scale.html` |
| `/en/latest/styleguide/scrollbar/` | `/en/latest/widgets/scrollbar.html` |
| `/en/latest/styleguide/separator/` | `/en/latest/widgets/separator.html` |
| `/en/latest/styleguide/sizegrip/` | `/en/latest/widgets/sizegrip.html` |
| `/en/latest/styleguide/spinbox/` | `/en/latest/widgets/spinbox.html` |
| `/en/latest/styleguide/treeview/` | `/en/latest/widgets/treeview.html` |
| `/en/latest/styleguide/datepickerpopup/` | `/en/latest/widgets/dateentry.html` |
| `/en/latest/styleguide/legacywidgets/` | `/en/latest/widgets/index.html` |

## Section wildcards (catch-all for the rest)

Add these so *any* remaining old path in a retired tree lands on the nearest new
home instead of 404ing. Put wildcards **after** the exact rules above (exacts win).

| Type | From URL | To URL |
|---|---|---|
| Wildcard | `/en/latest/styleguide/*` | `/en/latest/widgets/index.html` |
| Wildcard | `/en/latest/api/*` | `/en/latest/reference/index.html` |
| Wildcard | `/en/latest/themes/*` | `/en/latest/themes.html` |
| Wildcard | `/en/latest/gettingstarted/*` | `/en/latest/user-guide/getting-started/quickstart.html` |
| Wildcard | `/en/latest/gallery/*` | `/en/latest/index.html` |
| Wildcard | `/en/latest/cookbook/*` | `/en/latest/user-guide/index.html` |

Notes:
- The old **API** tree (`api/...`) had a completely different structure; a
  catch-all to the reference landing is safer than mapping each page.
- **Gallery** and **Cookbook** were retired in 2.0 (their content wasn't carried
  over); send them to the home / user-guide landing.
- `about/` and `license/` still exist under `about/` — add exacts if those old
  paths saw traffic (`/en/latest/about/` → `/en/latest/about/index.html`,
  `/en/latest/license/` → `/en/latest/about/license.html`).