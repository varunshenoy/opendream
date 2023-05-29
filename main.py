from opendream import opendream
from PIL import Image


# doing this overrides the default behavior of the default dream operator
# @opendream.define_op
# def dream(prompt: str, model_ckpt: str = "runwayml/stable-diffusion-v1-5", seed: int = 42, device: str = "mps", batch_size: int = 1, selected: int = 0, num_steps: int = 20, guidance_scale: float = 7.5, **kwargs):
#     width, height = 512, 512 
#     dummy_image = Image.new("1", (width, height))
#     return opendream.Layer(dummy_image)
  
# @opendream.define_op 
# def mask_and_inpaint(mask_layer, image_layer, prompt):
#     print("Inpainting dummy")

def create_workflow():
    # image_layer = dream("Quick brown fox jumping over lazy dog")

    # mask_layer = opendream.make_dummy_mask()

    # inpainted_layer = mask_and_inpaint(mask_layer, image_layer, prompt = "make the fox green")

    layers = opendream.execute("workflows/basic_dream.json")

if __name__ == "__main__":

    # create a workflow and save it 
    create_workflow()

    # save workflow
    #opendream.save("initial_pipeline.json")

    # execute workflow from json
    # layers = opendream.execute("initial_pipeline.json")

    # add another layer
    # dream("presidential debate 2024")

    # save new workflow to json
    # opendream.save("final_pipeline.json")
    #layers = opendream.execute("workflows/basic_dream+inpaint.json")