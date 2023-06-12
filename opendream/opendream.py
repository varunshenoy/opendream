import json
from . import reference
from .layer import Layer, ImageLayer, MaskLayer
from .canvas import Canvas

CANVAS = Canvas()
QUEUE = []
DEBUG = True

operators = {}

# decorator to make a function into a dream operator
def define_op(func):

    def wrapper(*args, **kwargs):

        # Run decorated function
        layers = func(*args, **kwargs)

        # if layers is not a list, make it a list
        if not isinstance(layers, list):
            layers = [layers]
        # since the layers were output by the function by passing in the same 
        # params, they all have the same metadata. We only need to set it once.

        # iterate through args / kwargs, replace layer objects with layer names (makes metadata compact)
        lm_args = list(args)   
        lm_kwargs = kwargs.copy()
        for i in range(len(lm_args)):
            lm_args[i] = lm_args[i].get_id() if isinstance(lm_args[i], Layer) else lm_args[i]
        for key, value in lm_kwargs.items():
            lm_kwargs[key] = value.get_id() if isinstance(value, Layer) else value
        
        # create layer, provide operation and arguments as metadata
        print("number of layers:")
        print(len(layers))
        for l in layers:
            l.set_metadata({"op": func.__name__, "params": lm_args, "options": lm_kwargs})
            # add to CANVAS
            CANVAS.add_layer(l)
            print("added layer to canvas")

        return layers
    
    func.title = func.__name__.replace("_", " ").title()
    operators[func.__name__] = func 
    return wrapper

def add_task_to_queue(func, *args, **kwargs):
    QUEUE.append((func, args, kwargs))

def execute_queue():
    for idx, (func, args, kwargs) in enumerate(QUEUE):
        func(*args, **kwargs)
        QUEUE.pop(idx)

def save(json_file_path: str = "opendream.json"):

    # Get workflow from canvas
    data = CANVAS.get_workflow()

    # Write dictionary to disk
    with open(json_file_path, 'w') as outfile:
        json.dump(data, outfile, indent = 4)

@define_op
def dream(prompt: str, model_ckpt: str = "runwayml/stable-diffusion-v1-5", seed: int = 42, device: str = "mps", batch_size: int = 1, selected: int = 0, num_steps: int = 20, guidance_scale: float = 7.5, **kwargs):
    return reference.dream(prompt, model_ckpt, seed, device, batch_size, selected, num_steps, guidance_scale, **kwargs)

@define_op
def mask_and_inpaint(mask_layer: MaskLayer, image_layer: ImageLayer, prompt: str, model_ckpt: str = "stabilityai/stable-diffusion-2-inpainting", seed: int = 42, device: str = "mps", batch_size: int = 1, selected: int = 0, num_steps: int = 20, guidance_scale: float = 11, **kwargs):
    return reference.mask_and_inpaint(mask_layer, image_layer, prompt, model_ckpt, seed, device, batch_size, selected, num_steps, guidance_scale, **kwargs)

@define_op
def mask_from_data_URI(URI: str):
    return reference.mask_from_data_URI(URI)

@define_op
def instruct_pix2pix(image_layer: ImageLayer, prompt, device = "mps"):
    return reference.instruct_pix2pix(image_layer, prompt, device)

@define_op
def controlnet_canny(image_layer: ImageLayer, prompt, device: str = "cpu", model_ckpt: str = "runwayml/stable-diffusion-v1-5", batch_size = 1, seed = 42, selected = 0, num_steps = 20, **kwargs):
    return reference.controlnet_canny(image_layer, prompt, device, model_ckpt, batch_size, seed, selected, num_steps, **kwargs)

@define_op
def controlnet_openpose(image_layer: ImageLayer, prompt, device: str = "cpu", model_ckpt: str = "runwayml/stable-diffusion-v1-5", batch_size = 1, seed = 42, selected = 0, num_steps = 20, **kwargs):
    return reference.controlnet_openpose(image_layer, prompt, device, model_ckpt, batch_size, seed, selected, num_steps, **kwargs)

@define_op
def sam(image_layer: ImageLayer, prompt=None):
    # if no prompt is provided, return all masks
    return reference.sam(image_layer, prompt)

@define_op
def load_image_from_path(path: str):
    return Layer.from_path(path)

def execute(json_file_path: str):
    
    # delete all files in debug folder
    if DEBUG:
        import os
        for filename in os.listdir("debug/"):
            os.remove(f"debug/{filename}")

    # Execute operations outlined in json
    with open(json_file_path) as json_file:
        data = json.load(json_file)
        for _, layer_metadata in data.items():
            print(layer_metadata)
            try:
                # retrieve function corresponding to json operation
                func = operators[layer_metadata["op"]]
                
                
                # cross-reference layer names with layers in canvas
                for index, arg in enumerate(layer_metadata["params"]):
                    associated_layer = CANVAS.get_layer(arg)
                    if associated_layer is not None:
                        layer_metadata["params"][index] = associated_layer
                
                # run function with arguments
                print(func)
                layer = define_op(func)(*layer_metadata["params"], **layer_metadata["options"])
                
            except Exception as e:
                print(f"Error executing {layer_metadata['op']}: {e}")
                raise e

    return CANVAS