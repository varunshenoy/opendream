# testing using pytest

import pytest
from opendream import opendream
from PIL import Image
import os

def test_sanity():
    assert 1 == 1

def test_num_layers():
    layers = opendream.execute("layers.json")
    assert len(layers) == 2

def test_dream():
    # make sure each layer has an associated image
    pass

def test_delete():
    # size of layers is decremented by 1
    pass