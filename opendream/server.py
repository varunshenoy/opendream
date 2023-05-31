from fastapi import FastAPI, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from . import opendream
from .layer import Layer
from . import extensions
from typing import Any, Dict
import inspect

app = FastAPI()

# Add CORSMiddleware
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/operation/{op_name}")
async def serve(op_name: str, **payload: Dict[str, Any]) -> Dict[str, Any]:

    if op_name not in opendream.operators:
        raise HTTPException(status_code=400, detail=f"Operator {op_name} not found")
    
    print(payload["payload"]["params"])
    
    # iterate over params, replace base64 images with PIL images
    for i, arg in enumerate(payload["payload"]["params"]):
        if isinstance(payload["payload"]["params"][i], str) and payload["payload"]["params"][i].startswith("data:image/png;base64,"):
            payload["payload"]["params"][i] = Layer.b64_to_layer(payload["payload"]["params"][i])
        
        associated_layer = opendream.CANVAS.get_layer(arg)
        if associated_layer is not None:
            payload["payload"]["params"][i] = associated_layer

    func = opendream.operators[op_name]
    try:
        layer = opendream.define_op(func)(*payload["payload"]["params"], **payload["payload"]["options"])
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

    return layer.serialize()

@app.get("/available_operations")
async def available_operations() -> Dict[str, Any]:
    to_return = {"operators": [op for op in opendream.operators]}
    
    return to_return

@app.get("/schema/{op_name}")
async def schema(op_name: str) -> Dict[str, Any]:
    if op_name not in opendream.operators:
        raise HTTPException(status_code=400, detail=f"Operator {op_name} not found")
    
    params = inspect.signature(opendream.operators[op_name]).parameters

    params = []
    
    for name, param in inspect.signature(opendream.operators[op_name]).parameters.items():
        if name == "kwargs" or name == "args":
            continue
        params.append({
            "name": name,
            "default": param.default if param.default is not inspect.Parameter.empty else None,
            "type": param.annotation.__name__ if param.annotation is not inspect.Parameter.empty else "unknown"
        })
    
    params_dict = {
        "params" : params
    }
    
    return params_dict

@app.get("/state")
async def state() -> Dict[str, Any]:
    return {"layers": opendream.CANVAS.get_serialized_layers(), "workflow": opendream.CANVAS.get_workflow()}

# run uvicorn opendream.server:app --reload