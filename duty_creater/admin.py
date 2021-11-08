from django.contrib import admin
from .models import Event, ScheduleModification


# Register your models here.
admin.site.register(Event)
admin.site.register(ScheduleModification)