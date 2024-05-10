from django.contrib import admin
from appointment_booking.models import Booking
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('start_time', 'end_time', 'is_canceled', 'service_id')
