# python
import pytest
from is_prime import is_prime

@pytest.mark.parametrize("n,expected", [
    (2, True),
    (3, True),
    (4, False),
    (0, False),
    (1, False),
    (5, True),
    (97, True),
])
def test_is_prime_examples(n, expected):
    assert is_prime(n) == expected

def test_is_prime_type_error_for_non_int():
    with pytest.raises(TypeError):
        is_prime(3.14)
