from django.contrib.auth.models import Group, User
from core_transit_app.models import Route, Trip, Bus
from rest_framework import serializers


class RouteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Route
        fields = ['route_id', 'route_short_name', 'route_long_name']

class TripSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Trip
        fields = ['route', 'service_id', 'trip_id']

class BusSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Bus
        fields = ['name', 'vehicle_id', 'latitude', 'longitude', 'timestamp']