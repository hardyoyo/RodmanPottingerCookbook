######################################################################
# Configuration
######################################################################

.DEFAULT_GOAL := help

# Improve Error Handling
.ONESHELL:
ifdef DEBUG
.SHELLFLAGS := -eux -o pipefail -c
else
.SHELLFLAGS := -eu -o pipefail -c
endif

# catch errors in pipe chains
SHELL := /bin/bash

# Build configuration

BUILD = build
MAKEFILE = Makefile
OUTPUT_FILENAME = cookbook
FINAL_FILENAME = RodmanPottingerFamilyCookbook
METADATA = metadata.yml
TMP_METADATA = $(BUILD)/tmp-metadata.yml
TOC = --toc --toc-depth 2
METADATA_ARGS = --metadata-file $(METADATA) --metadata-file $(TMP_METADATA)
IMAGES = $(shell find images -type f)
TEMPLATES = $(shell find templates/ -type f)
INCLUDES = $(shell find includes/ -type f)
COVER_IMAGE = images/cover.png
MATH_FORMULAS =

# Detected Operating System

OS = $(shell sh -c 'uname -s 2>/dev/null || echo Unknown')

# OS specific commands

ifeq ($(OS),Darwin)
	COPY_CMD = cp -P
else
	COPY_CMD = cp --parent
endif

MKDIR_CMD = mkdir -p
RMDIR_CMD = rm -r
ECHO_BUILDING = @echo "building $@..."
ECHO_BUILT = @echo "$@ was built"

