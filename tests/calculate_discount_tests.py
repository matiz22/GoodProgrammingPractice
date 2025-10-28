import pytest

from calculate_discount import calculate_discount


@pytest.mark.parametrize("price,discount,expected", [
    (100, 0.2, 80.0),
    (50, 0.0, 50.0),
    (200, 1.0, 0.0),
])
def test_calculate_discount_values(price, discount, expected):
    assert calculate_discount(price, discount) == expected

@pytest.mark.parametrize("price,discount", [
    (100, -0.1),
    (100, 1.5),
])
def test_calculate_discount_invalid_discount_raises(price, discount):
    with pytest.raises(ValueError):
        calculate_discount(price, discount)