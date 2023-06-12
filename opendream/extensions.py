from opendream import opendream
from opendream.layer import Layer
from .layer import Layer
from PIL import Image
from .reference import sam
# USERS CAN ADD THEIR OWN OPERATIONS HERE

# @opendream.define_op
# def a_test_operation(test: str):
#     width, height = 512, 512 
#     dummy_image = Image.new("1", (width, height))
#     return opendream.Layer(dummy_image)

# @opendream.define_op
# def dream(prompt: str):
#     import openai
#     import os
    
#     openai.api_key = os.environ["OPENAI_API_KEY"]
    
#     response = openai.Image.create(
#         prompt=prompt,
#         n=1,
#         size="512x512",
#     )
#     image_url = response['data'][0]['url']
    
#     return Layer.from_url(image_url)

# layer = Layer.from_url("https://i.imgur.com/KuWzaVC.png")
# mask = sam(layer)
# mask.save_image()


