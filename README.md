# Opendream

Create layers. Like Photoshop. [insert other stuff here]

## Getting started

Make a virtual environment, and run `bash ./run_opendream.sh`.

## Data model

1. We have a state object, think of this as being analagous to the HTML DOM. 
2. Users add layers - thereby making changes to the state object. 
3. Layers have associated metadata, can have opacities, can be hidden from view, etc. Like Photoshop. 
4. Operators create layers as output. 
5. Delete operator modifies the global layers object
   1. this layers object can be backed up by a datastore which implies it can be sent to other parties etc


## Testing

Run `pytest` from anywhere. Add tests to your code!