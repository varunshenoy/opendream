from opendream import opendream
from PIL import Image

# USERS CAN ADD THEIR OWN OPERATIONS HERE

@opendream.define_op
def a_test_operation(test: str):
    width, height = 512, 512 
    dummy_image = Image.new("1", (width, height))
    return opendream.Layer(dummy_image)