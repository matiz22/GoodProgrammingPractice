import pytest
from word_frequencies import word_frequencies

@pytest.mark.parametrize("text,expected", [
    ("To be or not to be", {"to": 2, "be": 2, "or": 1, "not": 1}),
    ("Hello, hello!", {"hello": 2}),
    ("", {}),
    ("Python Python python", {"python": 3}),
    ("Ala ma kota, a kot ma Ale.", {"ala": 1, "ma": 2, "kota": 1, "a": 1, "kot": 1, "ale": 1}),
])
def test_word_frequencies_examples(text, expected):
    assert word_frequencies(text) == expected

def test_word_frequencies_type_error_for_non_string():
    with pytest.raises(TypeError):
        word_frequencies(123)
