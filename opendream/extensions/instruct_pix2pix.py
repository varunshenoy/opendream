import torch
from diffusers import StableDiffusionInstructPix2PixPipeline, EulerAncestralDiscreteScheduler

from opendream import opendream
from opendream.layer import Layer, ImageLayer

@opendream.define_op
def instruct_pix2pix(image_layer: ImageLayer, prompt, device = "mps"):
    model_id = "timbrooks/instruct-pix2pix"
    pipe = StableDiffusionInstructPix2PixPipeline.from_pretrained(model_id, torch_dtype=torch.float32, safety_checker=None)
    pipe.to(device)
    pipe.scheduler = EulerAncestralDiscreteScheduler.from_config(pipe.scheduler.config)
    
    images = pipe(prompt, image=image_layer.get_image().convert("RGB"), num_inference_steps=10, image_guidance_scale=1).images
    return Layer(images[0])