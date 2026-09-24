from django.db.models import QuerySet
from core.models import Driver


def get_driver(driver_id: int) -> Driver | None:
    return Driver.objects.filter(id=driver_id).first()

def get_all_drivers()-> QuerySet:
    return Driver.objects.all()

def delete_driver(driver_id: int) -> bool:
    Driver.objects.filter(id=driver_id).delete()
    return True

def get_all_driver_truck(driver_id: int) -> list[Driver]:
    return list(Driver.objects.filter(id = driver_id))
