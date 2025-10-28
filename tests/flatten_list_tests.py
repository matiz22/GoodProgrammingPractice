import pytest
from flatten_list import flatten_list

@pytest.mark.parametrize("input_list,expected", [
    ([1, 2, 3], [1, 2, 3]),
    ([1, [2, 3], [4, [5]]], [1, 2, 3, 4, 5]),
    ([], []),
    ([[[1]]], [1]),
    ([1, [2, [3, [4]]]], [1, 2, 3, 4]),
])
def test_flatten_list_cases(input_list, expected):
    assert flatten_list(input_list) == expected
