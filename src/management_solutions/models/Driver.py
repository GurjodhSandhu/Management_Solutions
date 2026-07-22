from management_solutions.utils.exceptions import ValidationError
from pydantic import BaseModel, ValidationError

class Driver(BaseModel):
    driver_id: int | None = None
    assigned_truck_id: int|None = None
    driver_name: str|None = None
    driver_licensenumber: str|None = None


test1 = Driver(driver_id=1, assigned_truck_id=2, driver_name="", driver_licensenumber="123")
