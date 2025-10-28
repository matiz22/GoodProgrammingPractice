import unicodedata
from typing import Union


def count_vowels(value: Union[str, int]) -> int:
    """
    Return the number of vowel characters in `value`.
    - Accepts strings or integers (converted to string).
    - Normalizes Unicode, is case-insensitive.
    - Counts vowels including Polish diacritics: a, ą, e, ę, i, o, ó, u, y.
    """
    if not isinstance(value, (str, int)):
        raise TypeError("value must be a str or int")
    s = str(value)
    s = unicodedata.normalize("NFC", s).lower()
    vowels = set("aąeęiouyó")
    return sum(1 for ch in s if ch in vowels)