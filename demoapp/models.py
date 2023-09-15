from django.db import models

# Create your models here.
vehicles = [
    ('T1','T1'),
    ('T2W','T2W'),
    ('T2B','T2B'),
]
locations = [
    ('CU','CU'),
    ('NBTC','NBTC'),
]
labels = [
    ('battery','Battery'),
    ('sensing ','Sensing '),
    ('localization', 'Localization'),
    ('planning','Planning'),
    ('computing node', 'Computing Node'),
    ('incident','Incident')
]


class TestLog(models.Model):
    driver = models.CharField(max_length=50)
    date = models.DateField(null=True)
    time = models.TimeField(null=True)
    vehicle = models.CharField(max_length=10, choices=vehicles, null=True)
    location = models.CharField(max_length=10, choices=locations, null=True)
    label = models.CharField(max_length=30, choices=labels, null=True)
    note = models.TextField(null=True)
    stamp = models.DateTimeField(auto_now_add=True)
