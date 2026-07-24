from management_solutions.utils.exceptions import ValidationError
from pydantic import BaseModel,Field, ValidationError
from typing import Annotated

class Driver(BaseModel):
    driver_id: int | None = None
    assigned_truck_id: int|None = None
    driver_name: Annotated[str|None, Field(min_length=0, max_length=20)] = None
    driver_licensenumber: Annotated[str|None, Field(min_length=4)] = None


try:
    driving = Driver(driver_id=1,assigned_truck_id=1,
                     driver_licensenumber="1234",driver_name="faksssssssssssssssssssssssssssssssssssssssse name")
    print(driving)
except ValidationError as e:
    print(e)
