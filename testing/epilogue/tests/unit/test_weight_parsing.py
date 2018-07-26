import pytest

from epilogue import utils

def test_weight_not_set():
    weight = None
    weight_type = 1

    weight_val = utils.parse_weight(weight = weight, weight_type = weight_type)

    assert weight_val == 0.0, "When weight is not set, weight should be parse as 0"

def test_weight_is_zero():
    weight = 0
    weight_type = 1

    weight_val = utils.parse_weight(weight = weight, weight_type = weight_type)

    assert weight_val == 0.0, "When Weight is 0, parse it to 0"



@pytest.mark.parametrize(
    "weight, weight_type, expected",
    [
       ("70.5",2,70.5),
       ("70",2,70),
       ("125",1,56.70),
    ]
)
def test_weight(weight, weight_type, expected):
    assert utils.parse_weight(weight, weight_type) == expected, "Incorrect Weight parsed"
