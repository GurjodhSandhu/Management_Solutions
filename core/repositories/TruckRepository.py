from core.models import Truck

def get_truck(truck_id):
    return Truck.objects.filter(id=truck_id).first()

def get_all_trucks():
    return Truck.objects.all()

def delete_truck(truck_id):
    return Truck.objects.filter(id=truck_id).delete()
