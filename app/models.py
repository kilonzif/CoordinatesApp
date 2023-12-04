from django.db import models

class Trilateration(models.Model):
    lat1 = models.FloatField()
    lon1 = models.FloatField()
    lat2 = models.FloatField()
    lon2 = models.FloatField()
    lat3 = models.FloatField()
    lon3 = models.FloatField()
    d1 = models.FloatField()
    d2 = models.FloatField()
    d3 = models.FloatField()