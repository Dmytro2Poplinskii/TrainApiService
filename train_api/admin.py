from django.contrib import admin

from .models import Crew, Ticket, TrainType, Station, Order, Route, Journey


admin.site.register(Crew)
admin.site.register(Ticket)
admin.site.register(TrainType)
admin.site.register(Station)
admin.site.register(Order)
admin.site.register(Route)
admin.site.register(Journey)
