# Rodman/Pottinger Cookbook Project

This is a collection of recipes we use on a regular basis, and will hopefully be
used to produce a family cookbook, if I keep my act together this year.
TLDR, if you're just here for recipes, you can find them in the [recipes](./recipes/) folder.


## Software/Specs Used

* [RecipeMD](https://recipemd.org/): for the excellent markdown recipe format, and a few nice [tools](https://recipemd.org/recommended_tools.html).
* [Cookie](https://github.com/bbugyi200/cookie): for quickly creating a new recipe
* [Pandoc](https://pandoc.org/): for converting recipes into PDF files
* [poppler-utilsa](https://packages.debian.org/sid/poppler-utils): for it's
handy pdf-unite tool, so I can slap the coverpage on the final PDF of the
cookbook.
* [Scribus](https://www.scribus.net/): for general typesetting of book pages
* [Wikiti Pandoc Book Template](https://github.com/wikiti/pandoc-book-template)

## How to Use

The Makefile is from the [Wikiti Pandoc Book Template](https://github.com/wikiti/pandoc-book-template),
the docs there are good, but, here's a terse bit of suggestions:

`make pdf` will generate the basic cookbook.pdf file, and this is the easiest to
navigate because the page count matches the page numbers, so jumping to the
correct page from the TOC is pretty straightforward, and doesn't involve any
math.

`make final` assembles the entire cookbook, including the coverpage, into a
single PDF file, suitable for printing.

I haven't yet tried any of the other targets in the Makefile.

Eventually there will be a `make release` which will tag a new release on
GitHub, and upload the final version of the cookbook, for a new edition. But,
that work remains to be done.

## Handy Proofreading tips

`ack "[1-9]\*"` is a good way to find a common  typo in a recipe, it's easy to
forget to include the units inside the `*1 T *` markup for quantity of
ingredients... That [ack](https://beyondgrep.com/) search will find those 
mistakes, so you can fix them.
