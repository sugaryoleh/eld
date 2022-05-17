from rest_framework.serializers import ModelSerializer, HyperlinkedModelSerializer

from .models import *


class ProvinceSerializer(ModelSerializer):
    class Meta:
        model = Province
        fields = ['name', 'code']


class AddressSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Address
        fields = ['country', 'province', 'city', 'zip', 'street', 'building']


class UnitGroupSerializer(ModelSerializer):
    class Meta:
        model = UnitGroup
        fields = ['name', 'description']


class UnitSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Unit
        fields = ['name', 'year', 'make', 'model', 'license_plate_no', 'license_plate_state', 'VIN', 'group']


class TruckSerializer(UnitSerializer):
    class Meta(UnitSerializer.Meta):
        model = Truck


class TrailerSerializer(UnitSerializer):
    class Meta(UnitSerializer.Meta):
        model = Trailer


class DriverSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Driver
        fields = ['first_name', 'middle_name', 'last_name', 'email', 'phone', 'home_terminal_address',
                  'eld_enabled', 'truck', 'trailer', 'notes']


class LogSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Log
        fields = ['date', 'driver', 'from_city', 'from_province', 'to_city', 'to_province', 'distance', 'notes',
                  'trucks', 'trailers', 'shipping_docs_uploaded', 'DVIR_completed']


class StatusSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = Status
        fields = ['name', 'note', 'optional']


class LogEventSerializer(HyperlinkedModelSerializer):
    class Meta:
        model = LogEvent
        fields = ['log', 'status', 'start_time', 'end_time', 'truck', 'odometer_value', 'notes']
