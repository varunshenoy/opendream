import numpy as np

from diffusers import StableDiffusionPipeline
from diffusers import StableDiffusionInpaintPipeline, StableDiffusionInstructPix2PixPipeline, EulerAncestralDiscreteScheduler
from diffusers import StableDiffusionControlNetPipeline, UniPCMultistepScheduler, ControlNetModel

import os
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"
import importlib.util
import torch

from PIL import Image
from controlnet_aux import CannyDetector, OpenposeDetector

from .layer import Layer, ImageLayer, MaskLayer

def dream(prompt: str, model_ckpt: str = "runwayml/stable-diffusion-v1-5", seed: int = 42, device: str = "mps", batch_size: int = 1, selected: int = 0, num_steps: int = 20, guidance_scale: float = 7.5, **kwargs):
    pipe = StableDiffusionPipeline.from_pretrained(model_ckpt, torch_dtype=torch.float32, safety_checker=None)
    pipe = pipe.to(device)
    
    generator = [torch.Generator().manual_seed(seed + i) for i in range(batch_size)]
    
    image = pipe(prompt, generator=generator, num_inference_steps=num_steps, guidance_scale=guidance_scale).images[selected]

    return Layer(image=image)


def mask_and_inpaint(mask_layer: MaskLayer, image_layer: ImageLayer, prompt: str, model_ckpt: str = "stabilityai/stable-diffusion-2-inpainting", seed: int = 42, device: str = "mps", batch_size: int = 1, selected: int = 0, num_steps: int = 20, guidance_scale: float = 11, **kwargs):
    pipe = StableDiffusionInpaintPipeline.from_pretrained(
        model_ckpt,
        safety_checker=None,
    )
    pipe = pipe.to(device)
    
    generator = [torch.Generator().manual_seed(seed + i) for i in range(batch_size)]
    
    inpainted_image = pipe(prompt=prompt, image=image_layer.get_image(), mask_image=mask_layer.get_image(), generator=generator, num_inference_steps=num_steps, guidance_scale=guidance_scale).images[selected]

    return Layer(image=inpainted_image)
