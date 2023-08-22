# factorial.py

def factorial(n):
    """
    Calculate the factorial of a non-negative integer.

    Args:
        n (int): The non-negative integer for which to calculate the factorial.

    Returns:
        int or str: The factorial of the input integer, or an error message if input is invalid.

    Raises:
        ValueError: If the input is a negative number.

    Example:
	>>> import simple_factorial
        >>> simple_factorial.factorial(5)
        120
    """
    n = int(n)
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

if __name__ == "__main__":
    while True:
        num = input("Enter a non-negative integer (or 'q' to quit): ")
        if num.lower() == 'q':
            break
        result = calculate_factorial(num)
        print(result)
