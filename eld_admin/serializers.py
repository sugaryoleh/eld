from rest_framework.serializers import ModelSerializer, HyperlinkedModelSerializer

from .models import *


class UnitGroupSerializer(ModelSerializer):
    class Meta:
        model = UnitGroup
        fields = ['name', 'description']


class UnitSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Unit
        fields = ['name', 'year', 'make', 'model', 'license_plate_no', 'VIN', 'group']


class TruckSerializer(UnitSerializer):
    class Meta(UnitSerializer.Meta):
        model = Truck


class TrailerSerializer(UnitSerializer):
    class Meta(UnitSerializer.Meta):
        model = Trailer


class DriverSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Driver
        fields = ['url', 'first_name', 'middle_name', 'last_name', 'email', 'phone', 'homeTerminalAddress',
                  'eldEnabled', 'truck', 'trailer', 'notes']
