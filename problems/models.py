from django.db import models
from geoposition.fields import GeopositionField

class Customer(models.Model):
    """Customer data for VRPTW problems"""
    name = models.CharField(max_length=255)
    demand = models.IntegerField(default=1)
    ready_time = models.FloatField(default=0.0)
    due_date = models.FloatField(default=0.0)
    service_duration = models.FloatField(default=0.0)
    position = GeopositionField(null=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        """Constructs a string with a customer data"""
        c = {}
        c['customer'] = self.name
        c['position'] = self.position
        c['demand'] = self.demand
        c['ready_time'] = self.ready_time
        c['due_date'] = self.due_date
        c['service_duration'] = self.service_duration
        return str(c)

    class Meta:
        ordering = ['name']

class Problem(models.Model):
    """Instance data for VRPTW problems"""
    name = models.CharField(max_length=255)
    nvehicles = models.IntegerField(default=1)
    capacity = models.IntegerField(default=10)
    depot = models.ForeignKey(Customer, related_name='depot', null=True)
    customers = models.ManyToManyField(Customer)

    def __str__(self):
        return self.name
    
    def __repr__(self):
        """Constructs a string with the problem data"""
        p = {}
        p['name'] = self.name
        p['nvehicles'] = self.nvehicles
        p['capacity'] = self.capacity
        p['ncustomers'] = self.ncustomers
        p['customers'] = self.customers
        return str(p)

    class Meta:
        ordering = ['name']
