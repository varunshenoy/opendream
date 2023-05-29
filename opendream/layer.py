'''
The Layer class. A layer consists of an image and metadata. 
It can also optionally contain other kwargs. 
'''
from PIL import Image
import requests
import typing
import uuid

class Layer:

    def __init__(self, image: Image.Image, metadata: dict = {}, **kwargs):
        self.image = image
        self.id = -1
        self.metadata = metadata
        self.kwargs = kwargs # kwargs like opacity, etc.

    def get_image(self):
        return self.image
    
    def get_id(self):
        return self.id
    
    def set_id(self, id):
        self.id = id
    
    def get_metadata(self):
        return self.metadata
    
    def set_metadata(self, metadata: dict):
        self.metadata = metadata
        
    def save_image(self):
        self.image.save(f"debug/{self.id}.png")
        
    @staticmethod
    def from_url(url: str, metadata: dict = {}, **kwargs):
        return Layer(
            image=Image.open(requests.get(url, stream=True).raw),
            metadata=metadata,
            **kwargs
        )
        
    @staticmethod
    def from_path(path: str, metadata: dict = {}, **kwargs):
        return Layer(
            image=Image.open(path),
            metadata=metadata,
            **kwargs
        )

    @staticmethod
    def from_binary_mask(
        pixels: typing.List[typing.Tuple[int,int]],
        metadata: dict = {}, **kwargs
    ):
        # TODO: Convert pixels to image mask.
        raise NotImplementedError("Need to figure this out!")

    @staticmethod
    def from_segmentation(
        pixels: typing.List[typing.Tuple[int,int]],
        colors: typing.List[typing.Tuple[int,int,int]],
        metadata: dict = {}, **kwargs
    ):
        # TODO: Hmmmmm
        raise NotImplementedError("Need to figure this out!")
