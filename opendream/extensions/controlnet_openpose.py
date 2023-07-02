import torch
from diffusers import UniPCMultistepScheduler, ControlNetModel, StableDiffusionControlNetPipeline

from opendream import opendream
from opendream.layer import ImageLayer, Layer
from controlnet_aux import OpenposeDetector

@opendream.define_op
def controlnet_openpose(control_image_layer: ImageLayer, prompt, device: str = "cpu", model_ckpt: str = "runwayml/stable-diffusion-v1-5", batch_size = 1, seed = 42, selected = 0, num_steps = 20, **kwargs):
    openpose = OpenposeDetector.from_pretrained("lllyasviel/Annotators")
    openpose_image = openpose(control_image_layer.get_image(), hand_and_face=True)
    
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