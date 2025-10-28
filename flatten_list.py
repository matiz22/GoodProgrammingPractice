from typing import List, Any

def flatten_list(nested_list: list) -> list:
    """
    Flatten a list that may contain nested lists.
    Only instances of `list` are flattened (strings/tuples remain as elements).
    Example: [1, [2, 3], [4, [5]]] -> [1, 2, 3, 4, 5]
    """
    if not isinstance(nested_list, list):
        raise TypeError("nested_list must be a list")

    result: List[Any] = []

    def _flatten(lst: list) -> None:
        for item in lst:
            if isinstance(item, list):
                _flatten(item)
            else:
                result.append(item)

    _flatten(nested_list)
    return result
