# Opendream: A Better Stable Diffusion Web UI

Opendream brings much needed and familiar features, such as layering, non-destructive editing, portability, and easy-to-write extensions, to your Stable Diffusion workflows.

## Getting started

1. Clone this repository.
2. Navigate to this project within your terminal and run `sh ./run_opendream.sh`. After ~30 seconds, both the frontend and backend of the Opendream system should be up and running.

## Features

Diffusion models have emerged as powerful tools in the world of image generation and manipulation. While they offer significant benefits, these models are often considered black boxes due to their inherent complexity. The current diffusion image generation ecosystem is defined by tools that allow one-off image manipulation tasks to control these models - text2img, in-painting, pix2pix, among others.

For example, popular interfaces like Automatic1111, Midjourney, and Stability.AI's DreamStudio only support destructive editing: each edit "consumes" the previous image. This means users cannot easily build off of previous images or run multiple experiments on the same image, limiting their options for creative exploration.

### Layering and Non-destructive Editing

Non-destructive editing is a method of image manipulation that preserves the original image data while allowing users to make adjustments and modifications without overwriting previous work. This approach facilitates experimentation and provides more control over the editing process by using layers and masks.

Like Photoshop, Opendream supports non-destructive editing out of the box. Learn more here []().

### Save and Share Workflows

Users can also save their current workflows into a portable file format that can be opened up at a later time or shared with collaborators. In this context, a "state" is just a JSON file describing all of the current layers and how they were created.

## Extensions

From the get-go, Opendream supports two key primitive operations baked into the core system: `dream` and `mask_and_inpaint`. In this repository, extensions for `instruct_pix2pix`, `controlnet_canny`, `controlnet_openpose`, and `sam` (Segment Anything) are provided.

### Loading an Existing Extension

There are two ways to load extensions.

1. Install a pre-written one through the Web UI.
2. (Manual) Download a valid extension file (or write one yourself!) and add it to the `opendream/extensions` folder. Keep reading into the next section to learn how to write your own extension.

### Writing Your Own Extension

Users can write their own extensions as follows:

1. Create a new Python file in the `opendream/extensions` folder.
2. Write a method with type hints and a `@opendream.define_op` decorator. This decorator registers this method with the Opendream backend.

The method has a few requirements:

- Parameters must have type hints. These enable the backend to generate a schema for the input which is parsed into form components on the frontend. Valid types include: `str`, `int`, `float`, `Layer`, `MaskLayer`, or `ImageLayer`.
- The only valid return types are a `Layer` or a list of `Layer` objects.

## Contributions and Licensing

Opendream was built by Varun Shenoy, Eric Zhou, Shashank Rammoorthy, and Rahul Shiv as a part of Stanford's CS 348K.

Feel free to provide any contibutions you deem necessary or useful. This project is licensed under the MIT License.
