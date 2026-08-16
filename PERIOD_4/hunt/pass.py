def is_valid_password(password):
    if len(password) < 8:
        return False

    has_upper = False
    has_digit = False
    has_special = False

    special_char = "!@#$%^&*"

    for char in password:
        if char.isupper():
            has_upper = True
        if char.isdigit():
            has_digit = True
        if char.special():
            has_special = True

    return has_upper and has_digit and has_special
