from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from .permissions import IsStuff, IsDriver, IsAdmin, IsManager
from .serializers import UnitGroupSerializer, TruckSerializer, TrailerSerializer, DriverSerializer, LogSerializer, \
    StatusSerializer, LogEventSerializer, ProvinceSerializer, AddressSerializer
from .models import UnitGroup, Truck, Trailer, Driver, Log, Status, LogEvent, Province, Address

from .signals import delete_driver_user


class ProvinceViewSet(ModelViewSet):
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer
    permission_classes = [permissions.IsAuthenticated, IsStuff]


class AddressViewSet(ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated, IsStuff]

    def get_queryset(self):
        country = self.request.query_params.get('country')
        province = self.request.query_params.get('province')
        city = self.request.query_params.get('city')
        zip = self.request.query_params.get('zip')
        street = self.request.query_params.get('street')
        building = self.request.query_params.get('building')

        queryset = self.queryset

        if country is not None:
            queryset = self.queryset.filter(country=country)
        if city is not None:
            queryset = self.queryset.filter(city=city)
        if province is not None:
            queryset = self.queryset.filter(province__code=province)
        if zip is not None:
            queryset = self.queryset.filter(zip=zip)
        if street is not None:
            queryset = self.queryset.filter(street=street)
        if building is not None:
            queryset = self.queryset.filter(building=building)

        return queryset


class UnitGroupViewSet(ModelViewSet):
    queryset = UnitGroup.objects.all()
    serializer_class = UnitGroupSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def get_queryset(self):
        name = self.request.query_params.get('name')
        year = self.request.query_params.get('year')
        make = self.request.query_params.get('make')
        model = self.request.query_params.get('model')
        license_plate_no = self.request.query_params.get('license_plate_no')
        license_plate_province = self.request.query_params.get('license_plate_province')
        VIN = self.request.query_params.get('VIN')
        group = self.request.query_params.get('group')

        queryset = self.queryset

        if name is not None:
            queryset = self.queryset.filter(name=name)
        if name is not None:
            queryset = self.queryset.filter(year=year)
        if make is not None:
            queryset = self.queryset.filter(make=make)
        if model is not None:
            queryset = self.queryset.filter(model=model)
        if license_plate_no is not None:
            queryset = self.queryset.filter(license_plate_no=license_plate_no)
        if license_plate_province is not None:
            queryset = self.queryset.filter(license_plate_province__code=license_plate_province)
        if VIN is not None:
            queryset = self.queryset.filter(VIN=VIN)
        if group is not None:
            queryset = self.queryset.filter(group__name=group)

        return queryset


class TruckViewSet(UnitGroupViewSet):
    queryset = Truck.objects.all()
    serializer_class = TruckSerializer
    permission_classes = [permissions.IsAuthenticated, IsStuff]


class TrailerViewSet(UnitGroupViewSet):
    queryset = Trailer.objects.all()
    serializer_class = TrailerSerializer
    permission_classes = [permissions.IsAuthenticated, IsStuff]


class DriverViewSet(ModelViewSet):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    permission_classes = [permissions.IsAuthenticated, IsStuff]

    def get_queryset(self):
        first_name = self.request.query_params.get('first_name')
        middle_name = self.request.query_params.get('middle_name')
        last_name = self.request.query_params.get('last_name')
        email = self.request.query_params.get('email')
        phone = self.request.query_params.get('phone')
        home_terminal_city = self.request.query_params.get('home_terminal_city')
        home_terminal_province = self.request.query_params.get('home_terminal_province')
        home_terminal_address = self.request.query_params.get('home_terminal_address')
        truck = self.request.query_params.get('truck')
        trailer = self.request.query_params.get('trailer')

        queryset = self.queryset

        if first_name is not None:
            queryset = self.queryset.filter(first_name=first_name)
        if middle_name is not None:
            queryset = self.queryset.filter(middle_name=middle_name)
        if last_name is not None:
            queryset = self.queryset.filter(last_name=last_name)
        if email is not None:
            queryset = self.queryset.filter(email=email)
        if phone is not None:
            queryset = self.queryset.filter(phone=phone)
        if home_terminal_city is not None:
            queryset = self.queryset.filter(home_terminal_address__city=home_terminal_city)
        if home_terminal_province is not None:
            queryset = self.queryset.filter(home_terminal_address__province__code=home_terminal_province)
        if home_terminal_address is not None:
            queryset = self.queryset.filter(home_terminal_address=home_terminal_address)
        if truck is not None:
            queryset = self.queryset.filter(truck__name=truck)
        if trailer is not None:
            queryset = self.queryset.filter(trailer__name=trailer)

        return queryset


class LogViewSet(ModelViewSet):
    queryset = Log.objects.all()
    serializer_class = LogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if IsDriver().has_permission(self.request, self):
            driver = Driver.objects.get(user_id=self.request.user.id)
            queryset = self.queryset.filter(driver_id=driver.id)
            return queryset

        driver = self.request.query_params.get('driver')
        truck = self.request.query_params.get('truck')
        trailer = self.request.query_params.get('trailer')
        shipping_docs_uploaded = self.request.query_params.get('shipping_docs_uploaded')
        DVIR_completed = self.request.query_params.get('DVIR_completed')

        queryset = self.queryset

        if driver is not None:
            queryset = self.queryset.filter(driver=driver)
        if truck is not None:
            queryset = self.queryset.filter(truck__name=truck)
        if trailer is not None:
            queryset = self.queryset.filter(trailer__name=trailer)
        if shipping_docs_uploaded is not None:
            queryset = self.queryset.filter(shipping_docs_uploaded=shipping_docs_uploaded)
        if DVIR_completed is not None:
            queryset = self.queryset.filter(DVIR_completed=DVIR_completed)

        return queryset


class StatusViewSet(ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def get_queryset(self):
        optional = self.request.query_params.get('optional')

        queryset = self.queryset

        if optional is not None:
            queryset = self.queryset.filter(optional=optional)

        return queryset


class LogEventViewSet(ModelViewSet):
    queryset = LogEvent.objects.all()
    serializer_class = LogEventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if IsDriver().has_permission(self.request, self):
            driver = Driver.objects.get(user_id=self.request.user.id)
            truck = driver.truck
            queryset = self.queryset.filter(truck=truck)
            return queryset

        log = self.request.query_params.get('log')
        status = self.request.query_params.get('status')
        truck = self.request.query_params.get('truck')

        queryset = self.queryset

        if log is not None:
            queryset = self.queryset.filter(log=log)
        if status is not None:
            queryset = self.queryset.filter(status__name=status)
        if truck is not None:
            queryset = self.queryset.filter(truck__name=truck)

        return queryset
