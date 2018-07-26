import pytest

from epilogue import utils

@pytest.mark.parametrize("weight,expected",[
    ("70",True),
    ("60.0",True),
    ("Weight",False),
    ("123a",False),
])
def test_weight_validation(weight, expected):
    assert utils.validate_height(weight) == expected, "Incorrect Weight Validation"
