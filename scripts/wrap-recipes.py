"""Wrap prose paragraphs in RecipeMD files to 70 characters.

Only prose paragraphs (instruction text) are wrapped. Structural elements
like headings, tag lines, serving sizes, separators, ingredient list
items, and labels are left untouched.
"""

import textwrap
import glob
import os
import sys


RECIPES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'recipes')
WRAP_WIDTH = 70


def is_structural(stripped):
    """Return True if line is a markdown structure element, not prose."""
    if not stripped:
        return True
    if stripped.startswith('#'):
        return True
    if stripped == '---':
        return True
    if stripped.startswith('- '):
        return True
    if stripped.startswith('\\label'):
        return True
    # Tag line: standalone *text*
    if (stripped.startswith('*') and stripped.endswith('*')
            and not stripped.startswith('**')
            and stripped.count('*') == 2):
        return True
    # Servings / metadata line: **text**
    if stripped.startswith('**') and stripped.endswith('**'):
        return True
    return False


def process_file(fpath, width=WRAP_WIDTH, check_only=False):
    with open(fpath) as f:
        original = f.read()

    trailing_newline = original.endswith('\n')
    content = original[:-1] if trailing_newline else original

    lines = content.split('\n')
    new_lines = []
    para = []

    def flush_para():
        if not para:
            return None
        joined = ' '.join(p.strip() for p in para)
        joined = ' '.join(joined.split())
        para.clear()
        return textwrap.fill(joined, width=width)

    for line in lines:
        stripped = line.strip()
        if is_structural(stripped):
            flushed = flush_para()
            if flushed:
                new_lines.append(flushed)
            new_lines.append(line)
        else:
            para.append(line)

    flushed = flush_para()
    if flushed:
        new_lines.append(flushed)

    result = '\n'.join(new_lines)
    if trailing_newline:
        result += '\n'

    if result != original:
        if not check_only:
            with open(fpath, 'w') as f:
                f.write(result)
            print(f"  wrapped: {os.path.basename(fpath)}")
        return True
    return False


def main():
    check_only = '--check' in sys.argv
    changed = 0

    for fpath in sorted(glob.glob(os.path.join(RECIPES_DIR, "*.md"))):
        if process_file(fpath, check_only=check_only):
            changed += 1

    if changed:
        label = "Would wrap" if check_only else "Wrapped"
        print(f"{label} {changed} file(s)")
        if check_only:
            sys.exit(1)
    else:
        print("All recipes already wrapped at 70 characters.")


if __name__ == '__main__':
    main()
