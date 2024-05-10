from django.contrib import admin
from appointment_booking.models import Staff_Times
@admin.register(Staff_Times)
class StaffTimesAdmin(admin.ModelAdmin):

    list_display = ('working_hours', )
