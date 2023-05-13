from opendream import opendream
import numpy as np
from diffusers import StableDiffusionPipeline, StableDiffusionInpaintPipeline
import torch
from PIL import Image

@opendream.dream
def dream(prompt: str, model_ckpt: str = "runwayml/stable-diffusion-v1-5", seed: int = 42, device: str = "mps", batch_size: int = 1, selected: int = 0, num_steps: int = 5, guidance_scale: float = 7.5, **kwargs):
    pipe = StableDiffusionPipeline.from_pretrained(model_ckpt, torch_dtype=torch.float16, safety_checker=None)
    pipe = pipe.to(device)
    
    generator = [torch.Generator().manual_seed(seed + i) for i in range(batch_size)]
    
    image = pipe(prompt, generator=generator, num_inference_steps=num_steps, guidance_scale=guidance_scale).images[selected]

    image.save(f"{prompt}.png")
    return image.copy()


# this doesn't work yet lol
@opendream.mask_and_inpaint
def mask_and_inpaint(mask_image: Image.Image, image: Image.Image, prompt: str, model_ckpt: str = "runwayml/stable-diffusion-inpainting", seed: int = 42, device: str = "mps", batch_size: int = 1, selected: int = 0, num_steps: int = 20, guidance_scale: float = 7.5, **kwargs):
    pipe = StableDiffusionInpaintPipeline.from_pretrained(
        model_ckpt,
        revision="fp16",
        torch_dtype=torch.float16,
        safety_checker=None,
    )
    pipe = pipe.to(device)
    
    generator = [torch.Generator().manual_seed(seed + i) for i in range(batch_size)]
    
    image = pipe(prompt=prompt, image=image, mask_image=mask_image, generator=generator, num_inference_steps=num_steps, guidance_scale=guidance_scale).images[selected]
    image.save(f"{prompt}_inpaint.png")
    return image
        
output_image = opendream.execute("workflows/basic_dream+inpaint.json")