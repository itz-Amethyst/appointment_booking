from appointment_booking.admin.generic_picture import GenericPictureInline
from appointment_booking.admin.service import ServiceAdmin
from django.contrib import admin
from appointment_booking.models import Service


class CustomServiceAdmin(ServiceAdmin):
    inlines = [GenericPictureInline]


admin.site.unregister(Service)
admin.site.register(Service, CustomServiceAdmin)