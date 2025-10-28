def calculate_discount(price: float, discount: float) -> float:
    """
    Return price after applying discount.
    - calculate_discount(100, 0.2) -> 80.0
    Raises:
        TypeError: if price or discount are not numeric
        ValueError: if discount is not in [0, 1] or price is negative
    """
    if not isinstance(price, (int, float)):
        raise TypeError("price must be a number")
    if not isinstance(discount, (int, float)):
        raise TypeError("discount must be a number")
    if price < 0:
        raise ValueError("price must be non-negative")
    if discount < 0 or discount > 1:
        raise ValueError("discount must be between 0 and 1")
    return float(price * (1 - discount))