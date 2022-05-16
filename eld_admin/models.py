from django.db.models import Model, IntegerField, PositiveSmallIntegerField, CharField, EmailField, \
    BooleanField, OneToOneField, SET_NULL, ForeignKey, RESTRICT, BigIntegerField, TimeField, DateField, CASCADE

from phonenumber_field.modelfields import PhoneNumberField
from address.models import AddressField, State, Locality

from .validators import *


class UnitGroup(Model):
    id = IntegerField(primary_key=True)
    name = CharField(max_length=50)
    description = CharField(max_length=500)


class Unit(Model):
    id = IntegerField(primary_key=True)
    name = CharField(max_length=10, unique=True)
    year = PositiveSmallIntegerField(validators=[validate_unit_year])
    make = CharField(max_length=50)
    model = CharField(max_length=50)
    license_plate_no = CharField(max_length=20, unique=True)
    license_plate_state = ForeignKey(State, on_delete=RESTRICT)
    VIN = CharField(unique=True, validators=[validate_VIN])
    group = ForeignKey(UnitGroup, on_delete=RESTRICT)

    # TODO: add files


class Truck(Unit):
    pass


class Trailer(Unit):
    pass


class Driver(Model):
    id = IntegerField(primary_key=True)
    first_name = CharField(max_length=35)
    middle_name = CharField(max_length=35)
    last_name = CharField(max_length=35)
    email = EmailField()
    phone = PhoneNumberField(unique=True)
    homeTerminalAddress = ForeignKey(AddressField, on_delete=RESTRICT)
    eldEnabled = BooleanField()
    truck = OneToOneField(Truck, on_delete=SET_NULL)
    trailer = OneToOneField(Trailer, on_delete=SET_NULL)
    notes = CharField(max_length=500)

    # TODO: add file field


class Log(Model):
    id = BigIntegerField(primary_key=True)
    date = DateField()
    shipping_docs_uploaded = BooleanField()
    DVIR_completed = BooleanField()

    # TODO: add file field


class LogProfile(Model):
    id = OneToOneField(Log, on_delete=RESTRICT, primary_key=True)
    driver = ForeignKey(Driver, on_delete=RESTRICT)
    fromAddress = ForeignKey(Locality, on_delete=RESTRICT)
    toAddress = ForeignKey(Locality, on_delete=RESTRICT)
    distance = PositiveSmallIntegerField()
    notes = CharField(max_length=50)

    # TODO: add file field


class Status(Model):
    id = PositiveSmallIntegerField(primary_key=True)
    name = CharField(max_length=10)
    note = CharField(max_length=50)
    optional = BooleanField()


class LogEvent(Model):
    id = BigIntegerField(primary_key=True)
    log = ForeignKey(Log, on_delete=CASCADE)
    status = ForeignKey(Status, on_delete=RESTRICT)
    start_time = TimeField()
    end_time = TimeField()
    truck = ForeignKey(Truck, on_delete=RESTRICT)
    odometer_value = PositiveSmallIntegerField()
    notes = CharField(max_length=40)


