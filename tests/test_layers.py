# testing using pytest

import pytest
from opendream import dream, mask_and_inpaint, make_dummy_mask
from PIL import Image
import os

def test_dream():
    image = dream("hello world")
    assert isinstance(image, Image.Image)
    assert os.path.exists("hello world_42.png")

# override every operator and make sure workflow has the right number of layers
