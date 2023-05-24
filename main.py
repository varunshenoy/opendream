from opendream import opendream

# doing this overrides the default behavior of the default dream operator
@opendream.operator
def dream(prompt: str, model_ckpt: str = "runwayml/stable-diffusion-v1-5", seed: int = 42, device: str = "mps", batch_size: int = 1, selected: int = 0, num_steps: int = 20, guidance_scale: float = 7.5, **kwargs):
    return "override"
  
layers = opendream.execute("workflows/basic_dream+inpaint.json")