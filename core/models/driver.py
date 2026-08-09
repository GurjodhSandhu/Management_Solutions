from django.db import models
from .truck import Truck

class Driver(models.Model):
    truck = models.ForeignKey(Truck,on_delete=models.SET_NULL,null=True,blank=True,related_name='driver')
    driver_name = models.CharField(max_length=10, null=True,blank=True)
    driver_licensenumber = models.CharField(max_length=10, null=True,blank=True)


    def __str__(self):
        return f"{self.driver_name}"