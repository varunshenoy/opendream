# Opendream: A Web UI For the Rest of Us 💭 🎨

Opendream brings much needed and familiar features, such as layering, non-destructive editing, portability, and easy-to-write extensions, to your Stable Diffusion workflows.

## Getting started

1. Clone this repository.
2. Navigate to this project within your terminal and run `sh ./run_opendream.sh`. After ~30 seconds, both the frontend and backend of the Opendream system should be up and running.

## Features

Diffusion models have emerged as powerful tools in the world of image generation and manipulation. While they offer significant benefits, these models are often considered black boxes due to their inherent complexity. The current diffusion image generation ecosystem is defined by tools that allow one-off image manipulation tasks to control these models - text2img, in-painting, pix2pix, among others.

For example, popular interfaces like [Automatic1111](https://github.com/AUTOMATIC1111/stable-diffusion-webui), [Midjourney](https://midjourney.com/), and [Stability.AI's DreamStudio](https://beta.dreamstudio.ai/generate) only support destructive editing: each edit "consumes" the previous image. This means users cannot easily build off of previous images or run multiple experiments on the same image, limiting their options for creative exploration.

### Layering and Non-destructive Editing

Non-destructive editing is a method of image manipulation that preserves the original image data while allowing users to make adjustments and modifications without overwriting previous work. This approach facilitates experimentation and provides more control over the editing process by using layers and masks.

Like Photoshop, Opendream supports non-destructive editing out of the box. Learn more about the principles of non-destructive editing in Photoshop [here](https://helpx.adobe.com/photoshop/using/nondestructive-editing.html).

### Save and Share Workflows

Users can also save their current workflows into a portable file format that can be opened up at a later time or shared with collaborators. In this context, a "state" is just a JSON file describing all of the current layers and how they were created.

### Support Simple to Write, Easy to Install Extensions

As the open-source ecosystem flourishes around these models and tools, extensibility has also become a major concern. While Automatic1111 does offer extensions, they are often difficult to program, use, and install. It is far from being as full-featured as an application like Adobe Photoshop.

As new features for tools like ControlNet are released, users should be able to seamlessly integrate them into their artistic workflows with minimal overload.

Opendream makes writing and using new diffusion features as simple as writing a Python function. Keep reading to learn how.

## Extensions

From the get-go, Opendream supports two key primitive operations baked into the core system: `dream` and `mask_and_inpaint`. In this repository, extensions for `instruct_pix2pix`, `controlnet_canny`, `controlnet_openpose`, and `sam` (Segment Anything) are provided.

Any image manipulation logic can be easily written as an extension. With extensions, you can also decide how certain operations work. For example, you can override the `dream` operation to use OpenAI's DALL-E instead or call a serverless endpoint on a service like AWS or Replicate. [Here's an example using Modal](https://gist.github.com/varunshenoy/0146a65de2d4db3bad95c2e0e43a66a3).

### Loading an Existing Extension

There are two ways to load extensions.

1. Install a pre-written one through the Web UI.
2. _(Manual)_ Download a valid extension file (or write one yourself!) and add it to the `opendream/extensions` folder. Instructions for writing your own extension are below.

Here is a sampling of currently supported extensions. You can use the links to install any given extension through the Web UI.

| **Extension**                                       | **Link**                                                                                                                                                    |
| --------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| OpenAI's DALL-E                                     | [File](https://gist.githubusercontent.com/varunshenoy/4a9a6bbfedfa7def28178a8f0563320a/raw/d2d10faa0fad8c2d251e599d962b0c7f62c06db0/dalle.py)               |
| Instruct Pix2Pix                                    | [File](https://gist.githubusercontent.com/varunshenoy/894c7a723de6b4651380dd7fa2a81724/raw/fa678d8d6c430421fb481f7023ad76898dd27ad6/instruct_pix2pix.py)    |
| ControlNet Canny                                    | [File](https://gist.githubusercontent.com/varunshenoy/0b0455449454e5856021fe2971b78352/raw/1c08b376b499c25c84976eade71db9aa355dba47/controlnet_canny.py)    |
| ControlNet Openpose                                 | [File](https://gist.githubusercontent.com/varunshenoy/380722906b8ff184569af57e06fd37b7/raw/728832370db0448bc2807ffc9e267635749e6a9f/controlnet_openpose.py) |
| Segment Anything                                    | [File](https://gist.githubusercontent.com/varunshenoy/5fbc883360e5ab2a3c023ce1e286ddd5/raw/efbc92d27ae2209b15948fb52f657e88c185b349/sam.py)                 |
| PhotoshopGPT                                        | [Gist](https://gist.github.com/varunshenoy/63054e7a479f256974416ef45a51e6a0)                                                                                |
| ControlNet Super-resolution (requires a lot of RAM) | [File](https://gist.githubusercontent.com/varunshenoy/9fb80aa0eff0fec4ef4344ae9b108730/raw/cffd5e4542a5232ee0144700650a802e37f0434b/superresolution.py)     |

Feel free to make a PR if you create a useful extension!

### Writing Your Own Extension

Users can write their own extensions as follows:

1. Create a new Python file in the `opendream/extensions` folder.
2. Write a method with type hints and a `@opendream.define_op` decorator. This decorator registers this method with the Opendream backend.

The method has a few requirements:

- Parameters must have type hints. These enable the backend to generate a schema for the input which is parsed into form components on the frontend. Valid types include: `str`, `int`, `float`, `Layer`, `MaskLayer`, or `ImageLayer`.
- The only valid return types are a `Layer` or a list of `Layer` objects.

## Contributions and Licensing

_Opendream was built by Varun Shenoy, Eric Zhou, Shashank Rammoorthy, and Rahul Shiv as a part of Stanford's [CS 348K](https://cs348k.stanford.edu/)._

Feel free to provide any contibutions you deem necessary or useful. This project is licensed under the MIT License.
