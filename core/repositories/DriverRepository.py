from core.models import Driver

def get_driver(driver_id):
    return Driver.objects.filter(id=driver_id).first()

def get_all_drivers():
    return Driver.objects.all()

def delete_driver(driver_id):
     Driver.objects.filter(id=driver_id).delete()
     return True

def get_all_driver_truck(driver_id):
    return list(Driver.objects.filter(id = driver_id))
