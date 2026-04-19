from management_solutions.utils.exceptions import ValidationError
from management_solutions.utils.validation import validate_int
from management_solutions.utils.validation import validate_str

class truck:
    def __init__(self,truck_id = None,vin = None, brand = None, make= None, year= None, mileage= None, plate = None, assigned_driver_id = None):
            errors = {} #dictionary to hold validation errors | each key (parameter) keeps a list of errors for its category
            self.truck_id = truck_id
            self.vin = vin #vin number of truck
            self.brand = brand
            self.make = make
            self.year = year
            self.mileage = mileage
            self.plate = plate
            self.assigned_driver_id = assigned_driver_id

            self.validate_vin(errors,vin)
            self.validate_year(errors,year)
            self.validate_mileage(errors,mileage)
            self.validate_plate(errors, plate)

            if errors:
                raise ValidationError(errors) #raises all validation errors as a dictionary

    def add_mileage(self,miles):
        self.mileage += miles

    def remove_mileage(self, miles):
        self.mileage -= miles

    def validate_vin(self, errors: dict, vin):
        if vin:  # if vin is not None
            if validate_str(self, errors, "vin"):
                if len(self.vin) != 17:
                    errors.setdefault("vin", []).append("Invalid VIN: VIN must be 17 characters long")

    def validate_year(self,errors: dict, year):
        if year:
            if validate_int(self,errors,"year"): #if year is a int continue
                if self.year < 1700 or self.year > 2100:  # if year is a number validate further
                    errors.setdefault("year", []).append("Year is out of range")

    def validate_mileage(self,errors: dict, mileage):
        if mileage:
            if validate_int(self,errors,"mileage"): #if year is a int continue
                if self.mileage < 0:
                    errors.setdefault("mileage", []).append("Mileage is in the negative")

    def validate_plate(self,errors: dict, plate):
        if plate:
            if validate_str(self,errors, "plate"):
                if len(self.plate) > 6:
                    errors.setdefault("plate", []).append("Length of license plate number to high must be 6 or below")
