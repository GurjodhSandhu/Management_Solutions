from management_solutions.utils.exceptions import InvalidVinError
from management_solutions.utils.exceptions import InvalidYearError
from management_solutions.utils.exceptions import InvalidMileageError
from management_solutions.utils.exceptions import InvalidPlateError

class truck:
    def __init__(self,vin = None, brand = None, make= None, year= None, mileage= None, plate = "Asda"):

            self.vin = vin #vin number of truck

            if vin: #if vin is not None
                if len(vin) != 17: #validation of value
                    raise InvalidVinError("VIN number is length 17") #tracking error


            self.brand = brand
            self.make = make


            self.year = year
            if year:
                if not isinstance(year,int): #checks if mileage is a interger
                    raise InvalidYearError("Year inputted is not a number")
                if year < 1700 or year > 2100:
                    raise InvalidYearError("Year is out of range")


            self.mileage = mileage
            if mileage:
                if mileage < 0 :
                    raise InvalidMileageError("Mileage is in the negative")
                if not isinstance(mileage,int): #checks if mileage is a interger
                    raise InvalidMileageError("Mileage is not a number")


            self.plate = plate
            if plate:
                if len(plate) > 6:
                    raise InvalidPlateError("Length of license plate number to high must be 6 or below")


    def add_mileage(self,miles): #add mileage to truck
        self.mileage += miles

    def remove_mileage(self, miles):  # remove mileage to truck
        self.mileage -= miles


