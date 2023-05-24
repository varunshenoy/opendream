'''
The Layer class. A layer consists of an image and metadata. 
It can also optionally contain other kwargs. 
'''
from PIL import Image
import requests
import typing

class Layer:
    def __init__(self, image: Image.Image, metadata: dict, **kwargs):
        self.image = image
        self.metadata = metadata
        self.kwargs = kwargs # kwargs like opacity, etc.

    def get_image(self):
        return self.image
    
    def get_metadata(self):
        return self.metadata

    def init_from_url(self, url: str, metadata: dict, **kwargs):
        self.image = Image.open(requests.get(url, stream=True).raw)
        self.metadata = {}
        self.kwargs = {}


