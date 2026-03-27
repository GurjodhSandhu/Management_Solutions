class truck:
    def __init__(self,vin = None, brand = None, make= None, year= None, mileage= None, plate = "Asda"):
            self.vin = vin #vin number of truck
            self.brand = brand
            self.make = make
            self.year = year
            self.mileage = mileage
            self.plate = plate

    def add_mileage(self,miles): #add mileage to truck
        self.mileage += miles

    def remove_mileage(self, miles):  # remove mileage to truck
        self.mileage -= miles


