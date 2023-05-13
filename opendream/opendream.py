import json

# we need to represent the execution engine here

functions = {}
def dream(dream_func):
    # FLESH OUT PARAM CHECKING, THIS NEEDS TO MATCH SO EXEC ENGINE CAN RUN
    if dream_func.__code__.co_varnames[0] != "prompt":
        raise Exception("dream function must have prompt as first argument")
    functions["dream"] = dream_func
    
def mask_and_inpaint(mask_and_inpaint_func):
    # FLESH OUT PARAM CHECKING, THIS NEEDS TO MATCH SO EXEC ENGINE CAN RUN
    functions["mask_and_inpaint"] = mask_and_inpaint_func

def execute(json_file_path: str):
    with open(json_file_path) as json_file:
        data = json.load(json_file)
        workflow = data["workflow"]
        current_image = None
        for task in workflow:
            if task["operation"] == "dream":
                current_image = functions["dream"](task["prompt"], **task["params"])
            elif task["operation"] == "mask_and_inpaint":
                current_image = functions["mask_and_inpaint"](task["mask"], data["image"])
            else:
                raise Exception("Function not found")
    
    return current_image