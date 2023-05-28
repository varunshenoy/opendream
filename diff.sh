diff --git a/.gitignore b/.gitignore
index 6e5d0a8..844cc8e 100644
--- a/.gitignore
+++ b/.gitignore
@@ -1,2 +1,4 @@
 ./models
 **/__pycache__/
+.vscode
+**.pyc
diff --git a/main.py b/main.py
index f46899b..eddff3a 100644
--- a/main.py
+++ b/main.py
@@ -1,8 +1,39 @@
 from opendream import opendream
-
+from PIL import Image
 # doing this overrides the default behavior of the default dream operator
 @opendream.operator
 def dream(prompt: str, model_ckpt: str = "runwayml/stable-diffusion-v1-5", seed: int = 42, device: str = "mps", batch_size: int = 1, selected: int = 0, num_steps: int = 20, guidance_scale: float = 7.5, **kwargs):
-    return "override"
+    width, height = 512, 512 
+    dummy_image = Image.new("1", (width, height))
+    return dummy_image
   
-layers = opendream.execute("workflows/basic_dream+inpaint.json")
\ No newline at end of file
+@opendream.operator 
+def mask_and_inpaint(mask_layer: opendream.layer.Layer, image_layer: opendream.layer.Layer, prompt: str):
+    print("Inpainting dummy")
+
+def create_workflow():
+    image_layer = dream("Quick brown fox jumping over lazy dog")
+
+    mask_layer = opendream.make_dummy_mask()
+
+    inpainted_layer = mask_and_inpaint(mask_layer, image_layer, prompt = "make the fox green")
+
+    opendream.save("opendream.json")
+
+if __name__ == "__main__":
+
+    # create a workflow and save it 
+    #create_workflow()
+
+    # save workflow
+    #opendream.save("initial_pipeline.json")
+
+    # execute workflow from json
+    layers = opendream.execute("initial_pipeline.json")
+
+    # add another layer
+    dream("presidential debate 2024")
+
+    # save new workflow to json
+    opendream.save("final_pipeline.json")
+    #layers = opendream.execute("workflows/basic_dream+inpaint.json")
\ No newline at end of file
diff --git a/opendream/__pycache__/opendream.cpython-311.pyc b/opendream/__pycache__/opendream.cpython-311.pyc
index 91ccc86..c9036ea 100644
Binary files a/opendream/__pycache__/opendream.cpython-311.pyc and b/opendream/__pycache__/opendream.cpython-311.pyc differ
diff --git a/opendream/layer.py b/opendream/layer.py
index 293166a..18fa8be 100644
--- a/opendream/layer.py
+++ b/opendream/layer.py
@@ -8,15 +8,19 @@ import typing
 import uuid
 
 class Layer:
+
     def __init__(self, image: Image.Image, name: str = "", metadata: dict = {}, **kwargs):
         self.image = image
-        self.name = name or uuid.uuid4()
+        self.name = name or uuid.uuid4().hex    # clunky to store entire UUID object, store int for easy JSON writes
         self.metadata = metadata
         self.kwargs = kwargs # kwargs like opacity, etc.
 
     def get_image(self):
         return self.image
     
+    def get_name(self):
+        return self.name
+    
     def get_metadata(self):
         return self.metadata
     
diff --git a/opendream/opendream.py b/opendream/opendream.py
index 7075759..d7bd95a 100644
--- a/opendream/opendream.py
+++ b/opendream/opendream.py
@@ -7,15 +7,31 @@ operators = {}
 
 # TODO: all decorators must return Layer objects
 # decorator to make a function into a dream operator
-def operator(func):
-    def final(f):
-        image = f()
-        l = layer.Layer(image=image)
+def operator(func, layer_name: str = None):
+
+    def wrapper(*args, **kwargs):
+
+        # Run decorated function
+        image = func(*args, **kwargs)
+
+        # iterate through args / kwargs, replace layer objects with layer names (makes metadata compact)
+        lm_args = list(args)   
+        lm_kwargs = kwargs.copy()
+        for i in range(len(lm_args)):
+            lm_args[i] = lm_args[i].get_name() if isinstance(lm_args[i], layer.Layer) else lm_args[i]
+        for key, value in lm_kwargs.items():
+            lm_kwargs[key] = value.get_name() if isinstance(value, layer.Layer) else value
+        
+        # create layer, provide operation and arguments as metadata
+        params = {"op": func.__name__, "args": lm_args, "kwargs": lm_kwargs}
+        l = layer.Layer(image=image, metadata=params, name = layer_name)
+
+        # add to storage
         STORAGE.add_layer(l)
         return l
 
-    operators[func.__name__] = final(func)
-    return func
+    operators[func.__name__] = func 
+    return wrapper
 
 @operator
 def dream(prompt: str, model_ckpt: str = "runwayml/stable-diffusion-v1-5", seed: int = 42, device: str = "mps", batch_size: int = 1, selected: int = 0, num_steps: int = 20, guidance_scale: float = 7.5, **kwargs):
