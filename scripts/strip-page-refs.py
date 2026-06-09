import sys
import re

text = sys.stdin.read()

text = re.sub(
    r'\(see\s+page\s+\\pageref\{[^}]*\}\)',
    '', text
)

text = re.sub(
    r'\(see\s*\n\s*page\s+\\pageref\{[^}]*\}\)',
    '', text
)

text = re.sub(
    r'\(see\s*\n\s*page\s*\n\s*\\pageref\{[^}]*\}\)',
    '', text
)

text = re.sub(
    r',?\s*on\s+page\s+\\pageref\{[^}]*\}',
    '', text
)

text = re.sub(
    r'\(see\s+[^)]*?,\s*on\s+page\s+\\pageref\{[^}]*\}\)',
    '', text
)

sys.stdout.write(text)
