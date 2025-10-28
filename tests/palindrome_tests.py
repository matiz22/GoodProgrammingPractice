import pytest
from palindrome import is_palindrome

@pytest.mark.parametrize("value,expected", [
    ("kajak", True),
    ("Kobyła ma mały bok", True),
    ("python", False),
    ("", True),
    ("A", True),
])
def test_is_palindrome_cases(value, expected):
    assert is_palindrome(value) == expected