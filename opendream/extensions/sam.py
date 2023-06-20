import os
import numpy as np
from PIL import Image
from urllib.request import urlretrieve
from segment_anything import SamAutomaticMaskGenerator, sam_model_registry

from opendream import opendream
from opendream.layer import ImageLayer, MaskLayer

def convert_mask_to_layer(mask):
    rle_mask = mask['segmentation']

    # Convert boolean mask to integer (0 or 255) for pixel values
    image_data = np.where(rle_mask, 255, 0).astype(np.uint8)

    # Create a PIL image from the image data
    image = Image.fromarray(image_data, mode='L')

    return MaskLayer(image=image)

def ensure_directory(directory):
    if not os.path.isdir(directory):
        os.makedirs(directory)

def download_file_if_not_exists(url, file_path):
    if not os.path.isfile(file_path):
        print(f"Downloading {os.path.basename(file_path)}...")
        urlretrieve(url, file_path)

@opendream.define_op
def sam(image_layer: ImageLayer):
    
    # we want to download the checkpoint file if it doesn't exist
    checkpoints_dir = "opendream/checkpoints"
    ensure_directory(checkpoints_dir)

    checkpoint_file = "sam_vit_h_4b8939.pth"
    checkpoint_path = os.path.join(checkpoints_dir, checkpoint_file)

    if not os.path.isfile(checkpoint_path):
        print("Downloading SAM checkpoint...")
        url = "https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth"
        download_file_if_not_exists(url, checkpoint_path)
    
    model = sam_model_registry["vit_h"](checkpoint=checkpoint_path)
    mask_generator = SamAutomaticMaskGenerator(model)
    
    image = image_layer.get_image().convert("RGB")
    
    masks = mask_generator.generate(np.array(image))
    return [convert_mask_to_layer(mask) for mask in masks]