## START WITH ALL THE RECIPES, THEN THE WORDS
PAGES = recipes/*.md
PAGES += $(addprefix ./words/,\
  MidnightSnacks.md\
  MealPlans.md\
  InstantPotVsRiceCooker.md\
  Glossary.md\
  Tools.md\
  RoastedVegetables.md\
  InstantPotCheatSheet.md\
  EmergencySubstitutions.md\
  Acknowledgements.md\
)

# Recipe content
#  - ensure there is a pagebreak at the end of every recipe
CONTENT = awk 'FNR==1 && NR!=1 {print "\n\\pagebreak\n\n"}{print}' $(PAGES)
CONTENT_FILTERS = tee # can be used with sed to replace content
RECIPEMD = .venv/bin/recipemd

# Debugging

# DEBUG_ARGS = --verbose

# Pandoc filters - uncomment the following variable to enable cross
# references filter. For more information, check the "Cross references"
# section on the README.md file.

# FILTER_ARGS = --filter pandoc-crossref

LUA_FILTER = --lua-filter=scripts/indexer.lua

# Combined arguments

ARGS = $(TOC) $(MATH_FORMULAS) $(METADATA_ARGS) $(FILTER_ARGS) $(DEBUG_ARGS)

PANDOC_COMMAND = pandoc

# Per-format options

DOCX_ARGS = --standalone --reference-doc templates/docx.docx
EPUB_ARGS = --template templates/epub.html --epub-cover-image $(COVER_IMAGE)
HTML_ARGS = --template templates/html.html --standalone --to html5
PDF_ENGINE = xelatex

# Per-format file dependencies

BASE_DEPENDENCIES = $(MAKEFILE) $(PAGES) $(METADATA) $(IMAGES) \
	$(TEMPLATES) $(TMP_METADATA)
DOCX_DEPENDENCIES = $(BASE_DEPENDENCIES)
EPUB_DEPENDENCIES = $(BASE_DEPENDENCIES)
HTML_DEPENDENCIES = $(BASE_DEPENDENCIES)
PDF_DEPENDENCIES = $(BASE_DEPENDENCIES) $(INCLUDES)

######################################################################
# Basic actions
######################################################################

.PHONY: help all book clean epub html pdf docx final check \
	find-missing-units find-repeated-words find-missing-attribution \
	check-hr-formatting find-adjective-titles proofread \
	check-pdf-prereqs stats

help:	## -- Display this help message
	@printf "\033[1m📖 Rodman-Pottinger Family Cookbook — Build System\033[0m\n"
	@printf "\033[1m====================================================\033[0m\n"
	@echo ""
	@printf "\033[1mAvailable targets:\033[0m\n"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*## --' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*## -- "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@printf "\033[1mConfiguration:\033[0m\n"
	@echo ""
	@echo "  PUBLISH_PATH is not set for this project"
	@echo ""

all:	book ## -- Build all formats

book:	epub html pdf docx

clean:	## -- Clean up build directory
	@if [ -d "$(BUILD)" ]; then \
		echo "Removing $(BUILD) directory..."; \
		$(RMDIR_CMD) $(BUILD); \
	else \
		echo "$(BUILD) directory already clean."; \
	fi
	$(MKDIR_CMD) $(BUILD)
	touch $(BUILD)/.gitkeep

check:	## -- Validate all RecipeMD files (includes HR formatting check)
	@failed=0; \
	for f in recipes/*.md; do \
		if ! $(RECIPEMD) --title "$$f" > /dev/null 2>&1; then \
			echo "  FAILED: $$f"; \
			$(RECIPEMD) --title "$$f" 1>&2 2>&1; \
			failed=1; \
		fi; \
	done; \
	\
	hits=$$(awk 'FNR==1{prev=""} /^---$$/ && prev != "" {print FILENAME ":" FNR ": no blank line before ---"} prev ~ /^---$$/ && $$0 != "" {print FILENAME ":" (FNR-1) ": no blank line after ---"} {prev=$$0}' recipes/*.md); \
	if [ -n "$$hits" ]; then \
		echo "$$hits"; \
		failed=1; \
	fi; \
	\
	if [ $$failed -eq 1 ]; then \
		echo ""; \
		echo "Some checks failed!"; \
		exit 1; \
	else \
		echo "All checks passed!"; \
	fi

find-missing-units:	## -- Find possible missing ingredient units (digit before *)
	@hits=$$(grep -n '[1-9]\*' recipes/*.md 2>/dev/null); \
	if [ -n "$$hits" ]; then echo "$$hits"; else echo "  OK"; fi

find-repeated-words:	## -- Find possible repeated words (e.g. "the the")
	@hits=$$(grep -nP '(\b[a-zA-Z]+)\s+\1\b' recipes/*.md 2>/dev/null); \
	if [ -n "$$hits" ]; then echo "$$hits"; else echo "  OK"; fi

find-missing-attribution:	## -- Find recipes with tags but no Source: line
	@cd recipes && missing=0; \
	for f in $$(grep -Pzl '(?s)^#[^\n]*\n\n\*.*\*' *.md 2>/dev/null); do \
		grep -q 'Source:' "$$f" || { echo "MISSING Source: $$f"; missing=1; }; \
	done; \
	if [ $$missing -eq 0 ]; then echo "  OK"; fi

check-hr-formatting:	## -- Check horizontal rules have blank lines around them
	@hits=$$(awk 'FNR==1{prev=""} /^---$$/ && prev != "" {print FILENAME ":" FNR ": no blank line before ---"} prev ~ /^---$$/ && $$0 != "" {print FILENAME ":" (FNR-1) ": no blank line after ---"} {prev=$$0}' recipes/*.md); \
	if [ -n "$$hits" ]; then echo "$$hits"; else echo "  OK"; fi

find-adjective-titles:	## -- Find titles starting with an adjective
	##    (e.g. "Sweet Arepas" under S instead of A)
	@python3 scripts/find-adjective-titles.py recipes/*.md; exit 0

proofread: find-missing-units find-repeated-words find-missing-attribution \
	check-hr-formatting find-adjective-titles ## -- Run all proofreading checks

check-pdf-prereqs: ## -- Check if PDF generation prerequisites are available
	@echo "Checking PDF generation prerequisites..."
	@if ! command -v xelatex >/dev/null 2>&1; then \
		echo ""; \
		echo "❌ xelatex not found!"; \
		echo ""; \
		echo "To fix this:"; \
		echo "  devbox shell (if using devbox)"; \
		echo "  brew install --cask mactex (macOS)"; \
		echo "  sudo apt install texlive-xetex (Debian/Ubuntu)"; \
		echo ""; \
		exit 1; \
	fi
	@echo "✅ xelatex is available"

stats: ## -- Show book statistics
	@echo ""
	@echo "📚 Cookbook Statistics"
	@echo "========================"
	@recipe_count=$$(ls recipes/*.md 2>/dev/null | wc -l); \
	total_words=$$(cat $(PAGES) 2>/dev/null | wc -w); \
	total_lines=$$(cat $(PAGES) 2>/dev/null | wc -l); \
	recipe_words=$$(cat recipes/*.md 2>/dev/null | wc -w); \
	echo "🍳 Recipes: $$recipe_count"; \
	echo ""; \
	echo "📝 Total words: $$total_words"; \
	echo "📏 Total lines: $$total_lines"; \
	echo ""; \
	if [ -f "$(BUILD)/pdf/$(OUTPUT_FILENAME).pdf" ]; then \
		if command -v pdfinfo >/dev/null 2>&1; then \
			pages=$$(pdfinfo "$(BUILD)/pdf/$(OUTPUT_FILENAME).pdf" | grep "Pages:" | awk '{print $$2}'); \
			title=$$(pdfinfo "$(BUILD)/pdf/$(OUTPUT_FILENAME).pdf" | grep "Title:" | cut -d: -f2- | sed 's/^ *//'); \
			echo "📑 PDF pages: $$pages"; \
			echo "📖 PDF title: $$title"; \
		else \
			echo "📑 PDF pages: (install pdfinfo to see PDF metadata)"; \
		fi; \
		git_sha=$$(grep -o "git_sha: [a-f0-9]*" $(TMP_METADATA) 2>/dev/null | cut -d: -f2 | sed 's/^ *//'); \
		git_date=$$(grep -o "git_date: [0-9-]*" $(TMP_METADATA) 2>/dev/null | cut -d: -f2 | sed 's/^ *//'); \
		if [ -n "$$git_sha" ]; then \
			echo "📝 Git commit: $$git_sha"; \
			echo "📅 Git date: $$git_date"; \
		else \
			echo "📝 Git info: (run 'make clean && make pdf' to embed)"; \
		fi; \
	else \
		echo "📑 PDF pages: (run 'make pdf' first)"; \
	fi; \
	echo ""

