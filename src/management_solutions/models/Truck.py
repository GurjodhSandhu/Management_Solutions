from management_solutions.utils.exceptions import InvalidVinError
from management_solutions.utils.exceptions import InvalidYearError
from management_solutions.utils.exceptions import InvalidMileageError
from management_solutions.utils.exceptions import InvalidPlateError
from management_solutions.utils.exceptions import TruckValidationError


class truck:
    def __init__(self,vin = None, brand = None, make= None, year= None, mileage= None, plate = "Asda"):
            errors = {} #dictionary to hold validation errors | each key (parameter) keeps a list of errors for its category

            #VIN validation
            self.vin = vin #vin number of truck
            if vin: #if vin is not None
                if not isinstance(vin,str):
                    if "vin" not in errors: # if no previous errors in dictionary initiallize a list to hold vin errors
                        errors["vin"] = []
                    errors["vin"].append("Invalid VIN: VIN must be a string")
                if len(vin) != 17:
                    if "vin" not in errors: # if no previous errors in dictionary initiallize a list to hold vin errors
                        errors["vin"] = []
                    errors["vin"].append("Invalid VIN: VIN must be 17 characters long")


            self.brand = brand
            self.make = make

            #Year validation
            self.year = year
            if year:
                if not isinstance(year,int): #checks if year is a interger
                    if "year" not in errors:
                        errors["year"] = []
                    errors["year"].append("Year inputted is not a valid number")
                elif year < 1700 or year > 2100: #if year is a number validate further
                    if "year" not in errors:
                        errors["year"] = []
                    errors["year"].append("Year is out of range")

            #Mileage validation
            self.mileage = mileage
            if mileage:
                if not isinstance(mileage,int):
                    if "mileage" not in errors:
                        errors["mileage"] = []
                    errors["mileage"].append("Mileage is not a valid number")
                elif mileage < 0 :
                    if "mileage" not in errors:
                        errors["mileage"] = []
                    errors["mileage"].append("Mileage is in the negative")


            #Plate validation
            self.plate = plate
            if plate:
                if not isinstance(plate,str): #checks if plate is a string
                    if "plate" not in errors:
                        errors["plate"] = []
                    errors["plate"].append("License plate should be a string")
                if len(plate) > 6:
                    if "plate" not in errors:
                        errors["plate"] = []
                    errors["plate"].append("Length of license plate number to high must be 6 or below")

            if errors:
                raise TruckValidationError(errors) #raises all validation errors as a dictionary


    def add_mileage(self,miles):
        self.mileage += miles

    def remove_mileage(self, miles):
        self.mileage -= miles


