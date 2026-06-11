"""Normalize ingredient capitalization — lowercase generic ingredient words
in ingredient lists while preserving proper nouns and brand names."""

import os
import glob
import re
import sys


ALWAYS_LOWER = {
    'Salt', 'Sugar', 'Oil', 'Flour', 'Pepper', 'Water', 'Milk', 'Rice',
    'Butter', 'Garlic', 'Onion', 'Cheese', 'Eggs', 'Noodles', 'Tofu',
    'Vanilla', 'Cinnamon', 'Paprika', 'Basil', 'Oregano', 'Thyme',
    'Cumin', 'Seeds', 'Beans', 'Broth', 'Stock', 'Cream', 'Juice',
    'Mustard', 'Vinegar', 'Ketchup', 'Oregano',
    'Mushroom', 'Powder', 'Chile', 'Pepper', 'Yeast',
    'Nutritional', 'Roasted', 'Black', 'White', 'Brown',
    'Apple', 'Cider', 'Balsamic', 'Red', 'Wine',
    'Chili', 'Chilli', 'Chipotle', 'Ancho',
    'Soy', 'Sauce', 'Sesame', 'Flax', 'Coconut', 'Olive',
    'Canola', 'Vegetable', 'Avocado', 'Toasted', 'Neutral',
    'Pasta', 'Orange', 'Lemon', 'Lime', 'Parmesan',
    'Goat', 'Vegan', 'Bread', 'Wheat', 'Baking', 'Soda',
    'Whole', 'Oyster', 'All-purpose', 'All purpose',
    'Cayenne', 'Curry',
}

KEEP_PATTERNS = [
    # Brands / proper nouns
    "Bob's Red Mill", 'Better Than Bouillon', "Hershey's Cocoa",
    'Ritz Crackers', 'Beyond Meat', 'Beyond Italian Sausage',
    'Classico Tomato', 'Sambal Oelek', 'Worcestershire Sauce',
    'Monterey Jack Cheese', 'Liquid Smoke',
    # Specific products / names
    'Chile Garlic Sauce', 'Sriracha', 'Tamari', 'Dijon Mustard',
    'Arborio Rice', 'Smoked Paprika', 'Biga', 'Miso',
    'GF Dark Soy Sauce', 'GF Oyster Sauce',
    # Multi-word terms needing individual-word preservation
    'Hatch Chile Powder', 'Ground Cumin', 'Ground Turmeric',
    'Ground Cinnamon', 'Ground Ginger', 'Ground Cloves', 'Ground Cardamom',
    'Bread Flour',
]


def should_keep_as_is(name):
    lowered = name.lower()
    for p in KEEP_PATTERNS:
        if p.lower() in lowered:
            return True
    return False


def lowercase_generic_words(name):
    words = name.split()
    new_words = []
    for w in words:
        clean = w.strip('.,;:()"\'')
        if clean in ALWAYS_LOWER:
            new_words.append(w.lower())
        else:
            new_words.append(w)
    return ' '.join(new_words)


def process_file(fpath, check_only=False):
    with open(fpath) as f:
        lines = f.readlines()

    fname = os.path.basename(fpath)
    sep_count = 0
    modified = False
    new_lines = []

    for line in lines:
        stripped = line.strip()
        if stripped == '---':
            sep_count += 1
            new_lines.append(line)
            continue
        if sep_count == 1:
            m = re.match(r'(-{1,2}\s*\*[^*]+\*\s+)(.+)', stripped)
            if m:
                prefix = m.group(1)
                name = m.group(2)
                leading = line[:len(line.rstrip()) - len(stripped)]

                # Normalize prefix: single dash + single space
                new_prefix = re.sub(r'^-{1,2}\s*', '- ', prefix)
                prefix_changed = new_prefix != prefix

                if not should_keep_as_is(name):
                    new_name = lowercase_generic_words(name)
                    if new_name != name or prefix_changed:
                        modified = True
                        if not check_only:
                            line = leading + new_prefix + new_name + '\n'
                elif prefix_changed:
                    modified = True
                    if not check_only:
                        line = leading + new_prefix + name + '\n'
        new_lines.append(line)

    if modified and not check_only:
        with open(fpath, 'w') as f:
            f.writelines(new_lines)
    return modified


def main():
    check_only = '--check' in sys.argv
    recipes_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                               'recipes')
    changed = []

    for fpath in sorted(glob.glob(os.path.join(recipes_dir, "*.md"))):
        if process_file(fpath, check_only):
            changed.append(os.path.basename(fpath))

    if changed:
        print(f"{'Would modify' if check_only else 'Modified'} "
              f"{len(changed)} files:")
        for f in changed:
            print(f"  {f}")
        if check_only:
            sys.exit(1)
    else:
        print("All ingredient capitalization already normalized.")


if __name__ == '__main__':
    main()
