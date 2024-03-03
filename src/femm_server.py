import json
import traceback
from typing import Optional
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel, Extra
from __init__ import __version__
from src.executor import Executor


class InputJson(BaseModel):
    simulation: Optional[dict] = {"lua_file": "default"}
    version: Optional[str] = __version__


# Defining the API
app = FastAPI(title="Femm server API", docs_url="/", redoc_url=None)


@app.post("/run", include_in_schema=True, tags=["run"])
async def process(item: InputJson):
    """
    Endpoint for performing the project.run() method on data sent for the API in JSON format.
    The endpoint performs automatic input validation via the Item class.
    """
    data = json.loads(item.model_dump_json())
    try:
        calculation = Executor.run(data['simulation'])
    finally:
        return


def run_femm_server(host: str = "0.0.0.0", port: int = 8900):
    uvicorn.run(app, host=host, port=port, log_level="info")


if __name__ == "__main__":
    run_femm_server()
