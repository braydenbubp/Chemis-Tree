from django.db import models

class Element(models.Model):
    name = models.CharField(max_length=30)
    symbol = models.CharField(max_length=8)
    mass = models.IntegerField()
    group = models.CharField(max_length=50)
