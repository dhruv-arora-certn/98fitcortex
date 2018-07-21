from epilogue import utils



def test_height_not_set():
    height = None
    height_type = 1

    height_val = utils.parse_height(height, height_type)

    assert height_val is 0.0 , ""
