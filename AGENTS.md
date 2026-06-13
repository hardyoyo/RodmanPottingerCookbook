# Cookbook Project

## Overview
Family cookbook by Hardy Pottinger + Debbie Rodman. Recipes in `recipes/` as Markdown files (RecipeMD format). Builds a printable PDF cookbook via Pandoc.

## RecipeMD Conventions
- **Title**: `# Title` (level-1 heading)
- **Tags**: `*tag1, tag2, ...*` on the line after the title
- **Servings**: `**N Servings**` in bold
- **Separator**: `---`
- **Ingredients**: `- *Qty* ingredient name` (quantity in italics)
- **Separator**: `---`
- **Instructions**: Prose paragraphs
- **Attribution**: `Source: <url>` near the bottom
- **Label**: `\label{label-name}` as the last line

## Build Commands
- `make pdf` — basic PDF cookbook
- `make epub` — EPUB ebook
- `make html` — HTML version
- `make docx` — Word document
- `make final` — full PDF with cover page and grocery list
- `make clean` — clean build directory

## New Recipes
Create a new `.md` file in `recipes/` following RecipeMD conventions above. If adapting from a web source, include a `Source:` line.

## Validation
Run `make check` to validate all RecipeMD recipes using `recipemd --title`.

## Tools
Uses pandoc, xelatex, devbox, recipemd, cookie, scribus.

## Release Policy
- **Do NOT run `make release`** — it is interactive (prompts for version strategy and confirmation). Not agent-safe.
- **Do NOT simulate a release** by manually running git tag, push, or gh release create commands. The release process is user-driven, not agent-driven.
- If the user wants to release, explain the interactive flow and hand it off — do not execute any part of it.
