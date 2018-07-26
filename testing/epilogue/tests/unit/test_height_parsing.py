from epilogue import utils

import pytest
import math


def test_height_not_set():
    height = None
    height_type = 1

    height_val = utils.parse_height(height, height_type)

    assert height_val == 0.0, "Incorrect Height returned for when height is None"

def test_height_is_zero():
    height = 0
    height_type = 1

    height_val = utils.parse_height(height = height, height_type = height_type)

    assert height_val == 0.0, "Incorrect Height returned for when height is 0"

@pytest.mark.parametrize("height_in_feet,height_in_m",[
    ("5.01",1.549),
    ("5.1", 1.549),
    ("5.10",1.778),
])
def test_height_is_set_in_feet(height_in_feet, height_in_m):
    assert math.isclose(
        utils.parse_height(height = height_in_feet, height_type = 1), 
        height_in_m,
        rel_tol = 1e-1,
    )     , "Height Being parsed incorrectly"

