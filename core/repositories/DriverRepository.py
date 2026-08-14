from models import Driver

def get_driver(driver_id):
    return Driver.objects.filter(id=driver_id).first()

def delete_driver(driver_id):
    return Driver.objects.filter(id=driver_id).delete()
