def validate_abn(abn) -> bool:

    # Provided by the ABR
    weights = [10, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19]

    try:
        abn = list(int(i) for i in str(abn).replace(" ", ""))
    except ValueError:
        return False

    if len(abn) > 11:
        return False

    # subtract 1 from the first digit of the ABN
    abn[0] = int(abn[0]) - 1

    # sum the product of the abn digits and weights
    digit_sum = sum([x * y for x, y in zip(abn, weights)])

    if digit_sum % 89 == 0:
        return True

    return False
