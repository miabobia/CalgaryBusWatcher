from django.db import models

class Bus(models.Model):
    latitude = models.FloatField(default=-1.0)
    longitude = models.FloatField(default=-1.0)
    timestamp = models.BigIntegerField(default=000000000)
    vehicle_id = models.IntegerField(default=1)
    trip_id = models.IntegerField(default=1)
    name = models.TextField(default="DEFAULT_NAME")

class Route(models.Model):
    route_id = models.CharField(max_length=100, primary_key=True)
    route_short_name = models.CharField(max_length=50, blank=True, null=True)
    route_long_name = models.CharField(max_length=200, blank=True, null=True)
    route_desc = models.TextField(blank=True, null=True)
    route_type = models.IntegerField(blank=True, null=True)
    route_url = models.URLField(blank=True, null=True)
    route_color = models.CharField(max_length=6, blank=True, null=True)  # Hex color without #
    route_text_color = models.CharField(max_length=6, blank=True, null=True)  # Hex color without #

class Trip(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, to_field='route_id', db_column='route_id')
    service_id = models.CharField(max_length=100)
    trip_id = models.CharField(max_length=100, primary_key=True)
    trip_headsign = models.CharField(max_length=200, blank=True, null=True)
    direction_id = models.IntegerField(blank=True, null=True)
    block_id = models.CharField(max_length=100, blank=True, null=True)
    shape_id = models.CharField(max_length=100, blank=True, null=True)