from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField

from .models import *


class UnitGroupSerializer(ModelSerializer):
    class Meta:
        model = UnitGroup
        fields = ['name', 'description']


class UnitSerializer(HyperlinkedIdentityField):
    class Meta:
        model = Unit
        fields = ['url', 'name', 'year', 'make', 'model', 'license_plate_no', 'license_plate_state', 'VIN']


class TruckSerializer(UnitSerializer):
    class Meta(UnitSerializer.Meta):
        model = Truck


class TrailerSerializer(UnitSerializer):
    class Meta(UnitSerializer.Meta):
        model = Trailer


class DriverSerializer(Model):
    class Meta:
        model = Driver
        fields = ['url', 'first_name', 'middle_name', 'last_name', 'email', 'phone', 'homeTerminalAddress',
                  'eldEnabled', 'notes']