$(TMP_METADATA):
	$(MKDIR_CMD) $(BUILD)
	echo "git_sha: $(shell git rev-parse --short HEAD)" > $(TMP_METADATA)
	echo "git_url: $(shell git config --get remote.origin.url | \
		sed -E 's#git@([^:]+):#\1/#; s#\.git$$##')" >> $(TMP_METADATA)
	echo "git_date: $(shell git log -1 --format=%cd --date=short)" >> $(TMP_METADATA)

######################################################################
# File builders
######################################################################

epub:	$(BUILD)/epub/$(OUTPUT_FILENAME).epub ## -- Build EPUB file

html:	$(BUILD)/html/$(OUTPUT_FILENAME).html ## -- Build HTML file

pdf:	check-pdf-prereqs $(BUILD)/pdf/$(OUTPUT_FILENAME).pdf ## -- Build PDF file

docx:	$(BUILD)/docx/$(OUTPUT_FILENAME).docx ## -- Build DOCX file

final:  $(BUILD)/pdf/$(FINAL_FILENAME).pdf ## -- Build final PDF file

$(BUILD)/epub/$(OUTPUT_FILENAME).epub:	$(EPUB_DEPENDENCIES)
	$(ECHO_BUILDING)
	$(MKDIR_CMD) $(BUILD)/epub
	$(CONTENT) | $(CONTENT_FILTERS) | $(PANDOC_COMMAND) $(ARGS) $(EPUB_ARGS) -o $@
	$(ECHO_BUILT)

$(BUILD)/html/$(OUTPUT_FILENAME).html:	$(HTML_DEPENDENCIES)
	$(ECHO_BUILDING)
	$(MKDIR_CMD) $(BUILD)/html
	$(CONTENT) | $(CONTENT_FILTERS) | $(PANDOC_COMMAND) $(ARGS) $(HTML_ARGS) -o $@
	$(COPY_CMD) $(IMAGES) $(BUILD)/html/
	$(ECHO_BUILT)

$(BUILD)/pdf/$(OUTPUT_FILENAME).pdf:	$(PDF_DEPENDENCIES)
	$(ECHO_BUILDING)
	$(MKDIR_CMD) $(BUILD)/pdf
	$(CONTENT) | $(CONTENT_FILTERS) | $(PANDOC_COMMAND) $(ARGS) $(LUA_FILTER) \
		--template templates/pdf.latex \
		--include-in-header=includes/table-prefs.tex \
		-o $(BUILD)/pdf/$(OUTPUT_FILENAME).tex
	$(PDF_ENGINE) -output-directory=$(BUILD)/pdf -shell-escape \
		-interaction=nonstopmode $(BUILD)/pdf/$(OUTPUT_FILENAME).tex
	-makeindex $(BUILD)/pdf/$(OUTPUT_FILENAME).idx 2>/dev/null
	$(PDF_ENGINE) -output-directory=$(BUILD)/pdf -shell-escape \
		-interaction=nonstopmode $(BUILD)/pdf/$(OUTPUT_FILENAME).tex
	$(PDF_ENGINE) -output-directory=$(BUILD)/pdf -shell-escape \
		-interaction=nonstopmode $(BUILD)/pdf/$(OUTPUT_FILENAME).tex
	rm -f $(BUILD)/pdf/$(OUTPUT_FILENAME).tex \
		$(BUILD)/pdf/$(OUTPUT_FILENAME).aux \
		$(BUILD)/pdf/$(OUTPUT_FILENAME).idx \
		$(BUILD)/pdf/$(OUTPUT_FILENAME).ilg \
		$(BUILD)/pdf/$(OUTPUT_FILENAME).ind \
		$(BUILD)/pdf/$(OUTPUT_FILENAME).log \
		$(BUILD)/pdf/$(OUTPUT_FILENAME).out \
		$(BUILD)/pdf/$(OUTPUT_FILENAME).toc
	$(ECHO_BUILT)

$(BUILD)/docx/$(OUTPUT_FILENAME).docx:	$(DOCX_DEPENDENCIES)
	$(ECHO_BUILDING)
	$(MKDIR_CMD) $(BUILD)/docx
	$(CONTENT) | $(CONTENT_FILTERS) | $(PANDOC_COMMAND) $(ARGS) $(DOCX_ARGS) -o $@
	$(ECHO_BUILT)

$(BUILD)/pdf/$(FINAL_FILENAME).pdf: $(BUILD)/pdf/$(OUTPUT_FILENAME).pdf
	$(ECHO_BUILDING)
	pdfunite Coverpage.pdf $(BUILD)/pdf/$(OUTPUT_FILENAME).pdf GroceryList.pdf $@
	$(ECHO_BUILT)
