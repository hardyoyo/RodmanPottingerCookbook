# TODO

## Add labels to all recipes

- [x] All 105 recipes now have a `\label{...}` at the end enabling cross-references.

## Fix non-standard measurements in recipes

### Missing space between quantity and unit
- `recipes/PestoSauce.md`
  - Line 12: `*2T*` → `*2 T*`
  - Line 13: `*2T*` → `*2 T*`
  - Line 14: `*2T*` → `*2 T*`
- `recipes/BBQJackfruitSandwiches.md`
  - Line 13: `*1t*` → `*1 t*`

### Non-standard capitalization
- `recipes/PotatoSalad.md` — Line 11: `*2 Lb*` → `*2 lb*`
- `recipes/PotatoTofuCasserole.md` — Line 14: `*1 Lb*` → `*1 lb*`
- `recipes/SweetPotatoAndBlackBeanQuesadilla.md` — Line 15: `*1 Can*` → `*1 can*`

### Odd formatting in ingredient lines
- `recipes/ChocolateMintTruffleCookies.md` — Line 21: missing closing `*` after `*1/2 C`
- `recipes/Waffles.md` — Line 11: `--` instead of `-`
- `recipes/Waffles.md` — Line 16: missing leading `- `
- `recipes/PotatoSalad.md` — Line 12: `dash of salt` not formatted as ingredient
- `recipes/SweetPotatoAndBlackBeanQuesadilla.md` — Line 19: `=` instead of `-`
- `recipes/LentilSoup.md` — Line 16: `*2 C / 1*` slash notation
- `recipes/PumpkinPieWithPecanOatCrust.md` — Line 16: `*1/2 + 1/3 C*` math in measurement
- `recipes/Seitan.md` — Line 18: `*0.75 C*` decimal instead of fraction
- `recipes/DropBiscuits.md` — Line 14: shout instruction inside italics

### Prose with no-space measurements (lower priority)
- `recipes/SpicyLentils.md` — Line 16: `2T chunks`
- `recipes/PizzaDoughGF.md` — Line 19: `2C`
- `recipes/SweetPotatoAndBlackBeanEmpanadas.md` — Line 13: `1T`
- `recipes/MiddleEasternLentilSoup.md` — Line 40: `1t`
- `recipes/JapaneseCurry.md` — Lines 44-45: `1T` and `1t`
- `recipes/Japchae.md` — Line 30: `1t`

## CI via GitHub Actions

- [x] Set up a GitHub Actions workflow to validate recipes and build the cookbook on push/PR.

## Improve the index

- [x] Fix misspellings in recipe tags (e.g. "desert" → "dessert")
- [x] Investigate and fix duplicate index entries
- [x] Normalize tag capitalization in original recipes
- [x] Add ingredient labels (tofu, tempeh, seitan, jackfruit, soy-curls) to recipes so they appear in the index under major ingredient headings
- [x] Ensure cuisine tags are consistently applied across all recipes
- [x] Add "Instant Pot" tag to recipes that use the Instant Pot but are missing it (0 were missing)

- [x] Fix index page headers — redefine `\fancypagestyle{plain}` before `\printindex` to clear headers, then re-apply.

## Release target

- [ ] Add a `release` target to the Makefile that cuts a new release of the cookbook with compiled PDFs uploaded as artifacts on the release page.
