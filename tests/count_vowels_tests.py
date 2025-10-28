import pytest

from count_vowels import count_vowels


@pytest.mark.parametrize("value,expected", [
    ("Python", 1),
    ("AEIOUY", 6),
    ("bcd", 0),
    ("", 0),
    ("Próba żółwia", 4),
])
def test_count_vowels_cases(value, expected):
    assert count_vowels(value) == expected