@@ -30,14 +46,30 @@ def make_dummy_mask():
     return reference.make_dummy_mask()
 
 
-# populate the operators dictionary 
-global_vars = globals().copy()
+# # populate the operators dictionary 
+# global_vars = globals().copy()
+
+# # Iterate over global variables
+# for var_name, var_value in global_vars.items():
+#     # Check if the variable is a function decorated with @operator
+#     if callable(var_value) and hasattr(var_value, '__name__') and var_value.__name__ != operator.__name__:
+#         operators[var_value.__name__] = var_value
+
+def save(json_file_path: str = "opendream.json"):
+
+    ordering = STORAGE.get_ordering()
+    data = {}
+
+    # Iterate through layer list, write metadata to dictionary
+    for i, layer_name in enumerate(ordering):
+        layer = STORAGE.get_layer(layer_name)
+        data[layer_name] = layer.get_metadata()
+
+    # Write dictionary to disk
+    with open(json_file_path, 'w') as outfile:
+        json.dump(data, outfile, indent = 4)
+    return
 
-# Iterate over global variables
-for var_name, var_value in global_vars.items():
-    # Check if the variable is a function decorated with @operator
-    if callable(var_value) and hasattr(var_value, '__name__') and var_value.__name__ != operator.__name__:
-        operators[var_value.__name__] = var_value
 
 def execute(json_file_path: str):
     # override operators as necessary
@@ -49,14 +81,18 @@ def execute(json_file_path: str):
         if callable(var_value) and hasattr(var_value, '__name__') and var_value.__name__ != operator.__name__ and hasattr(var_value, '__annotations__'):
             operators[var_value.__name__] = var_value
 
+    # Execute operations outlined in json
     with open(json_file_path) as json_file:
         data = json.load(json_file)
-        workflow = data["workflow"]
-        for task in workflow:
+        for layer_name, layer_metadata in data.items():
             try:
-                operators[task["operation"]](**task["params"])
+                # retrieve function corresponding to json operation
+                func = operators[layer_metadata["op"]]
+
+                # wrap function in @operator and execute
+                layer = operator(func, layer_name)(*layer_metadata["args"], **layer_metadata["kwargs"])
             except Exception as e:
-                print(f"Error executing {task['operation']}: {e}")
+                print(f"Error executing {layer_metadata['op']}: {e}")
                 raise e
 
     return STORAGE
diff --git a/opendream/reference.py b/opendream/reference.py
index 830703a..867f7f6 100644
--- a/opendream/reference.py
+++ b/opendream/reference.py
@@ -19,7 +19,7 @@ def dream(prompt: str, model_ckpt: str = "runwayml/stable-diffusion-v1-5", seed:
     image.save(f"{prompt}_{seed}.png")
     return image
 
-
+# TODO: there should be no concept of "Images" in opendream, just layers. Change args to reflect this.
 def mask_and_inpaint(mask_image: Image.Image, image: Image.Image, prompt: str, model_ckpt: str = "runwayml/stable-diffusion-inpainting", seed: int = 42, device: str = "mps", batch_size: int = 1, selected: int = 0, num_steps: int = 20, guidance_scale: float = 7.5, **kwargs):
     pipe = StableDiffusionInpaintPipeline.from_pretrained(
         model_ckpt,
diff --git a/opendream/storage.py b/opendream/storage.py
index 95aea10..e097103 100644
--- a/opendream/storage.py
+++ b/opendream/storage.py
@@ -2,7 +2,7 @@
 The `Storage` class holds information and helper functions
 for the List[Layer] backend.
 '''
-from layer import Layer
+from .layer import Layer
 
 class Storage:
     # Singleton
@@ -28,3 +28,32 @@ class Storage:
             self.ordering.remove(name)
             return True
         return False
+    
+    def get_ordering(self) -> list[str]:
+        return self.ordering
+    
+    def get_layer(self, name: str) -> Layer:
+        if name in self.layers:
+            return self.layers[name]
+        else:
+            raise KeyError(f"Layer \'{name}\' does not exist.")
+
+    def set_layer_name(self, layer_idx: int, name: str):
+
+        # ensure index is valid
+        if layer_idx >= len(self.ordering):
+            raise ValueError(f"Unable to set name of layer at position {layer_idx} in Storage object")
+       
+        # allow for hash collisions for now..
+        # if name in self.ordering:
+        #     return False
+
+        # I opted not to use a Layer.set_name() function
+        # we don't want users to think they can fiddle with that,
+        # could result in collisions
+        print(f"In set_layer_name: self.layers: {self.layers}")
+        print(f"Name: {name}")
+        self.layers[self.ordering[layer_idx]].name = name
+        self.ordering[layer_idx] = name
+        print(f"In set_layer_name: self.layers: {self.layers}\n\n")
+        return True
\ No newline at end of file
