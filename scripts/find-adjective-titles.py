#!/usr/bin/env python3
"""Find recipe titles starting with an adjective that may hide them alphabetically."""
import sys

# ---- Curated list of adjectives commonly used as recipe prefixes ----
ADJECTIVES = {
    "sweet", "spicy", "creamy", "crispy", "crunchy", "chewy",
    "roasted", "baked", "fried", "grilled", "smoked", "steamed",
    "pickled", "fermented",
    "homemade",
    "simple", "easy", "quick", "fast", "basic",
    "warm", "cold", "hot", "chilled",
    "plain",
    "personal",
    "overnight",
    "flaky", "tender",
    "rich", "thick", "chunky", "smooth",
    "savory", "tangy", "zesty",
    "stir-fried", "stir fried",
    "slow-cooker", "slow cooker",
    "old-fashioned",
    "steamed or boiled",
    "not",
    "fantastic",
    "quick-soaked",
    "festive", "spirited",
    "comfortable", "edible",
    "classic", "organic",
}

SKIP_FIRST = {
    "gluten-free", "gluten free", "vegan", "vegetarian",
}

KNOWN_COMPOUNDS = {
    "sweet potato", "black bean", "brown rice", "red onion", "green onion",
    "dark chocolate", "white bean", "yellow onion", "red pepper", "green pepper",
}

# ---- Rule-based adjective detection (catches novel adjectives) ----

# Common English adjective suffixes
ADJ_SUFFIXES = ("ic", "al", "ous", "ful", "less", "ish", "like", "some")

# Past/present participle suffixes
PARTICIPLE_SUFFIXES = ("ed", "ing")

# Words that match ADJ_SUFFIXES but are NOT adjectives
NOT_ADJECTIVES = {
    "garlic", "broccoli", "cilantro",
    "curry", "gravy", "chili", "chilli", "miso",
    "sushi", "soy", "pho", "naan",
    "tofu", "tempeh", "seitan",
    "stock", "broth", "sauce", "juice",
    "guacamole",
    "udon", "soba", "ramen",
    "salsa", "pasta", "pizza", "taco", "queso",
    "vegetable",
    "five", "six", "seven", "eight", "nine", "ten",
}

# Past-participle looking words that are nouns (not adjectives)
ED_NOUNS = {
    "bread", "seed", "noodle", "rice", "sauce",
    "tofu", "tempeh", "seitan",
}

# Ing-looking words that are nouns (not adjectives)
ING_NOUNS = {
    "spring", "morning", "evening", "topping", "stuffing",
    "pudding", "dressing",
}

# Cuisine/language-origin words (not filing-adjectives)
CUISINES = {
    "spanish", "english", "irish", "dutch", "french", "polish",
    "japanese", "chinese", "korean", "vietnamese", "taiwanese",
    "indonesian", "italian", "indian", "mexican", "ethiopian",
    "thai", "greek", "turkish", "lebanese", "swedish", "swiss",
}


def _is_adj_suffix(word):
    """Check if word looks like an adjective by its suffix."""
    w = word.lower().replace("-", " ").replace("_", " ")
    # Check multi-word compounds like "stir fried"
    parts = w.split()
    first = parts[0]

    if first in CUISINES:
        return False
    if first in NOT_ADJECTIVES:
        return False

    if first.endswith(ADJ_SUFFIXES):
        return True
    if first.endswith("ed") and first not in ED_NOUNS:
        return True
    if first.endswith("ing") and first not in ING_NOUNS:
        return True
    # Short common adjectives that don't fit suffixes
    if first in {"fresh", "soft", "hard", "firm", "cool", "light", "dark"}:
        return True
    return False


def check_title(title):
    lower = title.lower()
    words = lower.split()
    if not words:
        return None
    first_word = words[0]
    first_two = " ".join(words[:2])

    if first_word in SKIP_FIRST:
        return None
    if first_two in KNOWN_COMPOUNDS:
        return None

    # Check curated list first (including multi-word)
    if first_two in ADJECTIVES:
        return first_two.capitalize()
    if first_word in ADJECTIVES:
        return first_word.capitalize()

    # Fall back to suffix heuristics
    adj = _is_adj_suffix(first_word)
    if adj:
        return first_word.capitalize()

    return None


def title_from_file(path):
    with open(path) as f:
        for line in f:
            if line.startswith("# "):
                return line[2:].strip()
    return None


def main():
    found = False
    for path in sorted(sys.argv[1:]):
        title = title_from_file(path)
        if title is None:
            continue
        adj = check_title(title)
        if adj:
            print(f'  "{title}" starts with adjective "{adj}"')
            found = True
    if not found:
        print("  OK")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
