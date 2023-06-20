from opendream import opendream
from opendream.layer import Layer

import openai
import os

@opendream.define_op
def dream(prompt: str):
    
    openai.api_key = os.environ["OPENAI_API_KEY"]
    
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="512x512",
    )
    image_url = response['data'][0]['url']
    
    return Layer.from_url(image_url)