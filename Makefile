####################################################################################################
# Configuration
####################################################################################################

# Build configuration

BUILD = build
MAKEFILE = Makefile
OUTPUT_FILENAME = cookbook
FINAL_FILENAME = RodmanPottingerFamilyCookbook
METADATA = metadata.yml
TOC = --toc --toc-depth 2
METADATA_ARGS = --metadata-file $(METADATA)
IMAGES = $(shell find images -type f)
TEMPLATES = $(shell find templates/ -type f)
INCLUDES = $(shell find includes/ -type f)
COVER_IMAGE = images/cover.png
MATH_FORMULAS = 

## START WITH ALL THE RECIPES, THEN THE WORDS
PAGES = recipes/*.md
PAGES += $(addprefix ./words/,\
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
CONTENT = awk 'FNR==1 && NR!=1 {print "\n\pagebreak\n\n"}{print}' $(PAGES)
CONTENT_FILTERS = tee # can be used with sed to replace content

# Debugging

# DEBUG_ARGS = --verbose

# Pandoc filters - uncomment the following variable to enable cross references filter. For more
# information, check the "Cross references" section on the README.md file.

# FILTER_ARGS = --filter pandoc-crossref

# Combined arguments

ARGS = $(TOC) $(MATH_FORMULAS) $(METADATA_ARGS) $(FILTER_ARGS) $(DEBUG_ARGS)

PANDOC_COMMAND = pandoc

# Per-format options

DOCX_ARGS = --standalone --reference-doc templates/docx.docx
EPUB_ARGS = --template templates/epub.html --epub-cover-image $(COVER_IMAGE)
HTML_ARGS = --template templates/html.html --standalone --to html5
PDF_ARGS = --template templates/pdf.latex --pdf-engine xelatex --include-in-header=includes/table-prefs.tex

# Per-format file dependencies

BASE_DEPENDENCIES = $(MAKEFILE) $(PAGES) $(METADATA) $(IMAGES) $(TEMPLATES)
DOCX_DEPENDENCIES = $(BASE_DEPENDENCIES)
EPUB_DEPENDENCIES = $(BASE_DEPENDENCIES)
HTML_DEPENDENCIES = $(BASE_DEPENDENCIES)
PDF_DEPENDENCIES = $(BASE_DEPENDENCIES) $(INCLUDES)

####################################################################################################
# Basic actions
####################################################################################################

.PHONY: all
all:	book

.PHONY: book
book:	epub html pdf docx

.PHONY: clean
clean:
	rm -r $(BUILD)
	mkdir ${BUILD}
	touch ${BUILD}/.gitkeep

####################################################################################################
# File builders
####################################################################################################

.PHONY: epub
epub:	$(BUILD)/epub/$(OUTPUT_FILENAME).epub

.PHONY: html
html:	$(BUILD)/html/$(OUTPUT_FILENAME).html

.PHONY: pdf
pdf:	$(BUILD)/pdf/$(OUTPUT_FILENAME).pdf

.PHONY: docx
docx:	$(BUILD)/docx/$(OUTPUT_FILENAME).docx

.PHONY: final
final:  $(BUILD)/pdf/$(FINAL_FILENAME).pdf

$(BUILD)/epub/$(OUTPUT_FILENAME).epub:	$(EPUB_DEPENDENCIES)
	mkdir -p $(BUILD)/epub
	$(CONTENT) | $(CONTENT_FILTERS) | $(PANDOC_COMMAND) $(ARGS) $(EPUB_ARGS) -o $@
	@echo "$@ was built"

$(BUILD)/html/$(OUTPUT_FILENAME).html:	$(HTML_DEPENDENCIES)
	mkdir -p $(BUILD)/html
	$(CONTENT) | $(CONTENT_FILTERS) | $(PANDOC_COMMAND) $(ARGS) $(HTML_ARGS) -o $@
	cp --parent $(IMAGES) $(BUILD)/html/
	@echo "$@ was built"

$(BUILD)/pdf/$(OUTPUT_FILENAME).pdf:	$(PDF_DEPENDENCIES)
	mkdir -p $(BUILD)/pdf
	$(CONTENT) | $(CONTENT_FILTERS) | $(PANDOC_COMMAND) $(ARGS) $(PDF_ARGS) -o $@
	@echo "$@ was built"

$(BUILD)/docx/$(OUTPUT_FILENAME).docx:	$(DOCX_DEPENDENCIES)
	mkdir -p $(BUILD)/docx
	$(CONTENT) | $(CONTENT_FILTERS) | $(PANDOC_COMMAND) $(ARGS) $(DOCX_ARGS) -o $@
	@echo "$@ was built"

$(BUILD)/pdf/$(FINAL_FILENAME).pdf: $(BUILD)/pdf/$(OUTPUT_FILENAME).pdf
	pdfunite Coverpage.pdf $(BUILD)/pdf/$(OUTPUT_FILENAME).pdf GroceryList.pdf $@
	@echo "$@ was built"
