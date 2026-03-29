from management_solutions.utils.exceptions import TruckValidationError


class truck:
    def __init__(self,vin = None, brand = None, make= None, year= None, mileage= None, plate = "Asda"):
            errors = {} #dictionary to hold validation errors | each key (parameter) keeps a list of errors for its category

            self.vin = vin #vin number of truck
            self.validate_vin(errors,vin)
            self.brand = brand
            self.make = make
            self.validate_year(errors,year)
            self.mileage = mileage
            self.validate_mileage(errors,mileage)
            self.plate = plate
            self.validate_plate(errors, plate)
            if errors:
                raise TruckValidationError(errors) #raises all validation errors as a dictionary


    def add_mileage(self,miles):
        self.mileage += miles

    def remove_mileage(self, miles):
        self.mileage -= miles

    def validate_vin(self, errors: dict, vin):
        if vin:  # if vin is not None
            if not isinstance(vin, str):
                errors.setdefault("vin", []).append("Invalid VIN: VIN must be a string")
            if len(vin) != 17:
                errors.setdefault("vin", []).append("Invalid VIN: VIN must be 17 characters long")

    def validate_year(self,errors: dict, year):
        if year:
            if not isinstance(year, int):  # checks if year is a interger
                errors.setdefault("year", []).append("Year inputted is not a valid number")
            elif year < 1700 or year > 2100:  # if year is a number validate further
                errors.setdefault("year", []).append("Year is out of range")

    def validate_mileage(self,errors: dict, mileage):
        if mileage:
            if not isinstance(mileage, int):
                errors.setdefault("mileage", []).append("Mileage is not a valid number")
            elif mileage < 0:
                errors.setdefault("mileage", []).append("Mileage is in the negative")

    def validate_plate(self,errors: dict, plate):
        if plate:
            if not isinstance(plate, str):  # checks if plate is a string
                if "plate" not in errors:
                    errors.setdefault("plate", []).append("License plate should be a string")
            if len(plate) > 6:
                errors["plate"].append("Length of license plate number to high must be 6 or below")
