from typing import Union

def is_palindrome(value: Union[str, int], *, ignore_non_alphanumeric: bool = True) -> bool:
    """
    Return True if `value` is a palindrome.
    - Accepts strings or integers.
    - If `ignore_non_alphanumeric` is True, removes non-alphanumeric chars and is case-insensitive.
    """
    s = str(value)
    if ignore_non_alphanumeric:
        s = ''.join(ch.lower() for ch in s if ch.isalnum())
    else:
        s = s.lower()
    return s == s[::-1]