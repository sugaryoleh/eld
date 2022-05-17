from django.contrib import admin

from .models import *


admin.site.register(Province)
admin.site.register(Address)
admin.site.register(UnitGroup)
admin.site.register(Truck)
admin.site.register(Trailer)
admin.site.register(Driver)
admin.site.register(Log)
admin.site.register(Status)
admin.site.register(LogEvent)