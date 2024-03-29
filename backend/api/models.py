from django.db import models

class Vehicle(models.Model):
    registration_number = models.CharField(max_length=20)
    type_choices = [
        ('Open Truck', 'Open Truck'),
        ('Dump Truck', 'Dump Truck'),
        ('Compactor', 'Compactor'),
        ('Container Carrier', 'Container Carrier'),
    ]
    type = models.CharField(max_length=20, choices=type_choices)
    capacity = models.DecimalField(max_digits=5, decimal_places=2)
    fuel_cost_loaded = models.DecimalField(max_digits=10, decimal_places=2)
    fuel_cost_unloaded = models.DecimalField(max_digits=10, decimal_places=2)

class STS(models.Model):
    ward_number = models.IntegerField(unique=True) 
    capacity = models.DecimalField(max_digits=5, decimal_places=2)
    latitude = models.FloatField()
    longitude = models.FloatField()

class Landfill(models.Model):
    name = models.CharField(max_length=100)
    capacity = models.DecimalField(max_digits=10, decimal_places=2)
    operational_timespan = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()

class FuelSlip(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    sts = models.ForeignKey(STS, on_delete=models.CASCADE)
    landfill = models.ForeignKey(Landfill, on_delete=models.CASCADE)
    weight_of_waste = models.DecimalField(max_digits=10, decimal_places=2)
    time_of_arrival = models.DateTimeField()
    time_of_departure = models.DateTimeField()


