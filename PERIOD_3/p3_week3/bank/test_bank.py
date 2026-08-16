from bank import value              # Import the value function from the bank module for testing


def test_hello():                   # Test cases for greetings that start with "hello"
    assert value("hello") == 0
    assert value("Hello") == 0
    assert value("HELLO") == 0
    assert value("hello there") == 0


def test_h_but_not_hello():
    assert value("hi") == 20
    assert value("hey") == 20
    assert value("How are you?") == 20


def test_other_greetings():
    assert value("what's up") == 100
    assert value("good morning") == 100
    assert value("bye") == 100
