import pytest
from fuel import convert, gauge


# --------------------
# Tests for convert()
# --------------------

def test_convert_regular_values():  # Regular cases
    assert convert("1/2") == 50     # assert that 1/2 is 50%, assert is used to check if the function returns the expected value
    assert convert("1/4") == 25
    assert convert("3/4") == 75
    assert convert("2/3") == 67  # Rounded


def test_convert_edge_values():     # Edge cases
    assert convert("0/1") == 0      # 0% when numerator is 0, assert is used to check if the function returns the expected value
    assert convert("1/1") == 100


def test_convert_invalid_values():  # Invalid cases
    with pytest.raises(ValueError): # Expect a ValueError when the input is not in the correct format
        convert("3/2")  # X > Y     # convert should raise a ValueError when the numerator is greater than the denominator, numerator is 3 and denominator is 2

    with pytest.raises(ValueError): # Expect a ValueError when the input is not in the correct format
        convert("cat/dog")  # Not integers

    with pytest.raises(ZeroDivisionError):  # Expect a ZeroDivisionError when the denominator is zero
        convert("1/0")


# --------------------
# Tests for gauge()
# --------------------

def test_gauge_empty():     # Empty or nearly empty cases
    assert gauge(0) == "E"  # assert that 0% is "E"
    assert gauge(1) == "E"  # assert that 1% is "E",


def test_gauge_full():      # Full or nearly full cases
    assert gauge(99) == "F" # assert that 99% is "F"
    assert gauge(100) == "F"    # assert that 100% is "F",

def test_gauge_percentage():    # Regular percentage cases
    assert gauge(50) == "50%"   # assert that 50% is "50%"
    assert gauge(67) == "67%"
