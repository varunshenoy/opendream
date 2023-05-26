import json
from . import layer, reference, storage

STORAGE = storage.Storage()

operators = {}

# TODO: all decorators must return Layer objects
# decorator to make a function into a dream operator
def operator(func):
    def final(f):
        image = f()
        l = layer.Layer(image=image)
        STORAGE.add_layer(l)
        return l

    operators[func.__name__] = final(func)
    return func

@operator
def dream(prompt: str, model_ckpt: str = "runwayml/stable-diffusion-v1-5", seed: int = 42, device: str = "mps", batch_size: int = 1, selected: int = 0, num_steps: int = 20, guidance_scale: float = 7.5, **kwargs):
    return reference.dream(prompt, model_ckpt, seed, device, batch_size, selected, num_steps, guidance_scale, **kwargs)

@operator
def mask_and_inpaint(mask_image, image, prompt, model_ckpt, seed: int = 42, device: str = "mps", batch_size: int = 1, selected: int = 0, num_steps: int = 20, guidance_scale: float = 7.5, **kwargs):
    return reference.mask_and_inpaint(mask_image, image, prompt, model_ckpt, seed, device, batch_size, selected, num_steps, guidance_scale, **kwargs)

@operator
def make_dummy_mask():
    return reference.make_dummy_mask()


# populate the operators dictionary 
global_vars = globals().copy()

# Iterate over global variables
for var_name, var_value in global_vars.items():
    # Check if the variable is a function decorated with @operator
    if callable(var_value) and hasattr(var_value, '__name__') and var_value.__name__ != operator.__name__:
        operators[var_value.__name__] = var_value

def execute(json_file_path: str):
    # override operators as necessary
    globals_vars = globals().copy()

    # Iterate over global variables
    for var_name, var_value in globals_vars.items():
        # Check if the variable is a function decorated with @operator
        if callable(var_value) and hasattr(var_value, '__name__') and var_value.__name__ != operator.__name__ and hasattr(var_value, '__annotations__'):
            operators[var_value.__name__] = var_value

    with open(json_file_path) as json_file:
        data = json.load(json_file)
        workflow = data["workflow"]
        for task in workflow:
            try:
                operators[task["operation"]](**task["params"])
            except Exception as e:
                print(f"Error executing {task['operation']}: {e}")
                raise e

    return STORAGE
