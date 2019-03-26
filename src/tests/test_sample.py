"""Basic tests to test env"""
# content of test_sample.py


def func(num):
    """basic function to test"""
    return num + 1


def test_answer():
    """test previously defined function"""
    assert func(3) == 4
