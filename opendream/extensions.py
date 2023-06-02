from layer import Layer
from PIL import Image
from reference import sam
# USERS CAN ADD THEIR OWN OPERATIONS HERE

# @opendream.define_op
# def a_test_operation(test: str):
#     width, height = 512, 512 
#     dummy_image = Image.new("1", (width, height))
#     return opendream.Layer(dummy_image)


layer = Layer.from_url("https://i.imgur.com/KuWzaVC.png")
sam(layer)