from opendream import opendream
import numpy as np
from diffusers import StableDiffusionPipeline
import torch

@opendream.dream
def dream(prompt: str, model_ckpt: str = "runwayml/stable-diffusion-v1-5", seed: int = 42, device: str = "mps", num_dreams: int = 1, selected: int = 0, num_steps: int = 20, guidance_scale: float = 7.5, **kwargs):
    pipe = StableDiffusionPipeline.from_pretrained(model_ckpt, torch_dtype=torch.float16, safety_checker=None)
    pipe = pipe.to(device)
    
    generator = [torch.Generator().manual_seed(seed + i) for i in range(num_dreams)]
    
    image = pipe(prompt, generator=generator, num_inference_steps=num_steps, guidance_scale=guidance_scale).images[selected]
    
    image.save(f"{prompt}.png")
    return image

@opendream.mask_and_inpaint
def mask_and_inpaint(mask: np.ndarray, image: np.ndarray):
    # mask the image
    image[mask] = 0
    
    # inpaint the image
    return image
    
opendream.execute("workflows/basic_dream.json")