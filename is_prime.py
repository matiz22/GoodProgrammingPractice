def is_prime(n: int) -> bool:
    """
    Return True if n is a prime number, False otherwise.
    Raises TypeError if n is not an int.
    """
    if not isinstance(n, int):
        raise TypeError("n must be an int")

    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False

    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True
