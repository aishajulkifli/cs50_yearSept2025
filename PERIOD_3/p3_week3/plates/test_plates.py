from plates import is_valid     # Import the function to be tested


def test_length():              # Test that the length of the plate is between 2 and 6 characters
    assert is_valid("A") == False
    assert is_valid("ABCDEFG") == False
    assert is_valid("AB") == True


def test_starting_letters():    # Test that the plate starts with at least two letters
    assert is_valid("1ABC") == False
    assert is_valid("A1BC") == False
    assert is_valid("AB123") == True


def test_numbers_rules():       # Test that numbers, if present, are at the end and do not start with 0
    assert is_valid("AB012") == False   # first number cannot be 0
    assert is_valid("AB123") == True
    assert is_valid("AB12C") == False   # no letters after number


def test_alphanumeric_only():   # Test that the plate contains only letters and numbers
    assert is_valid("AB@12") == False
    assert is_valid("AB 12") == False
    assert is_valid("AB12") == True
