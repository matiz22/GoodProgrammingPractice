def fibonacci(n: int) -> int:
    """
    Return the n-th Fibonacci number.
    - fibonacci(0) == 0
    - fibonacci(1) == 1
    Raises:
        TypeError: if n is not an integer
        ValueError: if n is negative
    """
    if not isinstance(n, int):
        raise TypeError("n must be an integer")
    if n < 0:
        raise ValueError("n must be non-negative")

    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a