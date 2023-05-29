'''
Reference implementation of various functions. The reason this exists
is so that the user can choose to either stick with the 
'''

import numpy as np
from diffusers import StableDiffusionPipeline, StableDiffusionPipeline, StableDiffusionInpaintPipeline
import torch
from PIL import Image

from .layer import Layer


def dream(prompt: str, model_ckpt: str = "runwayml/stable-diffusion-v1-5", seed: int = 42, device: str = "mps", batch_size: int = 1, selected: int = 0, num_steps: int = 20, guidance_scale: float = 7.5, **kwargs):
    pipe = StableDiffusionPipeline.from_pretrained(model_ckpt, torch_dtype=torch.float32, safety_checker=None)
    pipe = pipe.to(device)
    
    generator = [torch.Generator().manual_seed(seed + i) for i in range(batch_size)]
    
    image = pipe(prompt, generator=generator, num_inference_steps=num_steps, guidance_scale=guidance_scale).images[selected]

    return Layer(image=image)


def mask_and_inpaint(mask_image: Layer, image: Layer, prompt: str, model_ckpt: str = "runwayml/stable-diffusion-inpainting", seed: int = 42, device: str = "mps", batch_size: int = 1, selected: int = 0, num_steps: int = 20, guidance_scale: float = 7.5, **kwargs):
    pipe = StableDiffusionInpaintPipeline.from_pretrained(
        model_ckpt,
        safety_checker=None,
    )
    pipe = pipe.to(device)
    
    generator = [torch.Generator().manual_seed(seed + i) for i in range(batch_size)]
    
    inpainted_image = pipe(prompt=prompt, image=image.get_image(), mask_image=mask_image.get_image(), generator=generator, num_inference_steps=num_steps, guidance_scale=guidance_scale).images[selected]

    return Layer(image=inpainted_image)


def make_dummy_mask():
    from PIL import Image, ImageDraw

    # Create a blank mask with the size of 512x512
    width, height = 512, 512
    mask = Image.new("1", (width, height))

    # Draw a simple shape on the mask using ImageDraw
    draw = ImageDraw.Draw(mask)
    draw.rectangle([128, 128, 384, 384], fill="white")
                
    return Layer(image=mask)
