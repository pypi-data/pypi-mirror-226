import pytest
from RiteshSum import doSum

test_data = [(10, 20, 30), (-1, -2, -3), (78, 100, 178)]


@pytest.mark.parametrize("number1,number2,expected", test_data)
def test_sum_functionality(number1, number2, expected):
    assert doSum(number1, number2) == expected
