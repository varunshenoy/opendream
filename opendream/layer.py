'''
The Layer class. A layer consists of an image and metadata. 
It can also optionally contain other kwargs. 
'''
from PIL import Image
import requests
import typing
import uuid

class Layer:

    def __init__(self, image: Image.Image, name: str = "", metadata: dict = {}, **kwargs):
        self.image = image
        self.name = name or uuid.uuid4().hex    # clunky to store entire UUID object, store int for easy JSON writes
        self.metadata = metadata
        self.kwargs = kwargs # kwargs like opacity, etc.

    def get_image(self):
        return self.image
    
    def get_name(self):
        return self.name
    
    def get_metadata(self):
        return self.metadata
    
    @classmethod
    def from_url(cls, url: str, name: str = "", metadata: dict = {}, **kwargs):
        return cls(
            image=Image.open(requests.get(url, stream=True).raw),
            name=name,
            metadata=metadata,
            **kwargs
        )

    @classmethod
    def from_binary_mask(cls,
        pixels: typing.List[typing.Tuple[int,int]],
        name: str = "", metadata: dict = {}, **kwargs
    ):
        # TODO: Convert pixels to image mask.
        raise NotImplementedError("Need to figure this out!")

    @classmethod
    def from_segmentation(cls,
        pixels: typing.List[typing.Tuple[int,int]],
        colors: typing.List[typing.Tuple[int,int,int]],
        name: str = "", metadata: dict = {}, **kwargs
    ):
        # TODO: Hmmmmm
        raise NotImplementedError("Need to figure this out!")
