from django.contrib.auth.models import User, Group
from django.db.models import Model, IntegerField, PositiveSmallIntegerField, CharField, EmailField, \
    BooleanField, OneToOneField, SET_NULL, ForeignKey, RESTRICT, BigIntegerField, TimeField, DateField, CASCADE, \
    ManyToManyField, AutoField, BigAutoField

from phonenumber_field.modelfields import PhoneNumberField

from .validators import *


class Province(Model):
    id = AutoField(primary_key=True)
    name = CharField(max_length=50)
    code = CharField(max_length=3)

    class Meta:
        unique_together = ('name', 'code')

    def __str__(self):
        return '{}'.format(self.code)


class Address(Model):
    id = AutoField(primary_key=True)
    country = CharField(max_length=56)
    province = ForeignKey(Province, on_delete=RESTRICT)
    city = CharField(max_length=35)
    zip = CharField(max_length=10, validators=[validate_zip_code])
    street = CharField(max_length=35)
    building = PositiveSmallIntegerField()

    def __str__(self):
        province = self.province
        return '{} {}, {}, {} {}, {}'.format(self.building, self.street, self.city, province, self.zip,
                                             self.country)


class UnitGroup(Model):
    id = AutoField(primary_key=True)
    name = CharField(max_length=50)
    description = CharField(max_length=500, null=True, blank=True)


class Unit(Model):
    id = AutoField(primary_key=True)
    name = CharField(max_length=10, unique=True, null=True, blank=True)
    year = PositiveSmallIntegerField(validators=[validate_unit_year], null=True, blank=True)
    make = CharField(max_length=50, null=True, blank=True)
    model = CharField(max_length=50, null=True, blank=True)
    license_plate_no = CharField(max_length=20)
    license_plate_state = ForeignKey(Province, on_delete=RESTRICT)
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
    id = AutoField(primary_key=True)
    user = OneToOneField(User, on_delete=CASCADE, null=True, blank=True)
    first_name = CharField(max_length=35)
    middle_name = CharField(max_length=35, null=True, blank=True)
    last_name = CharField(max_length=35)
    email = EmailField(null=True, blank=True)
    phone = PhoneNumberField(unique=True, null=True, blank=True)
    home_terminal_address = ForeignKey(Address, on_delete=RESTRICT)
    eld_enabled = BooleanField()
    truck = OneToOneField(Truck, on_delete=SET_NULL, null=True, blank=True, unique=True)
    trailer = OneToOneField(Trailer, on_delete=SET_NULL, null=True, blank=True, unique=True)
    notes = CharField(max_length=500, null=True, blank=True)

    def save(self, *args, **kwargs):
        user = User(username=self.email, password=self.email)
        user.save()
        user.groups.add(Group.objects.get(name='Drivers'))
        self.user = user
        super(Driver,self).save(*args, **kwargs)

    # TODO: add file field


class Log(Model):
    id = BigAutoField(primary_key=True)
    date = DateField()
    driver = ForeignKey(Driver, on_delete=RESTRICT, null=True)
    from_city = CharField(max_length=35)
    from_province = ForeignKey(Province, on_delete=RESTRICT, related_name='from_province')
    to_city = CharField(max_length=35)
    to_province = ForeignKey(Province, on_delete=RESTRICT, related_name='to_province')
    distance = PositiveSmallIntegerField(null=True, blank=True)
    notes = CharField(max_length=50, null=True, blank=True)
    trucks = ManyToManyField(Truck, null=True, blank=True)
    trailers = ManyToManyField(Trailer, null=True, blank=True)
    shipping_docs_uploaded = BooleanField(default=False)
    DVIR_completed = BooleanField(default=False)

    class Meta:
        unique_together = ('date', 'driver')
    # TODO: add file field


class Status(Model):
    id = AutoField(primary_key=True)
    name = CharField(max_length=10)
    note = CharField(max_length=50, null=True, blank=True)
    optional = BooleanField(default=False)


class LogEvent(Model):
    id = BigAutoField(primary_key=True)
    log = ForeignKey(Log, on_delete=CASCADE)
    status = ForeignKey(Status, on_delete=RESTRICT)
    start_time = TimeField()
    end_time = TimeField(null=True, blank=True)
    truck = ForeignKey(Truck, on_delete=RESTRICT)
    odometer_value = PositiveSmallIntegerField(null=True, blank=True)
    notes = CharField(max_length=40)
    # todo: add location


