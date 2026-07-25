from pydantic import BaseModel, Field
from typing import Annotated

class Truck(BaseModel):
    truck_id: int|None = None
    vin: Annotated[str|None, Field(min_length=17,max_length=17)] = None
    brand: Annotated[str|None, Field(min_length=1,max_length=25)] = None
    make: Annotated[str|None, Field(min_length=1,max_length=25)] = None
    year: Annotated[int|None, Field(ge=1896,le=2200)] = None
    mileage: Annotated[int|None,Field(ge=0)] = None
    plate: Annotated[str|None, Field(min_length=1,max_length=15)] = None
    assigned_driver_id: int|None = None

    def add_mileage(self, miles):
        try:
            miles = int(miles)
        except (TypeError, ValueError):
            raise TypeError("miles must be an integer")
        if miles < 0:
            raise ValueError("miles cannot be negative")
        self.mileage += miles

    def remove_mileage(self, miles):
        try:
            miles = int(miles)
        except (TypeError, ValueError):
            raise TypeError("miles must be an integer")
        if self.mileage - miles < 0:
            raise ValueError("mileage cannot be negative")
        self.mileage -= miles


