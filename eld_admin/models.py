from django.db.models import Model, IntegerField, PositiveSmallIntegerField, CharField, EmailField, \
    BooleanField, OneToOneField, SET_NULL, ForeignKey, RESTRICT, BigIntegerField, TimeField, DateField, CASCADE, \
    ManyToManyField

from phonenumber_field.modelfields import PhoneNumberField
from address.models import AddressField, State, Locality

from .validators import *


class UnitGroup(Model):
    id = IntegerField(primary_key=True)
    name = CharField(max_length=50)
    description = CharField(max_length=500, null=True, blank=True)


class Unit(Model):
    id = IntegerField(primary_key=True)
    name = CharField(max_length=10, unique=True, null=True, blank=True)
    year = PositiveSmallIntegerField(validators=[validate_unit_year], null=True, blank=True)
    make = CharField(max_length=50, null=True, blank=True)
    model = CharField(max_length=50, null=True, blank=True)
    license_plate_no = CharField(max_length=20)
    license_plate_state = ForeignKey(State, on_delete=RESTRICT)
    VIN = CharField(max_length=17, unique=True, validators=[validate_VIN])
    group = ForeignKey(UnitGroup, on_delete=RESTRICT, null=True, blank=True)

    class Meta:
        unique_together = ('license_plate_no', 'license_plate_state')

    # TODO: add files


class Truck(Unit):
    pass


class Trailer(Unit):
    pass


class Driver(Model):
    id = IntegerField(primary_key=True)
    first_name = CharField(max_length=35)
    middle_name = CharField(max_length=35, null=True, blank=True)
    last_name = CharField(max_length=35)
    email = EmailField(null=True, blank=True)
    phone = PhoneNumberField(unique=True, null=True, blank=True)
    homeTerminalAddress = AddressField()
    eldEnabled = BooleanField()
    truck = OneToOneField(Truck, on_delete=SET_NULL, null=True, blank=True, unique=True)
    trailer = OneToOneField(Trailer, on_delete=SET_NULL, null=True, blank=True, unique=True)
    notes = CharField(max_length=500, null=True, blank=True)

    # TODO: add file field


class Log(Model):
    id = BigIntegerField(primary_key=True)
    date = DateField()
    driver = ForeignKey(Driver, on_delete=RESTRICT, null=True)
    fromAddress = Locality()
    toAddress = Locality()
    distance = PositiveSmallIntegerField(null=True, blank=True)
    notes = CharField(max_length=50, null=True, blank=True)
    trucks = ManyToManyField(Truck)
    trailers = ManyToManyField(Trailer)
    shipping_docs_uploaded = BooleanField()
    DVIR_completed = BooleanField()

    class Meta:
        unique_together = ('date', 'driver')
    # TODO: add file field


class Status(Model):
    id = PositiveSmallIntegerField(primary_key=True)
    name = CharField(max_length=10)
    note = CharField(max_length=50, null=True, blank=True)
    optional = BooleanField(default=False)


class LogEvent(Model):
    id = BigIntegerField(primary_key=True)
    log = ForeignKey(Log, on_delete=CASCADE)
    status = ForeignKey(Status, on_delete=RESTRICT)
    start_time = TimeField()
    end_time = TimeField(null=True, blank=True)
    truck = ForeignKey(Truck, on_delete=RESTRICT)
    odometer_value = PositiveSmallIntegerField(null=True, blank=True)
    notes = CharField(max_length=40)


