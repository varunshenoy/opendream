from fastapi import FastAPI, Body, HTTPException
from . import opendream
from typing import Any, Dict
import inspect

app = FastAPI()

@app.post("/operation/{op_name}")
async def serve(op_name: str, **payload: Dict[str, Any]) -> Dict[str, Any]:

    if op_name not in opendream.operators:
        raise HTTPException(status_code=400, detail=f"Operator {op_name} not found")

    func = opendream.operators[op_name]
    try:
        layer = func(*payload["payload"]["params"], **payload["payload"]["options"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return layer.serialize()

@app.post("/available_operations")
async def available_operations() -> Dict[str, Any]:
    return opendream.operators

@app.post("/schema/{op_name}")
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

# run uvicorn opendream.server:app --reload