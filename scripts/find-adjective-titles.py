#!/usr/bin/env python3
"""Find recipe filenames starting with an adjective that may hide them alphabetically."""
import os
import re
import sys

ADJECTIVES = {
    "sweet", "spicy", "creamy", "crispy", "crunchy", "chewy",
    "roasted", "baked", "fried", "grilled", "smoked",
    "fermented",
    "simple", "easy", "quick", "fast", "basic",
    "warm", "cold", "hot", "chilled",
    "plain",
    "overnight",
    "flaky", "tender",
    "rich", "thick", "chunky", "smooth",
    "savory", "tangy", "zesty",
    "slow",        # slow cooker
    "stir",        # stir fried
    "old",
    "not",
    "fantastic",
    "festive", "spirited",
    "comfortable", "edible",
    "classic", "organic",
    "scrambled",
    "cheesy", "buttery", "juicy",
    "gluten",     # gluten free
    "vegan",
    "vegetarian",
    "homemade",
}

SKIP_FIRST = {
    "gluten",     # gluten free
    "vegan",
    "vegetarian",
}

KNOWN_COMPOUNDS = {
    "sweet potato", "black bean", "brown rice", "red onion", "green onion",
    "dark chocolate", "white bean", "yellow onion", "red pepper", "green pepper",
    "slow cooker", "instant pot", "rice cooker",
    "field roast", "soy curl",
    "red wine", "white wine",
    "green chili", "red chili",
    "brown sugar", "powdered sugar",
    "soy sauce", "fish sauce", "worcestershire sauce",
    "olive oil", "sesame oil", "coconut oil",
    "baking soda", "baking powder",
    "brown lentil", "red lentil", "green lentil",
    "brussels sprout",
}

SKIP_WORDS = {"and", "or", "with", "the", "a", "an", "of"}  # conjunctions to skip when suggesting

NOUN_LOOKING = {
    "pot", "field", "rice", "bean", "bread", "onion", "pepper",
    "chocolate", "cake", "egg", "cheese", "cream",
    "potato", "carrot", "celery", "garlic", "ginger",
    "chicken", "beef", "pork", "tofu", "tempeh", "seitan",
    "water", "broth", "stock", "sauce", "oil", "butter",
    "sugar", "salt", "pepper", "flour", "corn",
    "lemon", "lime", "apple", "banana", "berry",
    "cheese", "yogurt", "milk", "cream",
    "noodle", "pasta", "rice", "bread", "tortilla",
    "soup", "salad", "stew", "curry", "chili",
    "cookie", "cake", "pie", "brownie", "muffin",
    "sauce", "dressing", "gravy", "salsa", "pesto",
    "breakfast", "lunch", "dinner",
}

ADJ_SUFFIXES = ("ic", "al", "ous", "ful", "less", "ish", "like", "some")

NOT_ADJECTIVES = {
    "garlic", "broccoli", "cilantro",
    "curry", "gravy", "chili", "chilli", "miso",
    "sushi", "soy", "pho", "naan",
    "tofu", "tempeh", "seitan",
    "stock", "broth", "sauce", "juice",
    "guacamole", "hummus",
    "udon", "soba", "ramen",
    "salsa", "pasta", "pizza", "taco", "queso",
    "vegetable",
    "five", "six", "seven", "eight", "nine", "ten",
    "personal",
    "pickled",
    "steamed",
    "brat", "loaf",
    "oatmeal", "cornmeal", "cornbread",
}

ED_NOUNS = {
    "bread", "seed", "noodle", "rice", "sauce",
    "tofu", "tempeh", "seitan",
    "red", "green", "blue", "white", "black", "brown", "gold",
}

ING_NOUNS = {
    "spring", "morning", "evening", "topping", "stuffing",
    "pudding", "dressing",
}

CUISINES = {
    "spanish", "english", "irish", "dutch", "french", "polish",
    "japanese", "chinese", "korean", "vietnamese", "taiwanese",
    "indonesian", "italian", "indian", "mexican", "ethiopian",
    "thai", "greek", "turkish", "lebanese", "swedish", "swiss",
}

POSSESSIVE_NAMES = {
    "liams", "hersheys",
}


def split_filename(name):
    """Split CamelCase filename into lowercase words."""
    name = name.replace(".md", "")
    s = re.sub(r"(?<=[a-z])(?=[A-Z])", " ", name)
    s = re.sub(r"(?<=[A-Z])(?=[A-Z][a-z])", " ", s)
    s = re.sub(r"[-_]", " ", s)
    return s.lower().split()


def is_adjective(word):
    """Check if a word is likely an adjective."""
    if word in ADJECTIVES:
        return True
    if word in NOT_ADJECTIVES:
        return False
    if word in CUISINES:
        return False
    if word in POSSESSIVE_NAMES:
        return False
    if word in ED_NOUNS or word in ING_NOUNS:
        return False
    if word.endswith(ADJ_SUFFIXES):
        return True
    if word.endswith("ed") and word not in ED_NOUNS:
        return True
    if word.endswith("ing") and word not in ING_NOUNS:
        return True
    if word in {"fresh", "soft", "hard", "firm", "cool", "light", "dark"}:
        return True
    return False


def check_filename(path):
    """Check if filename starts with an adjective. Returns (first_adj, suggestion) or None."""
    base = os.path.basename(path)
    words = split_filename(base)
    if not words:
        return None

    first = words[0]
    second = words[1] if len(words) > 1 else ""
    first_two = f"{first} {second}"

    # Skip dietary labels
    if first in SKIP_FIRST:
        return None

    # Skip known compound ingredients
    if first_two in KNOWN_COMPOUNDS:
        return None

    # Skip possessive names
    if first in POSSESSIVE_NAMES:
        return None

    # Remove leading adjectives to suggest a better filename
    rest = words[:]
    adjs = []
    while rest and (is_adjective(rest[0]) or rest[0] in SKIP_WORDS):
        next_two = f"{rest[0]} {rest[1]}" if len(rest) > 1 else ""
        if next_two in KNOWN_COMPOUNDS:
            break
        adjs.append(rest.pop(0))

    if adjs:
        adj_str = " ".join(adjs)
        suggested = "".join(w.capitalize() for w in rest) if rest else ""
        if suggested:
            return (first, f"  {base} starts with adjective \"{adj_str}\" → consider {suggested}.md")
        else:
            return (first, f"  {base} starts with adjective \"{adj_str}\" (no obvious main word)")

    return None


def main():
    found = False
    for path in sorted(sys.argv[1:]):
        if not path.endswith(".md"):
            continue
        result = check_filename(path)
        if result:
            print(result[1])
            found = True
    if not found:
        print("  OK")
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main())
