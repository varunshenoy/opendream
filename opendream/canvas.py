'''
The `Storage` class holds information and helper functions
for the List[Layer] backend.
'''
from .layer import Layer

DEBUG = True

class Canvas:
    
    # Singleton
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Canvas, cls).__new__(cls)
        return cls.instance
  
    def __init__(self):
        # Dict from layer_name: str --> layer: Layer
        self.layers = {}
        
        self.next_id = 0
        
        # Ordering of layers List[layer_name]
        self.ordering = []

    def add_layer(self, layer: Layer):
        curr_id = str(self.next_id)
        layer.set_id(curr_id)
        self.layers[curr_id] = layer
        self.ordering.append(curr_id)
        self.next_id += 1
        
        if DEBUG:
            layer.save_image()

    def delete_layer(self, layer_id: str) -> bool:
        if layer_id in self.layers:
            self.layers.pop(layer_id)
            self.ordering.remove(layer_id)
            return True
        return False
    
    def get_ordering(self) -> list[str]:
        return self.ordering
    
    def get_layer(self, layer_id: str) -> Layer:
        if layer_id in self.layers:
            return self.layers[layer_id]
        return None
    
    def get_serialized_layers(self) -> list[dict]:
        return [self.layers[layer_id].serialize() for layer_id in self.ordering]
    
    def get_workflow(self):
        data = {}

        # Iterate through layer list, write metadata to dictionary
        for i, layer_name in enumerate(self.ordering):
            layer = self.get_layer(layer_name)
            data[layer_name] = layer.get_metadata()
            
        return data
