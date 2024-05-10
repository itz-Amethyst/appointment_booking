from django.contrib import admin
from appointment_booking.models import Events
@admin.register(Events)
class EventsAdmin(admin.ModelAdmin):
    list_display = ('main_id', 'branch_id', 'off_date', 'reason')
