import pytest

from epilogue import utils

@pytest.mark.parametrize("height,expected",[
    ("5.01",True),
    ("5.10",True),
    ("Height",False),#do not match non number strings
    ("123a", False),
])
def test_height_validation(height, expected):
    assert utils.validate_height(height) == expected, "Incorrect height validated"
