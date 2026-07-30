from django.db import models
from .truck import Truck

class Driver(models.Model):
    assigned_truck_id = models.ForeignKey(Truck,on_delete=models.SET_NULL,null=True,blank=True,related_name='assigned_driver_id')
    driver_name = models.CharField(max_length=10)
    driver_licensenumber = models.CharField(max_length=10)
