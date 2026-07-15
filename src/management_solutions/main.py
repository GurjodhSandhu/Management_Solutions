from utils import Truck_util
from database import truck_repository
while True:
    print("""Select option from below
1.add truck 
2.add driver
3.list trucks
4.list drivers
5.assign driver to truck
6.unassign driver from truck 
7.unassign truck from driver
8.exit
----------

""")

    option = input("select option:")
    if option == "1": #add truck
        truck = Truck_util.get_truck_input()
        truck_repository.add_truck(**truck)
        print(truck)
    elif option == "2":
        print()
    elif option == "3":
        print()
    elif option == "4":
        print()
    elif option == "5":
        print()
    elif option == "6":
        print()
    elif option == "7":
        print()
    elif option == "8":
        break



