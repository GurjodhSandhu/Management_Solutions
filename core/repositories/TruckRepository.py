from django.db.models import QuerySet
from core.models import Truck


def get_truck(truck_id: int) -> Truck | None:
    return Truck.objects.filter(id=truck_id).first()

def get_all_trucks() -> QuerySet:
    return Truck.objects.all()

def delete_truck(truck_id: int) -> tuple[int, dict[str, int]]:
    """
       Deletes a truck by ID.
       Returns:
           (deleted_count, deleted_breakdown)
       """
    return Truck.objects.filter(id=truck_id).delete()
