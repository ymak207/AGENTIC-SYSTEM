def calculate(expression: str) -> str:
    """
    Safely evaluate basic math expressions.
    """

    try:
        allowed_chars = "0123456789+-*/(). "

        for char in expression:
            if char not in allowed_chars:
                return "Invalid characters in expression"

        result = eval(expression)

        return str(result)

    except Exception as e:
        return f"Calculation error: {str(e)}"