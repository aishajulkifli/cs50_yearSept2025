from PERIOD_3.p3_week3.my_twttr.twttr import shorten


def test_lowercase():
    assert shorten("twitter") == "twttr"        # Test that lowercase letters are removed correctly


def test_uppercase():
    assert shorten("TWITTER") == "TWTTR"        # Test that uppercase letters are removed correctly


def test_mixed_case():
    assert shorten("TwItTeR") == "TwtTR"        # Test that mixed case letters are removed correctly


def test_numbers():
    assert shorten("12345") == "12345"          # Test that numbers are not removed


def test_punctuation():
    assert shorten("hello!") == "hll!"          # Test that punctuation is not removed


def test_empty_string():
    assert shorten("") == ""                    # Test that an empty string returns an empty string
