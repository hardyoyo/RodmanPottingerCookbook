# Rodman/Pottinger Cookbook Project

[![CI](https://github.com/hardyoyo/RodmanPottingerCookbook/actions/workflows/ci.yml/badge.svg)](https://github.com/hardyoyo/RodmanPottingerCookbook/actions/workflows/ci.yml)

This is a collection of recipes we use on a regular basis, and will hopefully be
used to produce a family cookbook, if I keep my act together this year.
TLDR, if you're just here for recipes, you can find them in the [recipes](./recipes/) folder.


## Software/Specs Used

* [RecipeMD](https://recipemd.org/): for the excellent markdown recipe format, and a few nice [tools](https://recipemd.org/recommended_tools.html).
* [Cookie](https://github.com/bbugyi200/cookie): for quickly creating a new recipe
* [Pandoc](https://pandoc.org/): for converting recipes into PDF, EPUB, HTML, and DOCX files
* [poppler-utils](https://packages.debian.org/sid/poppler-utils): for its handy `pdfunite` tool to assemble the cover, content, and grocery list into the final PDF
* [Scribus](https://www.scribus.net/): for typesetting the cover page (static `.sla` source, exported as `Coverpage.pdf`)
* [XeLaTeX](https://www.overleaf.com/learn/latex/XeLaTeX): PDF generation engine via Pandoc; also used to render the versioned cover at build time
* [Wikiti Pandoc Book Template](https://github.com/wikiti/pandoc-book-template)

## Getting Started

This project includes a [Devbox](https://www.jetify.com/devbox/docs/quickstart/) configuration, to help you get a development environment going.

Steps to get the cookbook running on your local machine, with Devbox
1. Make sure [Devbox](https://www.jetify.com/devbox/docs/quickstart/) is
   installed
2. `devbox shell` downloads requirements and launches a devbox development environment 
3. skip down to the "how to use" section for commands you can run

NOTE: The first time you run `devbox shell` may take a while to complete due to 
Devbox downloading prerequisites and package catalogs required by Nix. This 
delay is a one-time cost, and future invocations and package additions should 
resolve much faster.

## How to Use

The Makefile is based on the [Wikiti Pandoc Book Template](https://github.com/wikiti/pandoc-book-template),
with significant customization for this project.

### Available Targets

| Target | Description |
|--------|-------------|
| `make pdf` | Build `cookbook.pdf` — the main content PDF (no cover). Easiest for navigating by page number. |
| `make epub` | Build `cookbook.epub` with cross-chapter link resolution and page-reference stripping. |
| `make html` | Build `cookbook.html` (single-page HTML, page refs stripped). |
| `make docx` | Build `cookbook.docx` for Word. |
| `make final` | Assemble the full print-ready PDF: versioned cover + content + grocery list → `RodmanPottingerFamilyCookbook.pdf`. |
| `make release` | Auto-bump semver version from latest git tag, build all formats, create a git tag, and publish a GitHub release with artifacts. |
| `make check` | Validate all RecipeMD files and check horizontal-rule formatting. |
| `make stats` | Show cookbook statistics (recipe count, word count, PDF pages, git info). |
| `make clean` | Remove the `build/` directory. |

### Versioning

Versions follow [semver](https://semver.org/). The current version is set in `VERSION` in the `Makefile`, or derived from git tags when running `make release`. The version appears on:

- The **cover page**: generated at build time from `scripts/generate-cover.tex`, showing the version and build date (e.g. `3.0.0 — 2026-06-09`)
- The **title page**: in the metadata line below the title

```
make release           # auto-bump patch → v3.0.0, build, tag, release
make release VERSION=4.0.0  # explicit version override
```

### Cross-References

Recipes can use `\label{name}` (on its own line, typically after the attribution) and `\pageref{name}` in the text to create cross-references. For example:

```markdown
\label{biga}

See the [Biga starter](./Biga.md) recipe for details (see page \pageref{biga}).
```

- **PDF**: rendered as native LaTeX cross-references (correct page numbers after multiple passes)
- **EPUB/HTML**: `\pageref` text is stripped; links to other recipe files are rewritten as HTML anchors. A post-processing step (`scripts/fix-epub-links.py`) resolves cross-chapter fragment links in EPUB output.

### Cover Page

The cover is generated fresh on every `make final` or `make release` build:

1. The cover image is extracted from `Coverpage.pdf` (exported from `Coverpage.sla` in Scribus)
2. A LaTeX template (`scripts/generate-cover.tex`) renders the image with the centered version + build date overlay
3. `pdfunite` assembles cover + content + `GroceryList.pdf` into the final PDF

To update the cover design, edit `Coverpage.sla` in Scribus and re-export to `Coverpage.pdf`.

### Proofreading

Several make targets help catch common RecipeMD errors:

| Target | Description |
|--------|-------------|
| `make check` | Full RecipeMD validation + HR formatting check |
| `make find-missing-units` | Find ingredient quantities missing units (e.g. `1*` instead of `*1 T*`) |
| `make find-repeated-words` | Find duplicate words (e.g. `the the`) |
| `make find-missing-attribution` | List recipes with tags but no `Source:` line |
| `make check-hr-formatting` | Verify blank lines around horizontal rules |
| `make find-adjective-titles` | Find titles starting with an adjective (alphabetization check) |
| `make proofread` | Run all proofreading checks at once |

## Handy Proofreading tips

For most proofreading tasks, use `make proofread` to run all checks at once, or
refer to the individual targets in the table above. Some raw command alternatives:

* `ack "[1-9]\*"` — find ingredient quantities missing units (alias for `make find-missing-units`)
* `ack --ignore-file ext:css "\b([a-zA-Z]+'?[a-zA-Z]+)\s+\1\b"` — find repeated words like `the the`
* `grep -Pzl '(?s)^#[^\n]*\n\n\*.*\*' recipes/*.md` — list recipes missing `Source:` lines
* `grep -Pzol '(?s)(?<!\n)\n---\n(?!.*---\n)' recipes/*.md` — find HRs without blank lines around them
