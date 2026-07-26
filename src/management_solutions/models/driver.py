from pydantic import BaseModel,Field
from typing import Annotated

class Driver(BaseModel):
    driver_id: int | None = None
    assigned_truck_id: int|None = None
    driver_name: Annotated[str|None, Field(min_length=0, max_length=20)] = None
    driver_licensenumber: Annotated[str|None, Field(min_length=4)] = None


