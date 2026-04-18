from management_solutions.models.Truck import truck
from management_solutions.utils.exceptions import ValidationError
test_case = {"vin": "1A3456C890VS345A7", "brand": "Volvo", "make": "DB4F", "year": 2026, "mileage": 11500,
                     "plate": "V2A3D2"}

def test_year(value, expected_error): #give input value and expected error
    try:
        test_case = {"vin": "1A3456C890VS345A7", "brand": "Volvo", "make": "DB4F", "year": value, "mileage": 11500,
                     "plate": "V2A3D2"}
        truck(**test_case)
    except ValidationError as e:
        if e.errors["year"][0] == expected_error: #if expected error is caught return pass flag
            print(f"Passed || input: {value} || error: {expected_error}")
            return 1 #pass 0
        else:
            print(f"Failed: input {value} || expected error: {expected_error} NOT caught")
            return 0 #fail
    if expected_error == None:
        print(f"Passed || input: {value} || error: {expected_error}")
        return 1

def test_vin(value, expected_error): #give input value and expected error
    try:
        test_case = {"vin": value, "brand": "Volvo", "make": "DB4F", "year": 20015, "mileage": 11500,
                     "plate": "V2A3D2"}
        truck(**test_case)
    except ValidationError as e:
        if e.errors["vin"][0] == expected_error: #if expected error is caught return pass flag
            print(f"Passed || input: {value} || error: {expected_error}")
            return 1 #pass 0
        else:
            print(f"Failed: input {value} || expected error: {expected_error} NOT caught")
            return 0 #fail
    print("No exception caught: if expected ignore")
    return 0

def test_mileage(value, expected_error): #give input value and expected error
    try:
        test_case = {"vin": "1A3456C890VS345A7", "brand": "Volvo", "make": "DB4F", "year": 2026, "mileage": value,
                     "plate": "V2A3D2"}
        truck(**test_case)
    except ValidationError as e:
        if e.errors["mileage"][0] == expected_error: #if expected error is caught return pass flag
            print(f"Passed || input: {value} || error: {expected_error}")
            return 1 #pass 0
        else:
            print(f"Failed: input {value} || expected error: {expected_error} NOT caught")
            print(e.errors["mileage"][0])
            return 0 #fail
    print("No exception caught: if expected ignore")
    return 0

def test_plate(value, expected_error): #give input value and expected error
    try:
        test_case = {"vin": "1A3456C890VS345A7", "brand": "Volvo", "make": "DB4F", "year": 2026, "mileage": 11500,
                     "plate": value}
        truck(**test_case)
    except ValidationError as e:
        if e.errors["plate"][0] == expected_error: #if expected error is caught return pass flag
            print(f"Passed || input: {value} || error: {expected_error}")
            return 1 #pass 0
        else:
            print(f"Failed: input {value} || expected error: {expected_error} NOT caught")
            return 0 #fail
    print("No exception caught: if expected ignore")
    return 0

print("\n Testing: VIN")
vin = [
test_vin(100,"Invalid VIN: VIN must be 17 characters long"),
test_vin("ABCDE","Invalid VIN: VIN must be 17 characters long"),
test_vin("1234asdbqwdasdqwdasd","Invalid VIN: VIN must be 17 characters long"),

]


passed = sum(vin)
total = len(vin)
print(f"Passed {passed} out of {total} tests")

print("\n Testing: year")
year=[
test_year("string","year inputted is not a valid number"),
test_year(1000,"Year is out of range"),
test_year(3000,"Year is out of range"),
test_year("2003",None),
test_year(2001, None)

]
passed = sum(year)
total = len(year)
print(f"Passed {passed} out of {total} tests")

print("\n Testing: Mileage")
mileage= [
test_mileage("string", "mileage inputted is not a valid number"),
test_mileage(-100, "Mileage is in the negative"),
test_mileage(-10, "Mileage is in the negative"),
test_mileage(-999999, "Mileage is in the negative"),
test_mileage(0, "Mileage is in the negative"),
test_mileage("-12", "Mileage is in the negative")

]
passed = sum(mileage)
total = len(mileage)
print(f"Passed {passed} out of {total} tests")

print("\n Testing: Plate number")
plate = [
test_plate(10000000, "Length of license plate number to high must be 6 or below"),
test_plate("4443123","Length of license plate number to high must be 6 or below"),
test_plate("sgevsewcw","Length of license plate number to high must be 6 or below"),
test_plate("aaaaaaaaaaaaaaaa","Length of license plate number to high must be 6 or below")
]
passed = sum(plate)
total = len(plate)
print(f"Passed {passed} out of {total} tests")

