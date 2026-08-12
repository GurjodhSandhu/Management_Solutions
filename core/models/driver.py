from django.db import models

from .truck import Truck

class Driver(models.Model):
    truck = models.ForeignKey(Truck,on_delete=models.SET_NULL,null=True,blank=True,related_name='drivers')
    driver_name = models.CharField(max_length=10, null=True,blank=True)
    driver_licensenumber = models.CharField(max_length=10, null=True,blank=True)

    def get_trips(self):
        return self.trips.all()

    def __str__(self):
        return f"Driver {self.id}: {self.driver_name}"