'''
The `Storage` class holds information and helper functions
for the List[Layer] backend.
'''
from layer import Layer

class Storage:
    # Singleton
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Storage, cls).__new__(cls)
        return cls.instance
  
    def __init__(self):
        # Dict from layer_name: str --> layer: Layer
        self.layers = {}
        # Ordering of layers List[layer_name]
        self.ordering = []

    def add_layer(self, layer: Layer):
        name = layer.name
        self.layers[name] = layer
        self.ordering.append(name)

    def delete_layer(self, name: str) -> bool:
        if name in self.layers:
            self.layers.pop(name)
            self.ordering.remove(name)
            return True
        return False
