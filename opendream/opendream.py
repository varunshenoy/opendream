import json

# we need to represent the execution engine here

operators = {}
def dream(dream_func):
    # FLESH OUT PARAM CHECKING, THIS NEEDS TO MATCH SO EXEC ENGINE CAN RUN
    if dream_func.__code__.co_varnames[0] != "prompt":
        raise Exception("dream function must have prompt as first argument")
    operators["dream"] = dream_func
    
def mask_and_inpaint(mask_and_inpaint_func):
    # FLESH OUT PARAM CHECKING, THIS NEEDS TO MATCH SO EXEC ENGINE CAN RUN
    operators["mask_and_inpaint"] = mask_and_inpaint_func

def make_dummy_mask():
    from PIL import Image, ImageDraw

    # Create a blank mask with the size of 512x512
    width, height = 512, 512
    mask = Image.new("1", (width, height))

    # Draw a simple shape on the mask using ImageDraw
    draw = ImageDraw.Draw(mask)
    draw.rectangle([128, 128, 384, 384], fill="white")
    
    mask.save(f"mask_inpaint.png")
                
    return mask


def execute(json_file_path: str):
    with open(json_file_path) as json_file:
        data = json.load(json_file)
        workflow = data["workflow"]
        current_image = None
        for task in workflow:
            if task["operation"] == "dream":
                current_image = operators["dream"](task["prompt"], **task["params"])
            elif task["operation"] == "mask_and_inpaint":
                # print("OK")
                current_image = operators["mask_and_inpaint"](make_dummy_mask(), current_image, task["prompt"], **task["params"])
            else:
                raise Exception("Function not found")
    
    return current_image