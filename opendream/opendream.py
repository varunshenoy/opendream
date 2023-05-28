import json
from . import layer, reference, storage

STORAGE = storage.Storage()

operators = {}

# TODO: all decorators must return Layer objects
# decorator to make a function into a dream operator
def operator(func, layer_name: str = None):

    def wrapper(*args, **kwargs):

        # Run decorated function
        image = func(*args, **kwargs)

        # iterate through args / kwargs, replace layer objects with layer names (makes metadata compact)
        lm_args = list(args)   
        lm_kwargs = kwargs.copy()
        for i in range(len(lm_args)):
            lm_args[i] = lm_args[i].get_name() if isinstance(lm_args[i], layer.Layer) else lm_args[i]
        for key, value in lm_kwargs.items():
            lm_kwargs[key] = value.get_name() if isinstance(value, layer.Layer) else value
        
        # create layer, provide operation and arguments as metadata
        params = {"op": func.__name__, "args": lm_args, "kwargs": lm_kwargs}
        l = layer.Layer(image=image, metadata=params, name = layer_name)

        # add to storage
        STORAGE.add_layer(l)
        return l

    operators[func.__name__] = func 
    return wrapper

@operator
def dream(prompt: str, model_ckpt: str = "runwayml/stable-diffusion-v1-5", seed: int = 42, device: str = "mps", batch_size: int = 1, selected: int = 0, num_steps: int = 20, guidance_scale: float = 7.5, **kwargs):
    return reference.dream(prompt, model_ckpt, seed, device, batch_size, selected, num_steps, guidance_scale, **kwargs)

@operator
def mask_and_inpaint(mask_image, image, prompt, model_ckpt, seed: int = 42, device: str = "mps", batch_size: int = 1, selected: int = 0, num_steps: int = 20, guidance_scale: float = 7.5, **kwargs):
    return reference.mask_and_inpaint(mask_image, image, prompt, model_ckpt, seed, device, batch_size, selected, num_steps, guidance_scale, **kwargs)

@operator
def make_dummy_mask():
    return reference.make_dummy_mask()


# # populate the operators dictionary 
# global_vars = globals().copy()

# # Iterate over global variables
# for var_name, var_value in global_vars.items():
#     # Check if the variable is a function decorated with @operator
#     if callable(var_value) and hasattr(var_value, '__name__') and var_value.__name__ != operator.__name__:
#         operators[var_value.__name__] = var_value

def save(json_file_path: str = "opendream.json"):

    ordering = STORAGE.get_ordering()
    data = {}

    # Iterate through layer list, write metadata to dictionary
    for i, layer_name in enumerate(ordering):
        layer = STORAGE.get_layer(layer_name)
        data[layer_name] = layer.get_metadata()

    # Write dictionary to disk
    with open(json_file_path, 'w') as outfile:
        json.dump(data, outfile, indent = 4)
    return


def execute(json_file_path: str):
    # override operators as necessary
    globals_vars = globals().copy()

    # Iterate over global variables
    for var_name, var_value in globals_vars.items():
        # Check if the variable is a function decorated with @operator
        if callable(var_value) and hasattr(var_value, '__name__') and var_value.__name__ != operator.__name__ and hasattr(var_value, '__annotations__'):
            operators[var_value.__name__] = var_value

    # Execute operations outlined in json
    with open(json_file_path) as json_file:
        data = json.load(json_file)
        for layer_name, layer_metadata in data.items():
            try:
                # retrieve function corresponding to json operation
                func = operators[layer_metadata["op"]]

                # wrap function in @operator and execute
                layer = operator(func, layer_name)(*layer_metadata["args"], **layer_metadata["kwargs"])
            except Exception as e:
                print(f"Error executing {layer_metadata['op']}: {e}")
                raise e

    return STORAGE
