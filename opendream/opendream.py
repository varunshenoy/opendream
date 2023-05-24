import json
import reference
# we need to represent the execution engine here

operators = {}

# decorator to make a function into a dream operator
def operator(func):
    operators[func.__name__] = func
    return func

@operator
def dream(prompt: str, model_ckpt: str = "runwayml/stable-diffusion-v1-5", seed: int = 42, device: str = "mps", batch_size: int = 1, selected: int = 0, num_steps: int = 20, guidance_scale: float = 7.5, **kwargs):
    return reference.dream(prompt, model_ckpt, seed, device, batch_size, selected, num_steps, guidance_scale, **kwargs)

@operator
def mask_and_inpaint(mask_image: Image.Image, image: Image.Image, prompt: str, model_ckpt: str = "runwayml/stable-diffusion-inpainting", seed: int = 42, device: str = "mps", batch_size: int = 1, selected: int = 0, num_steps: int = 20, guidance_scale: float = 7.5, **kwargs):
    return reference.mask_and_inpaint(mask_image, image, prompt, model_ckpt, seed, device, batch_size, selected, num_steps, guidance_scale, **kwargs)

@operator
def make_dummy_mask():
    return reference.make_dummy_mask()

def execute(json_file_path: str):
    layers = []
    with open(json_file_path) as json_file:
        data = json.load(json_file)
        workflow = data["workflow"]
        for task in workflow:
            try:
                layers.append(operators[task["operation"]](**task["params"]))
            except Exception as e:
                print(f"Error executing {task['operation']}: {e}")
                raise e

    return layers