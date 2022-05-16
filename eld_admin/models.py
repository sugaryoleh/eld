from django.db.models import Model, IntegerField, PositiveSmallIntegerField, CharField, EmailField, \
    BooleanField, OneToOneField, SET_NULL, ForeignKey, RESTRICT
from phonenumber_field.modelfields import PhoneNumberField

from .validators import *


class Province(Model):
    id = IntegerField(primary_key=True)
    name = CharField(max_length=100)
    abbreviation = CharField(max_length=2, unique=True)


class Group(Model):
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
    license_plate_state = ForeignKey(Province, on_delete=RESTRICT)
    VIN = CharField(unique=True, validators=[validate_VIN])
    group = ForeignKey(Group, on_delete=RESTRICT)


class Truck(Unit):
    pass


class Trailer(Unit):
    pass


class Address:
    pass
    # TODO: create field


class Driver(Model):
    id = IntegerField(primary_key=True)
    first_name = CharField(max_length=35)
    middle_name = CharField(max_length=35)
    last_name = CharField(max_length=35)
    email = EmailField()
    phone = PhoneNumberField(unique=True)
    homeTerminalAddress = ForeignKey(Address, on_delete=RESTRICT)
    eldEnabled = BooleanField()
    truck = OneToOneField(Truck, on_delete=SET_NULL)
    trailer = OneToOneField(Trailer, on_delete=SET_NULL)
    notes = CharField(max_length=500)

