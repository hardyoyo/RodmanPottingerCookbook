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
}

KEEP_PATTERNS = [
    'Chile Garlic Sauce', 'Sriracha', 'Tamari', 'Dijon Mustard',
    'Balsamic Vinegar', 'Arborio Rice', 'Coconut Milk', 'Cayenne Pepper',
    'Smoked Paprika', 'Baking Powder', 'Baking Soda', 'Chili Powder',
    'Chilli Powder', 'Onion Powder', 'Garlic Powder', 'Roasted Garlic Powder',
    'Brown Sugar', 'Liquid Smoke', 'Soy Milk', 'Bread Flour',
    'Gluten-Free', 'Gluten Free', 'All-purpose Flour', 'Wheat Flour',
    'Rice Wine Vinegar', 'Apple Cider Vinegar', 'Red Wine Vinegar',
    'GF Dark Soy Sauce', 'GF Oyster Sauce', 'Oyster Sauce', 'Soy Sauce',
    'Parmesan Cheese', 'Goat Cheese', 'Vegan Butter', 'Black Beans',
    'Flax Seeds', 'Sesame Seeds', 'Nutritional Yeast', 'Better Than Bouillon',
    'Pasta Sauce', 'Orange Juice', 'Lemon Juice', 'Lime Juice',
    'Sesame Oil', 'Toasted Sesame Oil', 'Olive Oil', 'Canola Oil',
    'Vegetable Oil', 'Neutral Oil', 'Avocado Oil', 'Black Pepper',
    'Cayenne Pepper', 'Ground Cumin', 'Ground Turmeric', 'Ground Cinnamon',
    'Ground Ginger', 'Ground Cloves', 'Ground Cardamom', 'Tomato Paste',
    'Worcestershire Sauce', 'Sambal Oelek', 'Classico Tomato',
    "Hershey's Cocoa", "Bob's Red Mill", 'Ritz Crackers', 'Beyond Meat',
    'Beyond Italian Sausage', 'Monterey Jack Cheese', 'Cream Cheese',
    'Sour Cream', 'Biga', 'Miso',
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
            m = re.match(r'(-\s+\*[^*]+\*\s+)(.+)', stripped)
            if m:
                prefix = m.group(1)
                name = m.group(2)
                leading = line[:len(line.rstrip('\n')) - len(stripped)]

                if not should_keep_as_is(name):
                    new_name = lowercase_generic_words(name)
                    if new_name != name:
                        modified = True
                        if not check_only:
                            line = leading + prefix + new_name + '\n'
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
