# Generated by Django 4.0.4 on 2022-05-16 19:18

import address.models
from django.db import migrations, models
import django.db.models.deletion
import eld_admin.validators
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('address', '0003_auto_20200830_1851'),
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('shipping_docs_uploaded', models.BooleanField()),
                ('DVIR_completed', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.PositiveSmallIntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=10)),
                ('note', models.CharField(max_length=50)),
                ('optional', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=10, unique=True)),
                ('year', models.PositiveSmallIntegerField(validators=[eld_admin.validators.validate_unit_year])),
                ('make', models.CharField(max_length=50)),
                ('model', models.CharField(max_length=50)),
                ('license_plate_no', models.CharField(max_length=20, unique=True)),
                ('VIN', models.CharField(max_length=17, unique=True, validators=[eld_admin.validators.validate_VIN])),
            ],
        ),
        migrations.CreateModel(
            name='UnitGroup',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Trailer',
            fields=[
                ('unit_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='eld_admin.unit')),
            ],
            bases=('eld_admin.unit',),
        ),
        migrations.CreateModel(
            name='Truck',
            fields=[
                ('unit_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='eld_admin.unit')),
            ],
            bases=('eld_admin.unit',),
        ),
        migrations.AddField(
            model_name='unit',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='eld_admin.unitgroup'),
        ),
        migrations.AddField(
            model_name='unit',
            name='license_plate_state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='address.state'),
        ),
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=35)),
                ('middle_name', models.CharField(max_length=35)),
                ('last_name', models.CharField(max_length=35)),
                ('email', models.EmailField(max_length=254)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, unique=True)),
                ('eldEnabled', models.BooleanField()),
                ('notes', models.CharField(max_length=500)),
                ('homeTerminalAddress', address.models.AddressField(on_delete=django.db.models.deletion.CASCADE, to='address.address')),
                ('trailer', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='eld_admin.trailer')),
                ('truck', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='eld_admin.truck')),
            ],
        ),
        migrations.CreateModel(
            name='LogProfile',
            fields=[
                ('id', models.OneToOneField(on_delete=django.db.models.deletion.RESTRICT, primary_key=True, serialize=False, to='eld_admin.log')),
                ('distance', models.PositiveSmallIntegerField()),
                ('notes', models.CharField(max_length=50)),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='eld_admin.driver')),
            ],
        ),
        migrations.CreateModel(
            name='LogEvent',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('odometer_value', models.PositiveSmallIntegerField()),
                ('notes', models.CharField(max_length=40)),
                ('log', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eld_admin.log')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='eld_admin.status')),
                ('truck', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='eld_admin.truck')),
            ],
        ),
    ]