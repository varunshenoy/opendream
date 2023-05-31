from opendream import opendream
from PIL import Image


# doing this overrides the default behavior of the default dream operator
# @opendream.define_op
# def dream(test: str, model_ckpt: str = "runwayml/stable-diffusion-v1-5", seed: int = 42, device: str = "mps", batch_size: int = 1, selected: int = 0, num_steps: int = 20, guidance_scale: float = 7.5, **kwargs):
#     width, height = 512, 512 
#     dummy_image = Image.new("1", (width, height))
#     return opendream.Layer(dummy_image)
  
# @opendream.define_op 
# def mask_and_inpaint(mask_layer, image_layer, prompt):
#     print("Inpainting dummy")

def create_workflow():
    # image_layer = opendream.dream("Quick brown fox jumping over lazy dog")

    # mask_layer = opendream.make_dummy_mask()

    # inpainted_layer = opendream.mask_and_inpaint(mask_layer, image_layer, "green fox")

    # opendream.save("workflows/basic_test.json")
    
    image_layer = opendream.load_image_from_path("test_images/body.png")
    transformed_layer = opendream.controlnet_openpose(image_layer, "oil painting of darth vader in the style of van gogh", model_ckpt="XpucT/Deliberate")
    opendream.save("workflows/basic_load+controlnet_openpose.json")

if __name__ == "__main__":

    # create a workflow and save it 
    # create_workflow()

    # save workflow
    #opendream.save("initial_pipeline.json")
    
    
    # image_layer = opendream.load_image_from_path("test.png")
    
    # print(image_layer)
    
    layers = opendream.execute("workflows/upload+controlnet.json")
    
    
    # opendream.save("workflows/test.json")
    

    # execute workflow from json
    # layers = opendream.execute("initial_pipeline.json")

    # add another layer
    # dream("presidential debate 2024")

    # save new workflow to json
    # opendream.save("final_pipeline.json")
    #layers = opendream.execute("workflows/basic_dream+inpaint.json")