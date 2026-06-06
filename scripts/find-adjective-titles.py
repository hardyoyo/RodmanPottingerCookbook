#!/usr/bin/env python3
"""Find recipe titles starting with an adjective that may hide them alphabetically."""
import re
import sys

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
}

SKIP_FIRST = {
    "gluten-free", "gluten free", "vegan", "vegetarian",
}

KNOWN_COMPOUNDS = {
    "sweet potato", "black bean", "brown rice", "red onion", "green onion",
    "dark chocolate", "white bean", "yellow onion", "red pepper", "green pepper",
}

def title_from_file(path):
    with open(path) as f:
        for line in f:
            if line.startswith("# "):
                return line[2:].strip()
    return None

def check_title(title):
    lower = title.lower()
    first_word = lower.split()[0] if lower.split() else ""
    first_two = " ".join(lower.split()[:2]) if len(lower.split()) >= 2 else ""

    if first_word in SKIP_FIRST:
        return None

    if first_two in KNOWN_COMPOUNDS:
        return None

    if first_two in ADJECTIVES:
        return first_two

    if first_word in ADJECTIVES:
        return first_word

    return None

def main():
    found = False
    for path in sorted(sys.argv[1:]):
        title = title_from_file(path)
        if title is None:
            continue
        adj = check_title(title)
        if adj:
            print(f'  "{title}" starts with "{adj.capitalize()}"')
            found = True
    if not found:
        print("  OK")
    return 1 if found else 0

if __name__ == "__main__":
    sys.exit(main())
