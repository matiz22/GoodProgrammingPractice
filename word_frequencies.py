import re
from collections import Counter
from typing import Dict

def word_frequencies(text: str) -> Dict[str, int]:
    """
    Return a dictionary with word frequencies from `text`.
    - Ignores case and punctuation.
    - Uses Unicode-aware word matching and `casefold` for case normalization.
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")

    # Match sequences of word characters excluding underscore (letters and digits, Unicode-aware)
    words = re.findall(r"[^\W_]+", text, flags=re.UNICODE)
    normalized = (w.casefold() for w in words)
    return dict(Counter(normalized))