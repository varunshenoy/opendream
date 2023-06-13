'''
Reference implementation of various functions. The reason this exists
is so that the user can choose to either stick with the 
'''

import numpy as np

from diffusers import StableDiffusionPipeline, StableDiffusionPipeline
from diffusers import StableDiffusionInpaintPipeline, StableDiffusionInstructPix2PixPipeline, EulerAncestralDiscreteScheduler
from diffusers import StableDiffusionControlNetPipeline, UniPCMultistepScheduler, ControlNetModel

import os
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"
import torch

from PIL import Image
from controlnet_aux import CannyDetector, OpenposeDetector

from .layer import Layer, ImageLayer, MaskLayer

# construct path 
ROOT = os.path.dirname(os.path.abspath(__file__))
SAM_CHECKPOINT_PATH = os.path.join(ROOT, "checkpoints", "sam_vit_h_4b8939.pth")

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


def mask_from_data_URI(URI: str):
    print(URI)
    # TODO: Convert Data URI to PIL Image.
    return


def instruct_pix2pix(image_layer: ImageLayer, prompt, device = "mps"):
    model_id = "timbrooks/instruct-pix2pix"
    pipe = StableDiffusionInstructPix2PixPipeline.from_pretrained(model_id, torch_dtype=torch.float32, safety_checker=None)
    pipe.to(device)
    pipe.scheduler = EulerAncestralDiscreteScheduler.from_config(pipe.scheduler.config)
    
    images = pipe(prompt, image=image_layer.get_image().convert("RGB"), num_inference_steps=10, image_guidance_scale=1).images
    return Layer(images[0])


def controlnet_canny(image_layer: ImageLayer, prompt, device: str = "cpu", model_ckpt: str = "runwayml/stable-diffusion-v1-5", batch_size = 1, seed = 42, selected = 0, num_steps = 20, **kwargs):
    canny = CannyDetector()
    canny_image = canny(image_layer.get_image())
    
    controlnet = ControlNetModel.from_pretrained("lllyasviel/sd-controlnet-canny", torch_dtype=torch.float32)
    pipe = StableDiffusionControlNetPipeline.from_pretrained(
        model_ckpt, controlnet=controlnet, torch_dtype=torch.float32, safety_checker=None
    ).to(device)
    
    pipe.scheduler = UniPCMultistepScheduler.from_config(pipe.scheduler.config)
    if device == "cuda":
        pipe.enable_xformers_memory_efficient_attention()
        pipe.enable_model_cpu_offload()
    
    generator = [torch.Generator().manual_seed(seed + i) for i in range(batch_size)]
    
    controlnet_image = pipe(
        prompt,
        canny_image,
        num_inference_steps=num_steps,
        generator=generator,
    ).images[selected]
    
    return Layer(image=controlnet_image)


def controlnet_openpose(image_layer: ImageLayer, prompt, device: str = "cpu", model_ckpt: str = "runwayml/stable-diffusion-v1-5", batch_size = 1, seed = 42, selected = 0, num_steps = 20, **kwargs):
    openpose = OpenposeDetector.from_pretrained("lllyasviel/Annotators")
    openpose_image = openpose(image_layer.get_image(), hand_and_face=True)
    
    controlnet = ControlNetModel.from_pretrained("lllyasviel/sd-controlnet-openpose", torch_dtype=torch.float32)
    pipe = StableDiffusionControlNetPipeline.from_pretrained(
        model_ckpt, controlnet=controlnet, torch_dtype=torch.float32, safety_checker=None
    ).to(device)
    
    pipe.scheduler = UniPCMultistepScheduler.from_config(pipe.scheduler.config)
    if device == "cuda":
        pipe.enable_xformers_memory_efficient_attention()
        pipe.enable_model_cpu_offload()
    
    generator = [torch.Generator().manual_seed(seed + i) for i in range(batch_size)]
    
    controlnet_image = pipe(
        prompt,
        openpose_image,
        num_inference_steps=num_steps,
        generator=generator,
    ).images[selected]
    
    return Layer(image=controlnet_image)
    
def convert_mask_to_layer(mask):
    rle_mask = mask['segmentation']

    # Convert boolean mask to integer (0 or 255) for pixel values
    image_data = np.where(rle_mask, 255, 0).astype(np.uint8)

    # Create a PIL image from the image data
    image = Image.fromarray(image_data, mode='L')

    return MaskLayer(image=image)

# TODO: ONNX web runtime instead of this 
def sam(image_layer: ImageLayer, points=None):
    model_type = "vit_h"
    # device = "cuda"
    from segment_anything import SamAutomaticMaskGenerator, sam_model_registry
    sam = sam_model_registry[model_type](checkpoint=SAM_CHECKPOINT_PATH)
    # sam.to(device)
    
    mask_generator = SamAutomaticMaskGenerator(sam)
    
    # drop the alpha channel, if it exists
    image = image_layer.get_image().convert("RGB")
    
    masks = mask_generator.generate(np.array(image))
    # this should probably be with ONNX and not a remote server? 
    # return only the first mask for now
    # TODO: allow for multiple masks
    return [convert_mask_to_layer(mask) for mask in masks]
